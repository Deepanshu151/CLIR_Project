"""
Text preprocessing module for tokenization, stopword removal, and lemmatization.
"""

import re
import string
from typing import List, Set
from pathlib import Path
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer

# Download required NLTK data
try:
    nltk.data.find('tokenizers/punkt')
except LookupError:
    nltk.download('punkt', quiet=True)

try:
    nltk.data.find('corpora/stopwords')
except LookupError:
    nltk.download('stopwords', quiet=True)

try:
    nltk.data.find('corpora/wordnet')
except LookupError:
    nltk.download('wordnet', quiet=True)

try:
    nltk.data.find('taggers/averaged_perceptron_tagger')
except LookupError:
    nltk.download('averaged_perceptron_tagger', quiet=True)


class TextPreprocessor:
    """Class for text preprocessing operations."""
    
    def __init__(self, language: str = 'english'):
        """
        Initialize preprocessor.
        
        Args:
            language: Language for stopwords ('english', 'hindi', etc.)
        """
        self.language = language
        self.lemmatizer = WordNetLemmatizer()
        self.stop_words = self._load_stopwords(language)
    
    def _load_stopwords(self, language: str) -> Set[str]:
        """Load stopwords for the given language."""
        stopwords_set = set()
        
        # Load NLTK stopwords
        try:
            if language == 'english':
                stopwords_set.update(stopwords.words('english'))
        except:
            pass
        
        # Load custom stopwords from file
        custom_stopwords_path = Path(__file__).parent.parent / "data" / "stopwords" / f"{language}_stopwords.txt"
        if custom_stopwords_path.exists():
            with open(custom_stopwords_path, 'r', encoding='utf-8') as f:
                custom_stopwords = [line.strip() for line in f if line.strip()]
                stopwords_set.update(custom_stopwords)
        
        return stopwords_set
    
    def clean_text(self, text: str) -> str:
        """
        Clean text by removing special characters and extra whitespace.
        
        Args:
            text: Input text
            
        Returns:
            Cleaned text
        """
        # Convert to lowercase
        text = text.lower()
        
        # Remove URLs
        text = re.sub(r'http\S+|www\S+|https\S+', '', text, flags=re.MULTILINE)
        
        # Remove email addresses
        text = re.sub(r'\S+@\S+', '', text)
        
        # Remove extra whitespace
        text = re.sub(r'\s+', ' ', text)
        
        # Remove leading/trailing whitespace
        text = text.strip()
        
        return text
    
    def tokenize(self, text: str) -> List[str]:
        """
        Tokenize text into words.
        
        Args:
            text: Input text
            
        Returns:
            List of tokens
        """
        try:
            tokens = word_tokenize(text)
        except:
            # Fallback to simple split if tokenization fails
            tokens = text.split()
        
        return tokens
    
    def remove_stopwords(self, tokens: List[str]) -> List[str]:
        """
        Remove stopwords from tokens.
        
        Args:
            tokens: List of word tokens
            
        Returns:
            List of tokens without stopwords
        """
        return [token for token in tokens if token.lower() not in self.stop_words and token not in string.punctuation]
    
    def lemmatize(self, tokens: List[str]) -> List[str]:
        """
        Lemmatize tokens.
        
        Args:
            tokens: List of word tokens
            
        Returns:
            List of lemmatized tokens
        """
        return [self.lemmatizer.lemmatize(token) for token in tokens]
    
    def preprocess(self, text: str, remove_stopwords_flag: bool = True, lemmatize_flag: bool = True) -> str:
        """
        Complete preprocessing pipeline.
        
        Args:
            text: Input text
            remove_stopwords_flag: Whether to remove stopwords
            lemmatize_flag: Whether to lemmatize
            
        Returns:
            Preprocessed text as a string
        """
        # Clean text
        cleaned_text = self.clean_text(text)
        
        # Tokenize
        tokens = self.tokenize(cleaned_text)
        
        # Remove stopwords
        if remove_stopwords_flag:
            tokens = self.remove_stopwords(tokens)
        
        # Lemmatize
        if lemmatize_flag:
            tokens = self.lemmatize(tokens)
        
        # Join tokens back to string
        preprocessed_text = ' '.join(tokens)
        
        return preprocessed_text
    
    def preprocess_for_retrieval(self, text: str) -> str:
        """
        Preprocess text specifically for retrieval (minimal preprocessing).
        
        Args:
            text: Input text
            
        Returns:
            Preprocessed text
        """
        return self.preprocess(text, remove_stopwords_flag=True, lemmatize_flag=False)

