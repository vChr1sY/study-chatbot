

def chunk_text(text):
    chunks = []

    for chunk in range(0, len(text), 100):
        chunks.append(text[chunk: chunk + 100])

    return chunks

def score_chunks(chunks, keywords):
    
    punctuation = ".,?!;:'\"-()"
    result = {}

    for index, chunk in enumerate(chunks):
        cleaned_chunks = []

        chunk_lower = chunk.lower()
        chunk_splitted =  chunk.split()
        score = 0

        for word in chunk_splitted:
            cleaned_word = word.strip(punctuation)
            cleaned_chunks.append(cleaned_word)
        
        for word in cleaned_chunks:
            if word in keywords:
                score += 1
        
        result[index] = score

        result_max = max(result.values())

        if result == 0:
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
        