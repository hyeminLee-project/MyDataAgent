# test_import.py
try:
    from sentence_transformers import SentenceTransformer
    print("sentence_transformers imported successfully!")
except ImportError as e:
    print(f"Error importing sentence_transformers: {e}")
