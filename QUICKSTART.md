# Quick Start Guide

## 🚀 Getting Started in 5 Minutes

### Step 1: Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 2: Download NLTK Data (if needed)

The system will automatically download NLTK data on first run, but you can also do it manually:

```python
import nltk
nltk.download('punkt')
nltk.download('stopwords')
nltk.download('wordnet')
nltk.download('averaged_perceptron_tagger')
```

### Step 3: Run the System

#### Option A: Streamlit UI (Recommended)

```bash
streamlit run src/ui.py
```

Then open your browser to `http://localhost:8501`

#### Option B: Command-Line Interface

```bash
python -m src.main
```

#### Option C: Flask UI (Alternative)

```bash
cd ui
python app.py
```

Then open your browser to `http://localhost:5000`

### Step 4: Test with a Query

Try these example queries:

**Hindi:**
- भारत का प्रधानमंत्री कौन है?
- भारत की राजधानी क्या है?

**English:**
- Who is the Prime Minister of India?
- What is the capital of India?

## 📝 First Run Notes

- On first run, the system will:
  1. Load the corpus from `data/english_corpus.txt`
  2. Build the TF-IDF index
  3. Save the model to `models/tfidf_vectorizer.pkl`
  4. This may take a few seconds

- Subsequent runs will be faster as the model is cached.

## 🔧 Troubleshooting

### Issue: ModuleNotFoundError
**Solution:** Make sure you're running from the project root directory.

### Issue: Translation API errors
**Solution:** Check your internet connection. Google Translate API requires internet access.

### Issue: NLTK data not found
**Solution:** Run the NLTK download commands from Step 2.

## 📚 Next Steps

- Explore the Jupyter notebooks in `notebooks/`
- Customize the corpus in `data/english_corpus.txt`
- Review the documentation in `docs/`
- Check out example queries in `results/sample_queries.json`

## 💡 Tips

- The system caches translations to reduce API calls
- You can modify `top_k` parameter to get more/fewer results
- Check `clir_system.log` for detailed operation logs

---

Happy searching! 🌍

