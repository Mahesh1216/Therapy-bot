"""
RAG (Retrieval Augmented Generation) service for processing and retrieving therapy-related content.
"""
from pathlib import Path
from typing import List, Dict, Optional
import os

import PyPDF2
from langchain.text_splitter import RecursiveCharacterTextSplitter
from sentence_transformers import SentenceTransformer
from pinecone import Pinecone, ServerlessSpec
from tqdm import tqdm
import numpy as np

from app.core.config import Settings
from datasets import load_dataset

class RAGService:
    def __init__(self, settings: Settings):
        """Initialize the RAG service with necessary components."""
        self.settings = settings
        self.model = SentenceTransformer('all-MiniLM-L6-v2')  # Efficient, good performance model
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=500,
            chunk_overlap=80,
            separators=["\n\n", "\n", ". ", " ", ""]
        )
        
        # Initialize Pinecone v4+
        self.index_name = "therapy-knowledge"
        self.pc = Pinecone(api_key=settings.PINECONE_API_KEY)
        
        # Create index if it doesn't exist
        if self.index_name not in self.pc.list_indexes().names():
            self.pc.create_index(
                name=self.index_name,
                dimension=384,  # all-MiniLM-L6-v2 embedding dimension
                metric="cosine",
                spec=ServerlessSpec(cloud="aws", region="us-east-1")  # Adjust if needed
            )
        self.index = self.pc.Index(self.index_name)

    def process_pdf(self, pdf_path: Path) -> List[Dict[str, str]]:
        """
        Process a single PDF file and return chunks with metadata.
        
        Args:
            pdf_path: Path to the PDF file
            
        Returns:
            List of dictionaries containing text chunks and metadata
        """
        chunks = []
        try:
            with open(pdf_path, 'rb') as file:
                pdf_reader = PyPDF2.PdfReader(file)
                
                # Extract text from each page
                full_text = ""
                for page in pdf_reader.pages:
                    text = page.extract_text()
                    if text:
                        full_text += text + "\n\n"
                
                # Split text into chunks
                text_chunks = self.text_splitter.split_text(full_text)
                
                # Create chunks with metadata
                for chunk in text_chunks:
                    chunks.append({
                        'text': chunk,
                        'metadata': {
                            'source': str(pdf_path),
                            'type': 'pdf',
                            'title': pdf_path.stem
                        }
                    })
                
        except Exception as e:
            print(f"Error processing PDF {pdf_path}: {str(e)}")
        
        return chunks

    def process_all_pdfs(self, directory: Path) -> List[Dict[str, str]]:
        """
        Process all PDFs in the given directory.
        
        Args:
            directory: Path to directory containing PDFs
            
        Returns:
            List of all chunks with metadata
        """
        all_chunks = []
        pdf_files = list(directory.glob('**/*.pdf'))
        
        for pdf_path in tqdm(pdf_files, desc="Processing PDFs"):
            chunks = self.process_pdf(pdf_path)
            all_chunks.extend(chunks)
            
        return all_chunks

    def embed_and_store(self, chunks: List[Dict[str, str]]) -> None:
        """
        Embed text chunks and store them in Pinecone.
        
        Args:
            chunks: List of dictionaries containing text chunks and metadata
        """
        batch_size = 100  # Process in batches to manage memory
        
        for i in tqdm(range(0, len(chunks), batch_size), desc="Storing embeddings"):
            batch = chunks[i:i + batch_size]
            
            # Generate embeddings for the batch
            texts = [chunk['text'] for chunk in batch]
            embeddings = self.model.encode(texts)
            
            # Prepare vectors for Pinecone
            vectors = []
            for j, embedding in enumerate(embeddings):
                vector = {
                    'id': f"chunk_{i+j}",
                    'values': embedding.tolist(),
                    'metadata': batch[j]['metadata'] | {'text': batch[j]['text']}
                }
                vectors.append(vector)
            
            # Upsert to Pinecone
            self.index.upsert(vectors=vectors)

    def query(self, query_text: str, top_k: int = 5) -> List[Dict]:
        """
        Query the knowledge base for relevant content.
        
        Args:
            query_text: The query text
            top_k: Number of results to return
            
        Returns:
            List of relevant chunks with their metadata
        """
        # Generate embedding for the query
        query_embedding = self.model.encode(query_text).tolist()
        
        # Query Pinecone
        results = self.index.query(
            vector=query_embedding,
            top_k=top_k,
            include_metadata=True
        )
        
        # Format results
        matches = []
        for match in results['matches']:
            matches.append({
                'text': match['metadata']['text'],
                'source': match['metadata']['source'],
                'score': match['score']
            })
            
        return matches

    def clear_index(self) -> None:
        """Clear all vectors from the Pinecone index."""
        try:
            self.index.delete(delete_all=True)
        except Exception as e:
            # Ignore 'Namespace not found' errors, re-raise others
            if "Namespace not found" not in str(e):
                raise 

    def process_hf_dataset(self, dataset_name: str, text_fields: list, metadata_fields: list = None, split: str = "train", chunk: bool = False) -> None:
        """
        Load a Hugging Face dataset (from hub or local folder), extract text and metadata, chunk if needed, and store in Pinecone.

        Args:
            dataset_name (str): Hugging Face dataset repo name or local folder path (e.g., 'nbertagnolli/counsel-chat' or 'local_counsel_chat')
            text_fields (list): List of field names to concatenate as the main text
            metadata_fields (list, optional): List of field names to include as metadata
            split (str): Which split to use (default 'train')
            chunk (bool): Whether to chunk the text (default False)
        """
        import uuid

        print(f"Loading dataset: {dataset_name} [{split}]")
        if dataset_name.endswith(".csv"):
            ds = load_dataset("csv", data_files=dataset_name)["train"]
        else:
            ds = load_dataset(dataset_name, split=split)
        chunks = []
        for i, row in enumerate(ds):
            # Concatenate text fields
            text = "\n".join([str(row[f]) for f in text_fields if f in row and row[f] is not None])
            if not text.strip():
                continue
            # Optionally chunk
            if chunk:
                text_chunks = self.text_splitter.split_text(text)
            else:
                text_chunks = [text]
            for chunk_text in text_chunks:
                metadata = {"source": dataset_name, "type": "hf", "row_id": i}
                if metadata_fields:
                    for f in metadata_fields:
                        if f in row:
                            metadata[f] = row[f]
                chunks.append({
                    "text": chunk_text,
                    "metadata": metadata
                })
        print(f"Prepared {len(chunks)} chunks from {dataset_name}")
        if chunks:
            self.embed_and_store(chunks)
        else:
            print(f"No valid chunks found for {dataset_name}") 