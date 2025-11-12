# Project Structure Documentation

## Overview
This document describes the complete structure of the Cross-Language Information Retrieval (CLIR) System project.

## Directory Structure

```
CLIR_Project/
│
├── 📁 src/                          # Source code directory
│   ├── __init__.py                  # Package initialization
│   ├── main.py                      # CLI entry point
│   ├── preprocessing.py             # Text preprocessing module
│   ├── translation.py               # Translation engine
│   ├── retrieval.py                 # Document retrieval (TF-IDF)
│   ├── evaluation.py                # Performance evaluation
│   ├── ui.py                        # Streamlit web UI
│   └── utils.py                     # Utility functions
│
├── 📁 data/                         # Data directory
│   ├── english_corpus.txt           # English documents corpus
│   ├── hindi_corpus.txt             # Hindi corpus (optional)
│   └── stopwords/                   # Stopword lists
│       ├── english_stopwords.txt
│       └── hindi_stopwords.txt
│
├── 📁 models/                       # Saved models
│   ├── tfidf_vectorizer.pkl         # TF-IDF model (auto-generated)
│   └── translations_cache.json      # Translation cache (auto-generated)
│
├── 📁 notebooks/                    # Jupyter notebooks
│   ├── data_preparation.ipynb       # Data preprocessing experiments
│   ├── model_training.ipynb         # Model training notebook
│   └── evaluation.ipynb             # Evaluation analysis
│
├── 📁 docs/                         # Documentation
│   ├── PROJECT_STRUCTURE.md         # This file
│   ├── references.txt               # Research references
│   ├── project_report.docx          # Project report (to be created)
│   ├── ppt_presentation.pptx        # Presentation (to be created)
│   └── readme_images/               # Screenshots directory
│
├── 📁 results/                      # Results and outputs
│   ├── sample_queries.json          # Example queries
│   └── performance_metrics.csv      # Evaluation metrics (auto-generated)
│
├── 📁 ui/                           # Flask UI (optional)
│   ├── templates/
│   │   └── index.html
│   ├── static/
│   │   ├── css/
│   │   │   └── style.css
│   │   └── js/
│   │       └── script.js
│   └── app.py
│
├── requirements.txt                 # Python dependencies
├── README.md                        # Project README
└── LICENSE                          # License file (optional)
```

## Module Descriptions

### src/main.py
- Command-line interface for the CLIR system
- Interactive query processing
- Results display

### src/preprocessing.py
- Text cleaning and normalization
- Tokenization
- Stopword removal
- Lemmatization
- Language-specific preprocessing

### src/translation.py
- Language detection
- Query translation (using Google Translate)
- Document translation
- Translation caching

### src/retrieval.py
- TF-IDF vectorization
- Document indexing
- Cosine similarity calculation
- Top-K document retrieval
- Model persistence

### src/evaluation.py
- Precision@K calculation
- Recall@K calculation
- F1-Score@K calculation
- Mean Reciprocal Rank (MRR)
- Batch evaluation

### src/ui.py
- Streamlit web interface
- Interactive query input
- Results visualization
- Charts and graphs
- Translation display

### src/utils.py
- Logging configuration
- Configuration loading
- Translation cache management
- Project path utilities

## Data Files

### english_corpus.txt
- Contains English documents (one per line or paragraph)
- Used as the searchable corpus
- Can be replaced with custom corpus

### stopwords/
- Language-specific stopword lists
- Used for text preprocessing
- Reduces noise in retrieval

## Model Files

### tfidf_vectorizer.pkl
- Serialized TF-IDF vectorizer
- Contains trained model and document vectors
- Auto-generated on first run
- Speeds up subsequent queries

### translations_cache.json
- Cached translations
- Reduces API calls
- Improves performance
- Auto-updated

## Notebooks

### data_preparation.ipynb
- Data loading and exploration
- Preprocessing experiments
- Text analysis

### model_training.ipynb
- TF-IDF model training
- Hyperparameter tuning
- Model evaluation

### evaluation.ipynb
- Performance metrics calculation
- Visualization of results
- Comparative analysis

## Usage Flow

1. **Query Input**: User enters query in any language
2. **Translation**: Query translated to English
3. **Preprocessing**: Query cleaned and normalized
4. **Retrieval**: TF-IDF + Cosine Similarity finds relevant docs
5. **Translation**: Top results translated back to query language
6. **Display**: Results shown with scores and translations

## File Generation

Some files are auto-generated:
- `models/tfidf_vectorizer.pkl` - Created on first run
- `models/translations_cache.json` - Created as translations occur
- `results/performance_metrics.csv` - Created during evaluation
- `clir_system.log` - Created for logging

## Notes

- All paths are relative to project root
- Models are cached for performance
- Translations are cached to reduce API calls
- Logs are written to project root

