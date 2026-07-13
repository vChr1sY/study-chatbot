from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

def chunk_text(text):
    chunks = []

    for chunk in range(0, len(text), 100):
        chunks.append(text[chunk: chunk + 100])

    return chunks

def score_chunks(chunks, question):
    
    model = SentenceTransformer("all-MiniLM-L6-v2")

    result = {}
    
    emb1 = model.encode(question)

    for index, chunk in enumerate(chunks):

        emb2 = model.encode(chunk)

        score = cosine_similarity([emb1], [emb2])[0][0]

        result[index] = score


    result_value = max(result.values())

    if result_value == 0.3:
        return None

    sorted_results = list(sorted(result.items(), key=lambda x: x[1], reverse=True))

    best_indexs = (sorted_results[:3])

    best_index = []

    for index in best_indexs:
        best_index.append(index[0])
            
    best_chunks = []

    for index in best_index:
        best_chunks.append(chunks[index])

    joined = " ".join(best_chunks)

    return joined
        