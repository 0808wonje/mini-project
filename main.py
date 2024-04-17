from fastapi import FastAPI, Form
import numpy as np
from sentence_transformers import SentenceTransformer, util
from fastapi.responses import JSONResponse
import repository


# ============================================== 
# huggingface 한국어 임베딩 모델 1위
# model = SentenceTransformer("intfloat/multilingual-e5-large")

# 한국어 데이터셋 학습 후 모델 정확도 비교 1위
# model = SentenceTransformer("jhgan/ko-sroberta-multitask")

# 이외의 추천 [출처] https://www.clien.net/service/board/cm_ai/18603203
model = SentenceTransformer("bespin-global/klue-sroberta-base-continue-learning-by-mnr")



# ============================================== 
# 이외의 카카오브레인의 KorNLU 데이터셋을 활용하여 성능을 비교했을때의 순위 비교
# ============================================== 
# model	cosine_pearson	cosine_spearman	euclidean_pearson	euclidean_spearman	manhattan_pearson	manhattan_spearman	dot_pearson	dot_spearman
# ko-sroberta-multitask	84.77	85.6	83.71	84.40	83.70	84.38	82.42	82.33
# ko-sbert-multitask	84.13	84.71	82.42	82.66	82.41	82.69	80.05	79.69
# ko-sroberta-base-nli	82.83	83.85	82.87	83.29	82.88	83.28	80.34	79.69
# ko-sbert-nli	82.24	83.16	82.19	82.31	82.18	82.3	79.3	78.78
# ko-sroberta-sts	81.84	81.82	81.15	81.25	81.14	81.25	79.09	78.54
# ko-sbert-sts	81.55	81.23	79.94	79.79	79.9	79.75	76.02	75.31
# paraphrase-multilingual-mpnet-base-v2	80.69	82.00	80.33	80.39	80.48	80.61	70.30	68.48
# distiluse-base-multilingual-cased-v1	75.50	74.83	73.05	73.15	73.67	73.86	74.79	73.95
# distiluse-base-multilingual-cased-v2	75.62	74.83	73.03	72.87	73.68	73.62	63.80	62.35
# paraphrase-multilingual-MiniLM-L12-v2	73.87	74.44	72.55	71.95	72.45	71.85	55.86	55.26
# [출처] https://github.com/jhgan00/ko-sentence-transformers
# ============================================== 


app = FastAPI()

@app.post("/comparefile/")
async def create_upload_file(contents: str = Form(...)):
    datas = repository.fetch_data(repository.db)

    # sentences = datas['법령명한글'].tolist()
    sentences = []
    for e in datas:
        sentences.append(e.title)
    target_output = model.encode(sentences)

    outputs = [output.tolist() for output in target_output]

    print('--------------------------------')

    queries = [contents]

    top_k = 5
    query_embedding = model.encode(queries, convert_to_tensor=True)

    response_data = []  

    for query in queries:
        cos_scores = util.pytorch_cos_sim(query_embedding, target_output)[0]
        cos_scores = cos_scores.cpu()

        top_results = np.argpartition(-cos_scores, range(top_k))[0:top_k]
        
        query_response = {"query": query, "matches": []}
        print("\n\n======================\n\n")
        print("Query:", query)
        print("\nTop 5 most similar sentences in corpus:")
        for idx in top_results[0:top_k]:
            match_data = {
                "sentence": sentences[idx],
                "score": float(cos_scores[idx]) 
            }
            print(sentences[idx], "(Score: %.4f)" % (cos_scores[idx]), "\n")
            query_response["matches"].append(match_data)

        response_data.append(query_response)

    return JSONResponse(content={"responses": response_data})