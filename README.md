# 🌍 Cross-Language Information Retrieval (CLIR) System

A comprehensive system that retrieves relevant documents or information in one language based on a query entered in another language using NLP and Translation APIs.

## 📋 Project Overview

This project implements a Cross-Language Information Retrieval system that:
- Accepts queries in multiple languages (Hindi, Tamil, Telugu, Bengali, etc.)
- Translates queries to English automatically
- Retrieves relevant documents from an English corpus using TF-IDF and Cosine Similarity
- Returns results in both English and translated target language

### Example Use Case
**Input (Hindi):** "भारत का प्रधानमंत्री कौन है?"  
**Translated:** "Who is the Prime Minister of India?"  
**Output:** Relevant documents about the Prime Minister of India in both English and Hindi

## 🚀 Features

- ✅ Multi-language query support (Hindi, English, Tamil, Telugu, Bengali, and more)
- ✅ Automatic language detection and translation
- ✅ TF-IDF vectorization for document indexing
- ✅ Cosine similarity for relevance ranking
- ✅ Interactive Streamlit UI with visualizations
- ✅ Translation caching to reduce API calls
- ✅ Comprehensive evaluation metrics (Precision, Recall, F1-score)
- ✅ Command-line interface for batch processing
- ✅ Logging and query statistics

## 📁 Project Structure

```
CLIR_Project/
│
├── 📁 src/
│   ├── __init__.py
│   ├── main.py                 # Main entry point (CLI)
│   ├── preprocessing.py        # Text preprocessing
│   ├── translation.py          # Language translation
│   ├── retrieval.py            # TF-IDF retrieval
│   ├── evaluation.py           # Performance metrics
│   ├── ui.py                   # Streamlit UI
│   └── utils.py                # Helper functions
│
├── 📁 data/
│   ├── english_corpus.txt      # English documents corpus
│   ├── hindi_corpus.txt        # Optional Hindi corpus
│   └── stopwords/              # Custom stopword lists
│
├── 📁 models/
│   ├── tfidf_vectorizer.pkl    # Saved TF-IDF model
│   └── translations_cache.json # Translation cache
│
├── 📁 notebooks/
│   ├── data_preparation.ipynb  # Data preprocessing
│   ├── model_training.ipynb    # Model training
│   └── evaluation.ipynb        # Performance analysis
│
├── 📁 docs/
│   ├── project_report.docx     # Project documentation
│   ├── ppt_presentation.pptx   # Presentation slides
│   └── readme_images/          # Screenshots
│
├── 📁 results/
│   ├── sample_queries.json     # Example queries
│   └── performance_metrics.csv # Evaluation results
│
├── requirements.txt            # Python dependencies
└── README.md                   # This file
```

## 🛠️ Installation

### Prerequisites
- Python 3.8 or higher
- pip package manager

### Setup Steps

1. **Clone or download the project**
   ```bash
   cd CLIR_Project
   ```

2. **Create a virtual environment (recommended)**
   ```bash
   python -m venv venv
   
   # On Windows
   venv\Scripts\activate
   
   # On Linux/Mac
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Download NLTK data** (if not automatically downloaded)
   ```python
   import nltk
   nltk.download('punkt')
   nltk.download('stopwords')
   nltk.download('wordnet')
   nltk.download('averaged_perceptron_tagger')
   ```

## 🎯 Usage

### 1. Command-Line Interface

Run the main script for interactive CLI:
```bash
python -m src.main
```

Or:
```bash
python src/main.py
```

### 2. Streamlit Web UI

Launch the interactive web interface:
```bash
streamlit run src/ui.py
```

The UI will open in your default browser at `http://localhost:8501`

### 3. Using as a Python Module

```python
from src.translation import translate_query
from src.retrieval import retrieve_documents

# Translate and retrieve
query = "भारत का प्रधानमंत्री कौन है?"
translated = translate_query(query, src='auto', dest='en')
results = retrieve_documents(translated, top_k=5)

for doc, score in results:
    print(f"Score: {score:.3f} - {doc}")
```

## 📊 Evaluation

Run evaluation on test queries:
```python
from src.evaluation import RetrievalEvaluator

evaluator = RetrievalEvaluator()

# Example: Evaluate a query
metrics = evaluator.evaluate_query(
    query="Who is the Prime Minister of India?",
    relevant_doc_indices=[1, 2],  # Indices of relevant documents
    top_k=5
)

print(metrics)
```

## 🔧 Configuration

The system uses default settings, but you can customize:
- **Corpus path**: Modify `corpus_path` in `retrieval.py`
- **Translation cache**: Automatically saved in `models/translations_cache.json`
- **TF-IDF model**: Saved in `models/tfidf_vectorizer.pkl`

## 📈 Performance Metrics

The system evaluates retrieval using:
- **Precision@K**: Fraction of retrieved documents that are relevant
- **Recall@K**: Fraction of relevant documents that are retrieved
- **F1-Score@K**: Harmonic mean of Precision and Recall
- **MRR**: Mean Reciprocal Rank

## 🌐 Supported Languages

The system supports translation for 100+ languages including:
- Hindi (हिंदी)
- Tamil (தமிழ்)
- Telugu (తెలుగు)
- Bengali (বাংলা)
- English
- And many more via Google Translate API

## 🎨 UI Features

The Streamlit UI includes:
- 🌍 Multi-language query input
- 📊 Interactive similarity score charts
- 📋 List and chart views of results
- 🌐 Automatic translation of top results
- ⚙️ Customizable settings (number of results, display options)
- 💡 Example queries in sidebar

## 📝 Logging

All queries and operations are logged to:
- Console output
- `clir_system.log` file

## 🐛 Troubleshooting

### Issue: Translation API errors
- **Solution**: Check internet connection. Google Translate API may have rate limits.

### Issue: NLTK data not found
- **Solution**: Run the NLTK download commands mentioned in installation.

### Issue: Import errors
- **Solution**: Ensure you're running from the project root directory and all dependencies are installed.

### Issue: Model not found
- **Solution**: The system will automatically build the TF-IDF model on first run if not found.

## 🔮 Future Enhancements

- [ ] Support for more Indian languages
- [ ] BERT multilingual embeddings (mBERT) for improved retrieval
- [ ] Voice input and output (speech-to-text + text-to-speech)
- [ ] Integration with Wikipedia API for dynamic data
- [ ] Advanced UI themes and customization
- [ ] Real-time query suggestions
- [ ] Multi-document summarization

## 📚 References

- TF-IDF: Term Frequency-Inverse Document Frequency
- Cosine Similarity for document matching
- Google Translate API for language translation
- NLTK for natural language processing

## 👥 Contributing

This is an academic project. For improvements or suggestions, please refer to the project documentation.

## 📄 License

This project is for academic/educational purposes.

## 🙏 Acknowledgments

- Google Translate API for translation services
- NLTK and scikit-learn communities
- Streamlit for the web framework

---

**Built with ❤️ for Cross-Language Information Retrieval**

For questions or issues, please refer to the project documentation in the `docs/` folder.

