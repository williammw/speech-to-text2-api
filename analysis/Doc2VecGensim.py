import jieba
from gensim.models.doc2vec import Doc2Vec, TaggedDocument

# Load the two articles
with open('chatGPTresult.txt', 'r', encoding='utf-8') as f:
    article1 = f.read()
with open('unknowenginer.txt', 'r', encoding='utf-8') as f:
    article2 = f.read()

# Tokenize the articles using jieba
article1_tokens = list(jieba.cut(article1))
article2_tokens = list(jieba.cut(article2))

# Convert the tokenized articles into TaggedDocument format
tagged_docs = [TaggedDocument(words=article1_tokens, tags=['article1']),
               TaggedDocument(words=article2_tokens, tags=['article2'])]

# Train the doc2vec model
model = Doc2Vec(tagged_docs, vector_size=300,
                window=10, min_count=5, workers=4)

# Infer the document vectors for the two articles
article1_vec = model.infer_vector(article1_tokens)
article2_vec = model.infer_vector(article2_tokens)

# Calculate the cosine similarity between the document vectors
cosine_sim = model.docvecs.similarity('article1', 'article2')

print("Cosine similarity between the two articles:", cosine_sim)
# Cosine similarity between the two articles: 0.48345158
