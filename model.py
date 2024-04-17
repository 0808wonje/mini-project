# 이건 feature extraction 예제입니다

# Use a pipeline as a high-level helper
from transformers import pipeline
import numpy as np
# Define a pipeline with a task and model
# The task is "text-similarity" and the model is "snunlp/KR-SBERT-V40K-klueNLI-augSTS"
pipe = pipeline("feature-extraction", model="snunlp/KR-SBERT-V40K-klueNLI-augSTS")

# Define two sentences
sentence1 = "나는 밥을 먹었다."
sentence2 = "나는 밥을 먹었었다."

# Average the vectors of each sentence

feat1 = pipe(sentence1)
feat2 = pipe(sentence2)

avg_feat1 = np.mean(feat1, axis=1)
avg_feat2 = np.mean(feat2, axis=1)

# Calculate the cosine similarity
cosine_similarity = np.dot(avg_feat1, avg_feat2.T) / (np.linalg.norm(avg_feat1) * np.linalg.norm(avg_feat2))

# print(cosine_similarity)

def stringToVector(sentence):
    return np.mean(pipe(sentence), axis=1)

def getSimilarity(feat1, feat2):
    cosine_similarity = np.dot(feat1, feat2.T) / (np.linalg.norm(feat1) * np.linalg.norm(feat2))


# print('1111',stringToVector(sentence1))
# print('2222',stringToVector(sentence2))