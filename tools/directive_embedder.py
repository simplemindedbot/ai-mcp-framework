#!/usr/bin/env python3
"""
Dynamic Directive Embedding System

Implements semantic chunking, local embedding, and retrieval of AI behavioral
directives for maximum token efficiency while maintaining behavioral integrity.
"""

import json
import pickle
import hashlib
import numpy as np
from pathlib import Path
from typing import Dict, List, Optional, Tuple, Any
from dataclasses import dataclass, asdict
import re

try:
    from sentence_transformers import SentenceTransformer
    TRANSFORMERS_AVAILABLE = True
except ImportError:
    TRANSFORMERS_AVAILABLE = False
    print("⚠️  sentence-transformers not installed. Using fallback TF-IDF embeddings.")

try:
    import faiss
    FAISS_AVAILABLE = True
except ImportError:
    FAISS_AVAILABLE = False
    print("⚠️  faiss not installed. Using numpy similarity search.")

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

@dataclass
class DirectiveChunk:
    """Represents a semantic chunk of a directive."""
    id: str
    content: str
    metadata: Dict[str, Any]
    embedding: Optional[np.ndarray] = None
    priority: int = 1  # 1=highest, 5=lowest
    context_tags: List[str] = None
    
    def __post_init__(self):
        if self.context_tags is None:
            self.context_tags = []

@dataclass
class RetrievalContext:
    """Context for directive retrieval."""
    query: str
    user_intent: Optional[str] = None
    current_tools: List[str] = None
    session_history: List[str] = None
    token_budget: Optional[int] = None
    
    def __post_init__(self):
        if self.current_tools is None:
            self.current_tools = []
        if self.session_history is None:
            self.session_history = []

