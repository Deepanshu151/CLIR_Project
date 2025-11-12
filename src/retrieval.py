"""
Information retrieval module using TF-IDF vectorization and cosine similarity.
"""

import pickle
from pathlib import Path
from typing import List, Tuple
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from src.preprocessing import TextPreprocessor
from src.utils import logger, get_project_root


class DocumentRetriever:
    """Class for document retrieval using TF-IDF and cosine similarity."""
    
    def __init__(self, corpus_path: str = None, load_existing: bool = True):
        """
        Initialize document retriever.
        
        Args:
            corpus_path: Path to corpus file
            load_existing: Whether to load existing vectorizer if available
        """
        self.corpus_path = corpus_path or (get_project_root() / "data" / "english_corpus.txt")
        self.preprocessor = TextPreprocessor(language='english')
        self.vectorizer = None
        self.documents = []
        self.document_vectors = None
        self.model_path = get_project_root() / "models" / "tfidf_vectorizer.pkl"
        
        if load_existing and self.model_path.exists():
            self.load_model()
        else:
            self.load_corpus()
            self.build_index()
    
    def load_corpus(self):
        """Load documents from corpus file."""
        corpus_path = Path(self.corpus_path)
        if not corpus_path.exists():
            logger.warning(f"Corpus file not found: {corpus_path}")
            # Create a sample corpus
            self.documents = [
                "India is a country in South Asia. It is the seventh-largest country by area.",
                "The Prime Minister of India is the head of government of the Republic of India.",
                "New Delhi is the capital of India. It is located in northern India.",
                "The Indian economy is one of the fastest-growing major economies in the world.",
                "Hindi is one of the official languages of India, along with English.",
                "The Indian flag has three horizontal stripes: saffron, white, and green.",
                "India gained independence from British rule on August 15, 1947.",
                "The Indian Parliament consists of two houses: Lok Sabha and Rajya Sabha.",
                "Cricket is the most popular sport in India.",
                "The Ganges is one of the major rivers in India."
            ]
            logger.info("Using default sample corpus")
        else:
            with open(corpus_path, 'r', encoding='utf-8') as f:
                # Split by double newlines or paragraphs
                content = f.read()
                self.documents = [doc.strip() for doc in content.split('\n\n') if doc.strip()]
                if not self.documents:
                    # Fallback to line-by-line if no double newlines
                    f.seek(0)
                    self.documents = [line.strip() for line in f if line.strip()]
        
        logger.info(f"Loaded {len(self.documents)} documents from corpus")
    
    def build_index(self):
        """Build TF-IDF index from documents."""
        logger.info("Building TF-IDF index...")
        
        # Preprocess documents
        preprocessed_docs = [
            self.preprocessor.preprocess_for_retrieval(doc) 
            for doc in self.documents
        ]
        
        # Create TF-IDF vectorizer
        self.vectorizer = TfidfVectorizer(
            max_features=5000,
            ngram_range=(1, 2),  # Unigrams and bigrams
            min_df=1,
            max_df=0.95
        )
        
        # Fit and transform documents
        self.document_vectors = self.vectorizer.fit_transform(preprocessed_docs)
        
        logger.info(f"TF-IDF index built with {self.document_vectors.shape[1]} features")
        
        # Save model
        self.save_model()
    
    def save_model(self):
        """Save vectorizer and document vectors to disk."""
        model_dir = self.model_path.parent
        model_dir.mkdir(parents=True, exist_ok=True)
        
        model_data = {
            'vectorizer': self.vectorizer,
            'document_vectors': self.document_vectors,
            'documents': self.documents
        }
        
        with open(self.model_path, 'wb') as f:
            pickle.dump(model_data, f)
        
        logger.info(f"Model saved to {self.model_path}")
    
    def load_model(self):
        """Load vectorizer and document vectors from disk."""
        try:
            with open(self.model_path, 'rb') as f:
                model_data = pickle.load(f)
            
            self.vectorizer = model_data['vectorizer']
            self.document_vectors = model_data['document_vectors']
            self.documents = model_data['documents']
            
            logger.info(f"Model loaded from {self.model_path}")
        except Exception as e:
            logger.error(f"Failed to load model: {e}")
            self.load_corpus()
            self.build_index()
    
    def retrieve(self, query: str, top_k: int = 5) -> List[Tuple[str, float]]:
        """
        Retrieve top-k most relevant documents for a query.
        
        Args:
            query: Query text (should be in English or preprocessed)
            top_k: Number of top results to return
            
        Returns:
            List of tuples (document, similarity_score) sorted by score
        """
        if self.vectorizer is None or self.document_vectors is None:
            logger.error("Index not built. Building now...")
            self.build_index()
        
        # Preprocess query
        preprocessed_query = self.preprocessor.preprocess_for_retrieval(query)
        
        # Vectorize query
        query_vector = self.vectorizer.transform([preprocessed_query])
        
        # Calculate cosine similarity
        similarities = cosine_similarity(query_vector, self.document_vectors).flatten()
        
        # Get top-k indices
        top_indices = np.argsort(similarities)[::-1][:top_k]
        
        # Build results
        results = []
        for idx in top_indices:
            if similarities[idx] > 0:  # Only include documents with non-zero similarity
                results.append((self.documents[idx], float(similarities[idx])))
        
        logger.info(f"Retrieved {len(results)} documents for query: {query[:50]}...")
        return results
    
    def retrieve_documents(self, query: str, top_k: int = 5) -> List[Tuple[str, float]]:
        """
        Alias for retrieve method.
        
        Args:
            query: Query text
            top_k: Number of top results
            
        Returns:
            List of (document, score) tuples
        """
        return self.retrieve(query, top_k)


# Global retriever instance
_retriever = None


def get_retriever(corpus_path: str = None) -> DocumentRetriever:
    """Get or create global retriever instance."""
    global _retriever
    if _retriever is None:
        _retriever = DocumentRetriever(corpus_path=corpus_path)
    return _retriever


def retrieve_documents(query: str, top_k: int = 5) -> List[Tuple[str, float]]:
    """
    Convenience function to retrieve documents.
    
    Args:
        query: Query text
        top_k: Number of top results
        
    Returns:
        List of (document, score) tuples
    """
    retriever = get_retriever()
    return retriever.retrieve(query, top_k)

