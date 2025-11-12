"""
Evaluation module for measuring retrieval performance (precision, recall, F1-score).
"""

from typing import List, Tuple, Dict
import numpy as np
from src.retrieval import DocumentRetriever
from src.utils import logger


class RetrievalEvaluator:
    """Class for evaluating retrieval performance."""
    
    def __init__(self, retriever: DocumentRetriever = None):
        """
        Initialize evaluator.
        
        Args:
            retriever: DocumentRetriever instance
        """
        self.retriever = retriever or DocumentRetriever()
    
    def precision_at_k(self, retrieved_docs: List[str], relevant_docs: List[str], k: int) -> float:
        """
        Calculate Precision@K.
        
        Args:
            retrieved_docs: List of retrieved document IDs/texts
            relevant_docs: List of relevant document IDs/texts
            k: Number of top results to consider
            
        Returns:
            Precision@K score
        """
        if k == 0 or len(retrieved_docs) == 0:
            return 0.0
        
        top_k_retrieved = retrieved_docs[:k]
        relevant_set = set(relevant_docs)
        
        # Count how many of top-k are relevant
        relevant_retrieved = sum(1 for doc in top_k_retrieved if doc in relevant_set)
        
        return relevant_retrieved / k
    
    def recall_at_k(self, retrieved_docs: List[str], relevant_docs: List[str], k: int) -> float:
        """
        Calculate Recall@K.
        
        Args:
            retrieved_docs: List of retrieved document IDs/texts
            relevant_docs: List of relevant document IDs/texts
            k: Number of top results to consider
            
        Returns:
            Recall@K score
        """
        if len(relevant_docs) == 0:
            return 0.0
        
        top_k_retrieved = retrieved_docs[:k]
        relevant_set = set(relevant_docs)
        retrieved_set = set(top_k_retrieved)
        
        # Count how many relevant docs were retrieved
        relevant_retrieved = len(relevant_set & retrieved_set)
        
        return relevant_retrieved / len(relevant_set)
    
    def f1_score_at_k(self, retrieved_docs: List[str], relevant_docs: List[str], k: int) -> float:
        """
        Calculate F1-Score@K.
        
        Args:
            retrieved_docs: List of retrieved document IDs/texts
            relevant_docs: List of relevant document IDs/texts
            k: Number of top results to consider
            
        Returns:
            F1-Score@K
        """
        precision = self.precision_at_k(retrieved_docs, relevant_docs, k)
        recall = self.recall_at_k(retrieved_docs, relevant_docs, k)
        
        if precision + recall == 0:
            return 0.0
        
        return 2 * (precision * recall) / (precision + recall)
    
    def mean_reciprocal_rank(self, query_results: List[Tuple[str, List[str], List[str]]]) -> float:
        """
        Calculate Mean Reciprocal Rank (MRR).
        
        Args:
            query_results: List of tuples (query, retrieved_docs, relevant_docs)
            
        Returns:
            MRR score
        """
        reciprocal_ranks = []
        
        for query, retrieved_docs, relevant_docs in query_results:
            relevant_set = set(relevant_docs)
            
            # Find rank of first relevant document
            for rank, doc in enumerate(retrieved_docs, 1):
                if doc in relevant_set:
                    reciprocal_ranks.append(1.0 / rank)
                    break
            else:
                # No relevant document found
                reciprocal_ranks.append(0.0)
        
        return np.mean(reciprocal_ranks) if reciprocal_ranks else 0.0
    
    def evaluate_query(self, query: str, relevant_doc_indices: List[int], top_k: int = 5) -> Dict[str, float]:
        """
        Evaluate retrieval for a single query.
        
        Args:
            query: Query text
            relevant_doc_indices: Indices of relevant documents in corpus
            top_k: Number of top results to retrieve
            
        Returns:
            Dictionary of evaluation metrics
        """
        # Retrieve documents
        results = self.retriever.retrieve(query, top_k=top_k)
        retrieved_docs = [doc for doc, score in results]
        
        # Get relevant documents
        relevant_docs = [self.retriever.documents[idx] for idx in relevant_doc_indices 
                        if 0 <= idx < len(self.retriever.documents)]
        
        # Calculate metrics
        metrics = {
            'precision@1': self.precision_at_k(retrieved_docs, relevant_docs, k=1),
            'precision@3': self.precision_at_k(retrieved_docs, relevant_docs, k=3),
            'precision@5': self.precision_at_k(retrieved_docs, relevant_docs, k=5),
            'recall@1': self.recall_at_k(retrieved_docs, relevant_docs, k=1),
            'recall@3': self.recall_at_k(retrieved_docs, relevant_docs, k=3),
            'recall@5': self.recall_at_k(retrieved_docs, relevant_docs, k=5),
            'f1@1': self.f1_score_at_k(retrieved_docs, relevant_docs, k=1),
            'f1@3': self.f1_score_at_k(retrieved_docs, relevant_docs, k=3),
            'f1@5': self.f1_score_at_k(retrieved_docs, relevant_docs, k=5),
        }
        
        return metrics
    
    def evaluate_batch(self, queries: List[Tuple[str, List[int]]], top_k: int = 5) -> Dict[str, float]:
        """
        Evaluate retrieval for multiple queries.
        
        Args:
            queries: List of tuples (query, relevant_doc_indices)
            top_k: Number of top results to retrieve
            
        Returns:
            Dictionary of average evaluation metrics
        """
        all_metrics = []
        
        for query, relevant_indices in queries:
            metrics = self.evaluate_query(query, relevant_indices, top_k)
            all_metrics.append(metrics)
        
        # Calculate averages
        avg_metrics = {}
        for key in all_metrics[0].keys():
            avg_metrics[f'avg_{key}'] = np.mean([m[key] for m in all_metrics])
        
        return avg_metrics