class DirectiveEmbedder:
    """Manages embedding and retrieval of directive chunks."""
    
    def __init__(self, cache_dir: str = None):
        self.cache_dir = Path(cache_dir) if cache_dir else Path.home() / ".ai-mcp-framework" / "embeddings"
        self.cache_dir.mkdir(parents=True, exist_ok=True)
        
        self.chunks: Dict[str, DirectiveChunk] = {}
        self.embeddings_matrix: Optional[np.ndarray] = None
        self.chunk_ids: List[str] = []
        
        # Initialize embedding model
        if TRANSFORMERS_AVAILABLE:
            self.model = SentenceTransformer('all-MiniLM-L6-v2')  # Lightweight but effective
            self.embedding_dim = 384
            print("✅ Using SentenceTransformer embeddings")
        else:
            self.model = TfidfVectorizer(max_features=1000, stop_words='english')
            self.embedding_dim = 1000
            print("✅ Using TF-IDF embeddings")
        
        # Initialize vector search
        if FAISS_AVAILABLE:
            self.index = None
            print("✅ FAISS available for fast similarity search")
        else:
            print("✅ Using numpy cosine similarity")
        
        # Load cached embeddings if available
        self._load_cache()
    
    def chunk_directive(self, directive_path: str, chunk_strategy: str = "semantic") -> List[DirectiveChunk]:
        """
        Chunk directive into semantic pieces.
        
        Strategies:
        - semantic: Based on content structure and meaning
        - paragraph: Split by paragraphs  
        - sentence: Split by sentences
        - hybrid: Combination approach
        """
        with open(directive_path, 'r') as f:
            content = f.read()
        
        if chunk_strategy == "semantic":
            return self._semantic_chunking(content, directive_path)
        elif chunk_strategy == "paragraph":
            return self._paragraph_chunking(content, directive_path)
        elif chunk_strategy == "sentence":
            return self._sentence_chunking(content, directive_path)
        elif chunk_strategy == "hybrid":
            return self._hybrid_chunking(content, directive_path)
        else:
            raise ValueError(f"Unknown chunking strategy: {chunk_strategy}")
    
    def _semantic_chunking(self, content: str, source: str) -> List[DirectiveChunk]:
        """Intelligent semantic chunking based on directive structure."""
        chunks = []
        
        # Define semantic boundaries for directive content
        section_patterns = [
            (r'(INITIALIZATION PHASE.*?)(?=EXECUTION PHASE|$)', 'initialization', 1),
            (r'(EXECUTION PHASE.*?)(?=VALIDATION PHASE|$)', 'execution', 1), 
            (r'(VALIDATION PHASE.*?)(?=TOKEN|OVERRIDE|$)', 'validation', 1),
            (r'(TOKEN.*?RULES.*?)(?=OVERRIDE|LEARNING|$)', 'token_rules', 1),
            (r'(OVERRIDE.*?)(?=SUCCESS|EMERGENCY|$)', 'overrides', 2),
            (r'(EMERGENCY.*?)(?=SUCCESS|LOOKUP|$)', 'emergency', 1),
            (r'(SUCCESS.*?)(?=LOOKUP|$)', 'success_metrics', 3),
            (r'(LOOKUP.*?)(?=$)', 'lookup', 5),
            (r'(@[A-Z]=.*?)(?=@[A-Z]=|$)', 'symbol_def', 4),
        ]
        
        for pattern, tag, priority in section_patterns:
            matches = re.finditer(pattern, content, re.DOTALL | re.IGNORECASE)
            for match in matches:
                chunk_content = match.group(1).strip()
                if len(chunk_content) > 20:  # Skip very short chunks
                    chunk_id = hashlib.md5(chunk_content.encode()).hexdigest()[:12]
                    
                    chunk = DirectiveChunk(
                        id=chunk_id,
                        content=chunk_content,
                        metadata={
                            'source': source,
                            'section': tag,
                            'length': len(chunk_content),
                            'strategy': 'semantic'
                        },
                        priority=priority,
                        context_tags=[tag, 'directive']
                    )
                    chunks.append(chunk)
        
        # If no semantic matches, fall back to paragraph chunking
        if not chunks:
            return self._paragraph_chunking(content, source)
        
        return chunks
    
    def _paragraph_chunking(self, content: str, source: str) -> List[DirectiveChunk]:
        """Split content by paragraphs."""
        chunks = []
        paragraphs = [p.strip() for p in content.split('\n\n') if p.strip()]
        
        for i, paragraph in enumerate(paragraphs):
            if len(paragraph) > 20:
                chunk_id = hashlib.md5(paragraph.encode()).hexdigest()[:12]
                
                chunk = DirectiveChunk(
                    id=chunk_id,
                    content=paragraph,
                    metadata={
                        'source': source,
                        'paragraph_index': i,
                        'length': len(paragraph),
                        'strategy': 'paragraph'
                    },
                    priority=2,
                    context_tags=['directive', 'paragraph']
                )
                chunks.append(chunk)
        
        return chunks
    
    def _sentence_chunking(self, content: str, source: str) -> List[DirectiveChunk]:
        """Split content by sentences."""
        chunks = []
        sentences = re.split(r'[.!?]+', content)
        
        for i, sentence in enumerate(sentences):
            sentence = sentence.strip()
            if len(sentence) > 10:
                chunk_id = hashlib.md5(sentence.encode()).hexdigest()[:12]
                
                chunk = DirectiveChunk(
                    id=chunk_id,
                    content=sentence,
                    metadata={
                        'source': source,
                        'sentence_index': i,
                        'length': len(sentence),
                        'strategy': 'sentence'
                    },
                    priority=3,
                    context_tags=['directive', 'sentence']
                )
                chunks.append(chunk)
        
        return chunks
    
    def _hybrid_chunking(self, content: str, source: str) -> List[DirectiveChunk]:
        """Combination of semantic and paragraph chunking."""
        semantic_chunks = self._semantic_chunking(content, source)
        
        # If semantic chunking produced good results, use it
        if len(semantic_chunks) >= 3:
            return semantic_chunks
        
        # Otherwise, fall back to paragraph chunking
        return self._paragraph_chunking(content, source)
    
    def embed_chunks(self, chunks: List[DirectiveChunk]) -> None:
        """Generate embeddings for directive chunks."""
        if not chunks:
            return
        
        # Extract content for embedding
        texts = [chunk.content for chunk in chunks]
        
        # Generate embeddings
        if TRANSFORMERS_AVAILABLE:
            embeddings = self.model.encode(texts, convert_to_numpy=True)
        else:
            # TF-IDF fallback
            embeddings = self.model.fit_transform(texts).toarray()
        
        # Store embeddings in chunks
        for i, chunk in enumerate(chunks):
            chunk.embedding = embeddings[i]
            self.chunks[chunk.id] = chunk
        
        # Update indices
        self._update_search_index()
        
        print(f"✅ Generated embeddings for {len(chunks)} chunks")
    
    def _update_search_index(self):
        """Update the search index with current embeddings."""
        if not self.chunks:
            return
        
        # Collect embeddings and IDs
        embeddings = []
        chunk_ids = []
        
        for chunk_id, chunk in self.chunks.items():
            if chunk.embedding is not None:
                embeddings.append(chunk.embedding)
                chunk_ids.append(chunk_id)
        
        if not embeddings:
            return
        
        self.embeddings_matrix = np.array(embeddings).astype('float32')
        self.chunk_ids = chunk_ids
        
        # Build FAISS index if available
        if FAISS_AVAILABLE and len(embeddings) > 0:
            self.index = faiss.IndexFlatIP(self.embedding_dim)  # Inner product for cosine similarity
            
            # Normalize embeddings for cosine similarity
            normalized_embeddings = self.embeddings_matrix / np.linalg.norm(
                self.embeddings_matrix, axis=1, keepdims=True
            )
            self.index.add(normalized_embeddings)
            
            print(f"✅ Built FAISS index with {len(embeddings)} embeddings")
    
    def retrieve_relevant_chunks(
        self, 
        context: RetrievalContext, 
        top_k: int = 5,
        min_similarity: float = 0.3
    ) -> List[Tuple[DirectiveChunk, float]]:
        """Retrieve most relevant directive chunks for given context."""
        
        if not self.chunks or self.embeddings_matrix is None:
            return []
        
        # Create composite query from context
        query_parts = [context.query]
        
        if context.user_intent:
            query_parts.append(f"Intent: {context.user_intent}")
        
        if context.current_tools:
            query_parts.append(f"Tools: {', '.join(context.current_tools)}")
        
        composite_query = " ".join(query_parts)
        
        # Generate query embedding
        if TRANSFORMERS_AVAILABLE:
            query_embedding = self.model.encode([composite_query], convert_to_numpy=True)[0]
        else:
            query_embedding = self.model.transform([composite_query]).toarray()[0]
        
        # Search for similar chunks
        if FAISS_AVAILABLE and self.index is not None:
            # Normalize query embedding
            query_embedding = query_embedding / np.linalg.norm(query_embedding)
            query_embedding = query_embedding.reshape(1, -1).astype('float32')
            
            # Search
            similarities, indices = self.index.search(query_embedding, top_k * 2)  # Get extra for filtering
            
            results = []
            for similarity, idx in zip(similarities[0], indices[0]):
                if idx < len(self.chunk_ids) and similarity >= min_similarity:
                    chunk_id = self.chunk_ids[idx]
                    chunk = self.chunks[chunk_id]
                    results.append((chunk, float(similarity)))
        else:
            # Numpy fallback
            similarities = cosine_similarity([query_embedding], self.embeddings_matrix)[0]
            
            # Get top results
            indices = np.argsort(similarities)[::-1][:top_k * 2]
            
            results = []
            for idx in indices:
                similarity = similarities[idx]
                if similarity >= min_similarity:
                    chunk_id = self.chunk_ids[idx]
                    chunk = self.chunks[chunk_id]
                    results.append((chunk, similarity))
        
        # Apply priority-based ranking
        results = self._apply_priority_ranking(results, context)
        
        # Apply token budget constraints if specified
        if context.token_budget:
            results = self._apply_token_budget(results, context.token_budget)
        
        return results[:top_k]
    
    def _apply_priority_ranking(
        self, 
        results: List[Tuple[DirectiveChunk, float]], 
        context: RetrievalContext
    ) -> List[Tuple[DirectiveChunk, float]]:
        """Apply priority-based ranking to results."""
        
        def priority_score(chunk_similarity_pair):
            chunk, similarity = chunk_similarity_pair
            
            # Base score from similarity
            score = similarity
            
            # Priority bonus (lower priority number = higher bonus)
            priority_bonus = (6 - chunk.priority) * 0.1
            score += priority_bonus
            
            # Context tag bonuses
            if context.current_tools:
                if any(tool.lower() in chunk.content.lower() for tool in context.current_tools):
                    score += 0.15
            
            # Essential section bonus
            if any(tag in ['initialization', 'execution', 'validation'] for tag in chunk.context_tags):
                score += 0.1
            
            return score
        
        return sorted(results, key=priority_score, reverse=True)
    
    def _apply_token_budget(
        self, 
        results: List[Tuple[DirectiveChunk, float]], 
        token_budget: int
    ) -> List[Tuple[DirectiveChunk, float]]:
        """Filter results to fit within token budget."""
        
        filtered_results = []
        current_tokens = 0
        
        for chunk, similarity in results:
            # Rough token estimation (1 token ≈ 4 characters)
            chunk_tokens = len(chunk.content) // 4
            
            if current_tokens + chunk_tokens <= token_budget:
                filtered_results.append((chunk, similarity))
                current_tokens += chunk_tokens
            else:
                break
        
        return filtered_results
    
    def generate_contextual_directive(self, context: RetrievalContext) -> str:
        """Generate a contextual directive using retrieved chunks."""
        
        relevant_chunks = self.retrieve_relevant_chunks(context, top_k=8)
        
        if not relevant_chunks:
            # Fallback to minimal directive
            return self._get_minimal_directive()
        
        # Organize chunks by priority and section
        core_chunks = []
        supplementary_chunks = []
        
        for chunk, similarity in relevant_chunks:
            if chunk.priority <= 2 or similarity >= 0.7:
                core_chunks.append(chunk)
            else:
                supplementary_chunks.append(chunk)
        
        # Build directive
        directive_parts = [
            "Enhanced MCP Prime Directive - Contextual",
            f"Generated: {context.query}",
            ""
        ]
        
        # Add core chunks
        if core_chunks:
            directive_parts.append("CORE DIRECTIVES:")
            for chunk in core_chunks[:5]:  # Limit core chunks
                directive_parts.append(f"- {chunk.content}")
            directive_parts.append("")
        
        # Add supplementary chunks if space allows
        if supplementary_chunks and context.token_budget:
            remaining_budget = context.token_budget - (len("\n".join(directive_parts)) // 4)
            if remaining_budget > 100:
                directive_parts.append("ADDITIONAL CONTEXT:")
                for chunk in supplementary_chunks[:3]:
                    chunk_tokens = len(chunk.content) // 4
                    if remaining_budget >= chunk_tokens:
                        directive_parts.append(f"- {chunk.content}")
                        remaining_budget -= chunk_tokens
                    else:
                        break
        
        return "\n".join(directive_parts)
    
    def _get_minimal_directive(self) -> str:
        """Return absolute minimal directive for emergency situations."""
        return """MCP Prime Directive - Minimal
- Use available MCP tools proactively
- Mark verified vs assumed claims
- Cache operations for efficiency
- Direct task focus"""
    
    def save_embeddings_cache(self):
        """Save embeddings to cache for faster loading."""
        cache_file = self.cache_dir / "directive_embeddings.pkl"
        
        cache_data = {
            'chunks': {chunk_id: asdict(chunk) for chunk_id, chunk in self.chunks.items()},
            'embeddings_matrix': self.embeddings_matrix,
            'chunk_ids': self.chunk_ids,
            'embedding_dim': self.embedding_dim
        }
        
        try:
            with open(cache_file, 'wb') as f:
                pickle.dump(cache_data, f)
            print(f"✅ Saved embeddings cache to {cache_file}")
        except Exception as e:
            print(f"⚠️  Error saving cache: {e}")
    
    def _load_cache(self):
        """Load embeddings from cache."""
        cache_file = self.cache_dir / "directive_embeddings.pkl"
        
        if not cache_file.exists():
            return
        
        try:
            with open(cache_file, 'rb') as f:
                cache_data = pickle.load(f)
            
            # Restore chunks
            for chunk_id, chunk_data in cache_data['chunks'].items():
                chunk = DirectiveChunk(**chunk_data)
                self.chunks[chunk_id] = chunk
            
            # Restore matrices and indices
            self.embeddings_matrix = cache_data.get('embeddings_matrix')
            self.chunk_ids = cache_data.get('chunk_ids', [])
            
            # Update search index
            if self.embeddings_matrix is not None:
                self._update_search_index()
            
            print(f"✅ Loaded {len(self.chunks)} chunks from cache")
            
        except Exception as e:
            print(f"⚠️  Error loading cache: {e}")

def main():
    import argparse
    
    parser = argparse.ArgumentParser(description="Dynamic Directive Embedding System")
    parser.add_argument("--directive", required=True, help="Path to directive file")
    parser.add_argument("--chunk-strategy", choices=['semantic', 'paragraph', 'sentence', 'hybrid'], 
                       default='semantic', help="Chunking strategy")
    parser.add_argument("--query", help="Test query for retrieval")
    parser.add_argument("--top-k", type=int, default=5, help="Number of chunks to retrieve")
    parser.add_argument("--cache-dir", help="Cache directory for embeddings")
    parser.add_argument("--save-cache", action="store_true", help="Save embeddings to cache")
    
    args = parser.parse_args()
    
    # Initialize embedder
    embedder = DirectiveEmbedder(args.cache_dir)
    
    # Process directive
    if Path(args.directive).exists():
        print(f"🔄 Processing directive: {args.directive}")
        
        # Chunk the directive
        chunks = embedder.chunk_directive(args.directive, args.chunk_strategy)
        print(f"📊 Created {len(chunks)} chunks using {args.chunk_strategy} strategy")
        
        # Generate embeddings
        embedder.embed_chunks(chunks)
        
        # Save cache if requested
        if args.save_cache:
            embedder.save_embeddings_cache()
        
        # Test retrieval if query provided
        if args.query:
            context = RetrievalContext(query=args.query)
            results = embedder.retrieve_relevant_chunks(context, top_k=args.top_k)
            
            print(f"\n🔍 Top {len(results)} results for query: '{args.query}'")
            for i, (chunk, similarity) in enumerate(results, 1):
                print(f"\n{i}. Similarity: {similarity:.3f} | Priority: {chunk.priority}")
                print(f"   Section: {chunk.metadata.get('section', 'unknown')}")
                print(f"   Content: {chunk.content[:100]}...")
            
            # Generate contextual directive
            contextual_directive = embedder.generate_contextual_directive(context)
            print(f"\n📝 Contextual Directive (tokens ≈ {len(contextual_directive)//4}):")
            print("=" * 50)
            print(contextual_directive)
    else:
        print(f"❌ Directive file not found: {args.directive}")

if __name__ == "__main__":
    main()