# test_transformers.py

import logging

try:
    from transformers import pipeline
    print("Transformers pipeline imported successfully.")
except Exception as e:
    print(f"Error importing transformers pipeline: {e}")
    logging.error(f"Error importing transformers pipeline: {e}")
