import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
 
 
def cosine_similarity(a: np.ndarray, b: np.ndarray) -> float:
    """Cosine similarity between two vectors. Range: -1 (opposite) to 1 (identical)."""
    norm = np.linalg.norm(a) * np.linalg.norm(b)
    if norm == 0:
        return 0.0
    return float(np.dot(a, b) / norm)
 
 
def build_embeddings(sentences: list[str]) -> np.ndarray:
    """Convert a list of sentences into TF-IDF embedding vectors."""
    vectorizer = TfidfVectorizer(stop_words="english", ngram_range=(1, 2))
    matrix = vectorizer.fit_transform(sentences) 
    return matrix.toarray()
 
 
def print_similarity_matrix(embeddings: np.ndarray, sentences: list[str]) -> None:
    n = len(sentences)
    header = f"{'':5}" + "".join(f"  S{i+1:>2}" for i in range(n))
    print(header)
    print("-" * len(header))
    for i in range(n):
        row = f"  S{i+1:<2}"
        for j in range(n):
            sim = cosine_similarity(embeddings[i], embeddings[j])
            row += f" {sim:.2f}"
        print(row + f"   {sentences[i][:55]}")
 

# DEMO 1 — Semantic similarity across topics
print("DEMO 1 — Similarity matrix across three topic groups")
 
sentences = [
    "A dog is playing in the park.",           # S1
    "A puppy is running on the grass.",         # S2
    "Machine learning models learn from data.", # S3
    "Neural networks are trained on examples.", # S4
    "I enjoy eating pizza for dinner.",         # S5
    "She loves having pasta in the evening.",   # S6
]
 
print("\nSentences:")
for i, s in enumerate(sentences):
    print(f"  S{i+1}: {s}")
 
embeddings = build_embeddings(sentences)
print("\nCosine similarity matrix:")
print_similarity_matrix(embeddings, sentences)
 
# Find top similar pairs
pairs = []
for i in range(len(sentences)):
    for j in range(i + 1, len(sentences)):
        sim = cosine_similarity(embeddings[i], embeddings[j])
        pairs.append((sim, i, j))
pairs.sort(reverse=True)
 
print("\nTop 3 most similar pairs:")
for sim, i, j in pairs[:3]:
    print(f"  {sim:.4f}  S{i+1} <-> S{j+1}")
    print(f"           \"{sentences[i]}\"")
    print(f"           \"{sentences[j]}\"")
 
 
# DEMO 2 — Semantic search over a knowledge base
print("DEMO 2 — Semantic search over a knowledge base")
 
knowledge_base = [
    "Python is a high-level programming language known for readability.",
    "FastAPI is a modern web framework for building APIs with Python.",
    "SQLAlchemy is an ORM that maps Python classes to database tables.",
    "Large language models are trained on vast amounts of text data.",
    "Embeddings represent text as numeric vectors in high-dimensional space.",
    "Cosine similarity measures the angle between two vectors.",
    "Git is a distributed version control system for tracking code changes.",
    "PostgreSQL is an open-source relational database management system.",
]
 
queries = [
    "How do I store data in a database using Python?",
    "What are word vectors used for in NLP?",
    "How do AI models understand human language?",
]
 
print("\nKnowledge base:")
for i, doc in enumerate(knowledge_base):
    print(f"  [{i}] {doc}")
 
# Fit vectorizer on the full corpus (KB + queries together)
all_texts  = knowledge_base + queries
vectorizer = TfidfVectorizer(stop_words="english", ngram_range=(1, 2))
all_vecs   = vectorizer.fit_transform(all_texts).toarray()
kb_vecs    = all_vecs[:len(knowledge_base)]
query_vecs = all_vecs[len(knowledge_base):]
 
print()
for i, query in enumerate(queries):
    q_vec  = query_vecs[i]
    scores = [(cosine_similarity(q_vec, kb_vecs[j]), j) for j in range(len(knowledge_base))]
    scores.sort(reverse=True)
    top_score, top_idx = scores[0]
    print(f"  Query : {query}")
    print(f"  Match : [{top_idx}] {knowledge_base[top_idx]}")
    print(f"  Score : {top_score:.4f}")
    print()
 
 
# DEMO 3 — Paraphrase detection
print("DEMO 3 — Paraphrase detection")
 
THRESHOLD = 0.25   # TF-IDF similarity is lower than neural embeddings
                   # In production with sentence-transformers, use 0.70+
 
pairs_to_check = [
    ("How do I learn Python?",          "What is the best way to study Python?"),
    ("How do I learn Python?",          "What is the capital of France?"),
    ("The cat sat on the mat.",         "A feline rested on a rug."),
    ("I need to fix this bug in code.", "The weather is nice today."),
    ("Doctors recommend daily exercise.","Physicians advise regular physical activity."),
]
 
print(f"\n  (Threshold for paraphrase: similarity >= {THRESHOLD})\n")
for s1, s2 in pairs_to_check:
    vecs    = TfidfVectorizer(stop_words="english").fit_transform([s1, s2]).toarray()
    sim     = cosine_similarity(vecs[0], vecs[1])
    verdict = "PARAPHRASE" if sim >= THRESHOLD else "DIFFERENT  "
    print(f"  {verdict}  sim={sim:.4f}")
    print(f"    A: {s1}")
    print(f"    B: {s2}")
    print()