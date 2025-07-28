from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

def compute_similarity_matrix(query_vec, section_vecs):
    return cosine_similarity([query_vec], section_vecs)[0]