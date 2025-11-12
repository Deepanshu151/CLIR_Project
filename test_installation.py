"""
Simple test script to verify CLIR system installation.
Run this to check if all dependencies are installed correctly.
"""

import sys
from pathlib import Path

def test_imports():
    """Test if all required modules can be imported."""
    print("Testing imports...")
    
    try:
        import numpy
        print("✅ numpy")
    except ImportError as e:
        print(f"❌ numpy: {e}")
        return False
    
    try:
        import sklearn
        print("✅ scikit-learn")
    except ImportError as e:
        print(f"❌ scikit-learn: {e}")
        return False
    
    try:
        import nltk
        print("✅ nltk")
    except ImportError as e:
        print(f"❌ nltk: {e}")
        return False
    
    try:
        from googletrans import Translator
        print("✅ googletrans")
    except ImportError as e:
        print(f"❌ googletrans: {e}")
        return False
    
    try:
        import streamlit
        print("✅ streamlit")
    except ImportError as e:
        print(f"❌ streamlit: {e}")
        return False
    
    try:
        import pandas
        print("✅ pandas")
    except ImportError as e:
        print(f"❌ pandas: {e}")
        return False
    
    try:
        import matplotlib
        print("✅ matplotlib")
    except ImportError as e:
        print(f"❌ matplotlib: {e}")
        return False
    
    return True

def test_project_modules():
    """Test if project modules can be imported."""
    print("\nTesting project modules...")
    
    # Add src to path
    project_root = Path(__file__).parent
    sys.path.insert(0, str(project_root))
    
    try:
        from src.preprocessing import TextPreprocessor
        print("✅ preprocessing")
    except Exception as e:
        print(f"❌ preprocessing: {e}")
        return False
    
    try:
        from src.translation import translate_query
        print("✅ translation")
    except Exception as e:
        print(f"❌ translation: {e}")
        return False
    
    try:
        from src.retrieval import retrieve_documents
        print("✅ retrieval")
    except Exception as e:
        print(f"❌ retrieval: {e}")
        return False
    
    try:
        from src.evaluation import RetrievalEvaluator
        print("✅ evaluation")
    except Exception as e:
        print(f"❌ evaluation: {e}")
        return False
    
    try:
        from src.utils import logger
        print("✅ utils")
    except Exception as e:
        print(f"❌ utils: {e}")
        return False
    
    return True

def test_basic_functionality():
    """Test basic functionality."""
    print("\nTesting basic functionality...")
    
    try:
        from src.preprocessing import TextPreprocessor
        preprocessor = TextPreprocessor()
        result = preprocessor.preprocess("This is a test query.")
        print(f"✅ Preprocessing works: '{result}'")
    except Exception as e:
        print(f"❌ Preprocessing failed: {e}")
        return False
    
    try:
        # Check if corpus exists
        corpus_path = Path("data/english_corpus.txt")
        if corpus_path.exists():
            print("✅ Corpus file found")
        else:
            print("⚠️  Corpus file not found (will be created on first run)")
    except Exception as e:
        print(f"⚠️  Corpus check failed: {e}")
    
    return True

def main():
    """Run all tests."""
    print("=" * 60)
    print("CLIR System - Installation Test")
    print("=" * 60)
    print()
    
    all_passed = True
    
    # Test imports
    if not test_imports():
        all_passed = False
    
    # Test project modules
    if not test_project_modules():
        all_passed = False
    
    # Test basic functionality
    if not test_basic_functionality():
        all_passed = False
    
    print("\n" + "=" * 60)
    if all_passed:
        print("✅ All tests passed! System is ready to use.")
        print("\nNext steps:")
        print("1. Run: streamlit run src/ui.py")
        print("2. Or run: python -m src.main")
    else:
        print("❌ Some tests failed. Please check the errors above.")
        print("\nTry installing dependencies:")
        print("pip install -r requirements.txt")
    print("=" * 60)

if __name__ == "__main__":
    main()

