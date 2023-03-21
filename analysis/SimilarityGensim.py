import jieba
from gensim import corpora, models, similarities

# Load the two articles
with open('chatGPTresult.txt', 'r', encoding='utf-8') as f:
    article1 = f.read()
with open('unknowenginer.txt', 'r', encoding='utf-8') as f:
    article2 = f.read()

# Tokenize the articles using jieba
article1_tokens = list(jieba.cut(article1))
article2_tokens = list(jieba.cut(article2))

# Create dictionary and corpus using gensim
dictionary = corpora.Dictionary([article1_tokens, article2_tokens])
corpus = [dictionary.doc2bow(text)
          for text in [article1_tokens, article2_tokens]]

# Train TF-IDF model
tfidf = models.TfidfModel(corpus)

# Apply TF-IDF transformation to corpus
corpus_tfidf = tfidf[corpus]

# Create similarity index using cosine similarity
index = similarities.MatrixSimilarity(corpus_tfidf)

# Get similarity score between article1 and article2
similarity_score = index[corpus_tfidf[0]][1]

print(similarity_score)
# Loading model cost 0.501 seconds.
# Prefix dict has been built successfully.
# 0.0
# The result of 0.0 from the gensim similarities code means that the two texts being compared have no
# similarity based on the Jaccard similarity coefficient. This could be due to several reasons such as
#  the texts being completely different or containing very different sets of words.
# It's also possible that the Jaccard similarity metric is not the most appropriate metric
# for these particular texts.
