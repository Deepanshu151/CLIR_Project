"""
Utility functions for logging, configuration loading, and helper functions.
"""

import json
import logging
import os
from pathlib import Path
from typing import Dict, Any

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('clir_system.log'),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)


def get_project_root() -> Path:
    """Get the project root directory."""
    return Path(__file__).parent.parent


def load_config(config_path: str = None) -> Dict[str, Any]:
    """Load configuration from JSON file."""
    if config_path is None:
        config_path = get_project_root() / "config.json"
    
    if os.path.exists(config_path):
        with open(config_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    return {}


def save_translation_cache(query: str, translation: str, cache_path: str = None):
    """Save translation to cache to reduce API calls."""
    if cache_path is None:
        cache_path = get_project_root() / "models" / "translations_cache.json"
    
    cache_path = Path(cache_path)
    cache_path.parent.mkdir(parents=True, exist_ok=True)
    
    cache = {}
    if cache_path.exists():
        with open(cache_path, 'r', encoding='utf-8') as f:
            cache = json.load(f)
    
    cache[query] = translation
    
    with open(cache_path, 'w', encoding='utf-8') as f:
        json.dump(cache, f, ensure_ascii=False, indent=2)


def load_translation_cache(cache_path: str = None) -> Dict[str, str]:
    """Load translation cache."""
    if cache_path is None:
        cache_path = get_project_root() / "models" / "translations_cache.json"
    
    cache_path = Path(cache_path)
    if cache_path.exists():
        with open(cache_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    return {}


def log_query(query: str, translated_query: str, results_count: int):
    """Log query and retrieval statistics."""
    logger.info(f"Query: {query}")
    logger.info(f"Translated Query: {translated_query}")
    logger.info(f"Results Retrieved: {results_count}")

