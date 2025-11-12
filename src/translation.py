"""
Translation module for handling language translation using googletrans or IndicTrans.
"""

from typing import Optional
from googletrans import Translator, LANGUAGES
from src.utils import save_translation_cache, load_translation_cache, logger


class TranslationEngine:
    """Class for handling translations."""
    
    def __init__(self, use_cache: bool = True):
        """
        Initialize translation engine.
        
        Args:
            use_cache: Whether to use translation cache
        """
        self.translator = Translator()
        self.use_cache = use_cache
        self.cache = load_translation_cache() if use_cache else {}
    
    def detect_language(self, text: str) -> str:
        """
        Detect the language of the input text.
        
        Args:
            text: Input text
            
        Returns:
            Language code (e.g., 'hi', 'en', 'ta')
        """
        try:
            detected = self.translator.detect(text)
            return detected.lang
        except Exception as e:
            logger.warning(f"Language detection failed: {e}")
            return 'auto'
    
    def translate(self, text: str, src: str = 'auto', dest: str = 'en') -> str:
        """
        Translate text from source language to destination language.
        
        Args:
            text: Text to translate
            src: Source language code ('auto' for auto-detection)
            dest: Destination language code (default: 'en')
            
        Returns:
            Translated text
        """
        # Check cache first
        cache_key = f"{text}_{src}_{dest}"
        if self.use_cache and cache_key in self.cache:
            logger.info(f"Using cached translation for: {text[:50]}...")
            return self.cache[cache_key]
        
        try:
            # Auto-detect source language if needed
            if src == 'auto':
                detected_lang = self.detect_language(text)
                if detected_lang == dest:
                    # Already in target language
                    return text
                src = detected_lang
            
            # Translate
            translation = self.translator.translate(text, src=src, dest=dest)
            translated_text = translation.text
            
            # Save to cache
            if self.use_cache:
                self.cache[cache_key] = translated_text
                save_translation_cache(cache_key, translated_text)
            
            logger.info(f"Translated: {text[:50]}... -> {translated_text[:50]}...")
            return translated_text
            
        except Exception as e:
            logger.error(f"Translation failed: {e}")
            # Return original text if translation fails
            return text
    
    def translate_query(self, query: str, dest: str = 'en') -> str:
        """
        Translate a query to the destination language.
        
        Args:
            query: Query text
            dest: Destination language code
            
        Returns:
            Translated query
        """
        return self.translate(query, src='auto', dest=dest)
    
    def translate_document(self, document: str, src: str = 'en', dest: str = 'hi') -> str:
        """
        Translate a document to the destination language.
        
        Args:
            document: Document text
            src: Source language code
            dest: Destination language code
            
        Returns:
            Translated document
        """
        return self.translate(document, src=src, dest=dest)
    
    def get_supported_languages(self) -> dict:
        """
        Get dictionary of supported languages.
        
        Returns:
            Dictionary mapping language codes to language names
        """
        return LANGUAGES


# Global translation engine instance
_translation_engine = None


def get_translation_engine(use_cache: bool = True) -> TranslationEngine:
    """Get or create global translation engine instance."""
    global _translation_engine
    if _translation_engine is None:
        _translation_engine = TranslationEngine(use_cache=use_cache)
    return _translation_engine


def translate_query(query: str, src: str = 'auto', dest: str = 'en') -> str:
    """
    Convenience function to translate a query.
    
    Args:
        query: Query text
        src: Source language code
        dest: Destination language code
        
    Returns:
        Translated query
    """
    engine = get_translation_engine()
    return engine.translate_query(query, dest=dest)

