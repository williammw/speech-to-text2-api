from nltk import ngrams


def jaccard_similarity(a, b):
    a_words = set(ngrams(a.split(), 1))
    b_words = set(ngrams(b.split(), 1))

    intersection = len(a_words & b_words)
    union = len(a_words | b_words)

    similarity = intersection / union

    return similarity


with open('chatGPTresult.txt', 'r') as f:
    a = f.read()

with open('unknowenginer.txt', 'r') as f:
    b = f.read()

similarity = jaccard_similarity(a, b)
print(similarity)


'''
Jaccard similarity coefficient 
of 0.0007552870090634441 suggests that the two input strings 
have very little in common, and are therefore quite dissimilar.
'''
