"""
Script to ingest Hugging Face datasets and store them in Pinecone.
"""
from pathlib import Path
import sys

# Add the project root to the Python path
project_root = Path(__file__).parent.parent
sys.path.append(str(project_root))

from app.core.config import Settings
from app.services.rag_service import RAGService

# List of datasets to ingest: (dataset_path, text_fields, metadata_fields, split, chunk)
DATASETS = [
    ("local_counsel_chat", ["question_text", "answer_text"], [], "train", False),
    ("local_mental_health_counseling", ["Context", "response"], [], "train", False),
    ("local_psych8k", ["input", "output"], [], "train", False),
]

def main(clear_existing: bool = False):
    settings = Settings()
    rag_service = RAGService(settings)

    if clear_existing:
        print("Clearing existing vectors from Pinecone...")
        rag_service.clear_index()

    for dataset_path, text_fields, metadata_fields, split, chunk in DATASETS:
        print(f"\n--- Ingesting {dataset_path} ---")
        try:
            rag_service.process_hf_dataset(
                dataset_name=dataset_path,
                text_fields=text_fields,
                metadata_fields=metadata_fields,
                split=split,
                chunk=chunk
            )
        except Exception as e:
            print(f"Error ingesting {dataset_path}: {e}")

    print("\nDone! Hugging Face datasets are ingested into Pinecone.")

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Ingest Hugging Face datasets into Pinecone knowledge base")
    parser.add_argument("--clear", action="store_true", help="Clear existing vectors before ingestion")
    args = parser.parse_args()
    main(clear_existing=args.clear) 