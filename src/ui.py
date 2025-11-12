"""
Streamlit-based user interface for the CLIR system.
"""

import sys
from pathlib import Path

# Ensure project root is available on sys.path when running via `streamlit run`
PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

import streamlit as st
import matplotlib.pyplot as plt
import pandas as pd
from src.translation import translate_query, get_translation_engine
from src.retrieval import retrieve_documents
from src.utils import log_query, logger

# Page configuration
st.set_page_config(
    page_title="CLIR System",
    page_icon="🌍",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
    <style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
    }
    .sub-header {
        font-size: 1.5rem;
        color: #2c3e50;
        margin-top: 1.5rem;
        margin-bottom: 1rem;
    }
    .result-box {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 0.5rem;
        margin: 0.5rem 0;
    }
    .score-badge {
        display: inline-block;
        background-color: #4CAF50;
        color: white;
        padding: 0.25rem 0.75rem;
        border-radius: 1rem;
        font-size: 0.9rem;
        font-weight: bold;
    }
    </style>
""", unsafe_allow_html=True)


def main():
    """Main Streamlit application."""
    
    # Header
    st.markdown('<h1 class="main-header">🌍 Cross-Language Information Retrieval System</h1>', 
                unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Sidebar
    with st.sidebar:
        st.header("⚙️ Settings")
        
        top_k = st.slider("Number of Results", min_value=1, max_value=10, value=5)
        
        show_translation = st.checkbox("Show Translation", value=True)
        show_charts = st.checkbox("Show Similarity Charts", value=True)
        
        st.markdown("---")
        st.markdown("### 📚 Supported Languages")
        st.markdown("""
        - Hindi (हिंदी)
        - English
        - Tamil (தமிழ்)
        - Telugu (తెలుగు)
        - Bengali (বাংলা)
        - And many more...
        """)
        
        st.markdown("---")
        st.markdown("### 💡 Example Queries")
        st.markdown("""
        **Hindi:**
        - भारत का प्रधानमंत्री कौन है?
        - भारत की राजधानी क्या है?
        
        **English:**
        - Who is the Prime Minister of India?
        - What is the capital of India?
        """)
    
    # Main content
    col1, col2 = st.columns([2, 1])
    
    with col1:
        query = st.text_input(
            "🔍 Enter your query (any language):",
            placeholder="e.g., भारत का प्रधानमंत्री कौन है?",
            key="query_input"
        )
    
    with col2:
        st.write("")  # Spacing
        search_button = st.button("🔎 Search", type="primary", use_container_width=True)
    
    if search_button and query:
        with st.spinner("🔄 Translating and retrieving documents..."):
            try:
                # Translate query
                translated_query = translate_query(query, src='auto', dest='en')
                
                # Retrieve documents
                results = retrieve_documents(translated_query, top_k=top_k)
                
                # Log query
                log_query(query, translated_query, len(results))
                
                # Display translated query
                if show_translation:
                    st.markdown('<div class="sub-header">🔹 Translated Query</div>', 
                              unsafe_allow_html=True)
                    st.info(f"**English:** {translated_query}")
                    
                    # Show original query if different
                    if query != translated_query:
                        st.caption(f"**Original:** {query}")
                    
                    st.markdown("---")
                
                # Display results
                st.markdown('<div class="sub-header">📄 Top Retrieved Results</div>', 
                          unsafe_allow_html=True)
                
                if not results:
                    st.warning("No relevant documents found. Try a different query.")
                else:
                    # Create tabs for different views
                    tab1, tab2 = st.tabs(["📋 List View", "📊 Chart View"])
                    
                    with tab1:
                        for i, (doc, score) in enumerate(results, 1):
                            with st.container():
                                st.markdown(f"""
                                <div class="result-box">
                                    <h4>Result #{i} <span class="score-badge">Score: {score:.3f}</span></h4>
                                    <p>{doc}</p>
                                </div>
                                """, unsafe_allow_html=True)
                                st.markdown("<br>", unsafe_allow_html=True)
                    
                    with tab2:
                        if show_charts and results:
                            # Create similarity score chart
                            fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))
                            
                            # Bar chart
                            scores = [score for _, score in results]
                            ranks = [f"Rank {i+1}" for i in range(len(results))]
                            
                            ax1.bar(ranks, scores, color='#4CAF50', alpha=0.7)
                            ax1.set_xlabel('Rank')
                            ax1.set_ylabel('Similarity Score')
                            ax1.set_title('Similarity Scores by Rank')
                            ax1.set_ylim([0, 1])
                            ax1.grid(axis='y', alpha=0.3)
                            
                            # Pie chart (normalized scores)
                            if sum(scores) > 0:
                                ax2.pie(scores, labels=ranks, autopct='%1.1f%%', startangle=90)
                                ax2.set_title('Score Distribution')
                            
                            plt.tight_layout()
                            st.pyplot(fig)
                            
                            # Data table
                            st.markdown("### 📊 Results Summary")
                            df = pd.DataFrame({
                                'Rank': range(1, len(results) + 1),
                                'Similarity Score': scores,
                                'Document Preview': [doc[:100] + '...' if len(doc) > 100 else doc 
                                                    for doc, _ in results]
                            })
                            st.dataframe(df, use_container_width=True, hide_index=True)
                
                # Translation of top results
                if results and show_translation:
                    st.markdown("---")
                    st.markdown('<div class="sub-header">🌐 Translated Results (Hindi)</div>', 
                              unsafe_allow_html=True)
                    
                    engine = get_translation_engine()
                    top_result = results[0][0]  # Get top result
                    translated_result = engine.translate_document(top_result, src='en', dest='hi')
                    
                    st.success(f"**Top Result (Hindi):** {translated_result}")
                
            except Exception as e:
                logger.error(f"Error in UI: {e}")
                st.error(f"❌ An error occurred: {str(e)}")
                st.info("Please try again or check the logs for more details.")
    
    elif search_button and not query:
        st.warning("⚠️ Please enter a query before searching.")
    
    # Footer
    st.markdown("---")
    st.markdown("""
    <div style='text-align: center; color: #666; padding: 2rem;'>
        <p>Cross-Language Information Retrieval System | Built with Streamlit</p>
        <p>Supports multiple languages with automatic translation and TF-IDF-based retrieval</p>
    </div>
    """, unsafe_allow_html=True)


if __name__ == "__main__":
    main()

