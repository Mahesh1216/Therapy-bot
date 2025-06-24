"""
Script to ingest PDFs from the Therapy_Guides directory and store them in Pinecone.
"""
from pathlib import Path
import sys
from typing import Optional

# Add the project root to the Python path
project_root = Path(__file__).parent.parent
sys.path.append(str(project_root))

from app.core.config import Settings
from app.services.rag_service import RAGService

def main(clear_existing: bool = False):
    """
    Main function to ingest PDFs and store them in Pinecone.
    
    Args:
        clear_existing: Whether to clear existing vectors from the index
    """
    # Load settings
    settings = Settings()
    
    # Initialize RAG service
    rag_service = RAGService(settings)
    
    # Clear existing vectors if requested
    if clear_existing:
        print("Clearing existing vectors from Pinecone...")
        rag_service.clear_index()
    
    # Process PDFs
    pdf_dir = Path(settings.THERAPY_GUIDES_DIR)
    if not pdf_dir.exists():
        print(f"Error: Directory {pdf_dir} does not exist!")
        return
    
    print(f"Processing PDFs from {pdf_dir}...")
    chunks = rag_service.process_all_pdfs(pdf_dir)
    
    if not chunks:
        print("No chunks were generated from PDFs!")
        return
    
    print(f"Generated {len(chunks)} chunks from PDFs")
    
    # Store chunks in Pinecone
    print("Storing chunks in Pinecone...")
    rag_service.embed_and_store(chunks)
    
    print("Done! Knowledge base is ready for querying.")

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Ingest PDFs into Pinecone knowledge base")
    parser.add_argument("--clear", action="store_true", help="Clear existing vectors before ingestion")
    args = parser.parse_args()
    
    main(clear_existing=args.clear) 