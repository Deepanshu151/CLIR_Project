"""
Main entry point for the CLIR system (command-line interface).
"""

from src.translation import translate_query
from src.preprocessing import TextPreprocessor
from src.retrieval import retrieve_documents
from src.utils import log_query, logger


def main():
    """Main function for command-line interface."""
    print("=" * 60)
    print("🌍 Cross-Language Information Retrieval (CLIR) System")
    print("=" * 60)
    print("\nEnter your query in any language (e.g., Hindi, Tamil, etc.)")
    print("Type 'exit' to quit.\n")
    
    while True:
        try:
            query = input("Query: ").strip()
            
            if query.lower() in ['exit', 'quit', 'q']:
                print("\nThank you for using CLIR System!")
                break
            
            if not query:
                print("Please enter a valid query.\n")
                continue
            
            print("\n🔄 Processing query...")
            
            # Translate query
            print("📝 Translating query...")
            translated_query = translate_query(query, src='auto', dest='en')
            print(f"✅ Translated Query (English): {translated_query}\n")
            
            # Retrieve documents
            print("🔍 Retrieving documents...")
            results = retrieve_documents(translated_query, top_k=5)
            
            # Log query
            log_query(query, translated_query, len(results))
            
            # Display results
            print("\n" + "=" * 60)
            print("📄 Top Retrieved Documents:")
            print("=" * 60)
            
            if not results:
                print("No relevant documents found.")
            else:
                for rank, (doc, score) in enumerate(results, 1):
                    print(f"\n{rank}. Score: {score:.3f}")
                    print(f"   {doc[:200]}{'...' if len(doc) > 200 else ''}")
            
            print("\n" + "=" * 60 + "\n")
            
        except KeyboardInterrupt:
            print("\n\nExiting...")
            break
        except Exception as e:
            logger.error(f"Error processing query: {e}")
            print(f"\n❌ Error: {e}\n")


if __name__ == "__main__":
    main()

