"""
Flask-based web UI for CLIR System (Alternative to Streamlit)
"""

from flask import Flask, render_template, request, jsonify
import sys
from pathlib import Path

# Add src to path
sys.path.append(str(Path(__file__).parent.parent))

from src.translation import translate_query, get_translation_engine
from src.retrieval import retrieve_documents
from src.utils import log_query, logger

app = Flask(__name__)


@app.route('/')
def index():
    """Render main page."""
    return render_template('index.html')


@app.route('/search', methods=['POST'])
def search():
    """Handle search query."""
    try:
        data = request.get_json()
        query = data.get('query', '').strip()
        top_k = data.get('top_k', 5)
        
        if not query:
            return jsonify({'error': 'Query is required'}), 400
        
        # Translate query
        translated_query = translate_query(query, src='auto', dest='en')
        
        # Retrieve documents
        results = retrieve_documents(translated_query, top_k=top_k)
        
        # Log query
        log_query(query, translated_query, len(results))
        
        # Translate top result to Hindi
        translated_result = None
        if results:
            engine = get_translation_engine()
            translated_result = engine.translate_document(results[0][0], src='en', dest='hi')
        
        # Format results
        formatted_results = [
            {
                'document': doc,
                'score': float(score)
            }
            for doc, score in results
        ]
        
        return jsonify({
            'success': True,
            'original_query': query,
            'translated_query': translated_query,
            'results': formatted_results,
            'translated_top_result': translated_result
        })
        
    except Exception as e:
        logger.error(f"Error in search: {e}")
        return jsonify({'error': str(e)}), 500


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)

