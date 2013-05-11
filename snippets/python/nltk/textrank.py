#!/usr/local/bin/python2.7

from nltk.tokenize.punkt import PunktSentenceTokenizer

document = """To Sherlock Holmes she is always the woman. I have
seldom heard him mention her under any other name. In his eyes she
eclipses and predominates the whole of her sex. It was not that he
felt any emotion akin to love for Irene Adler. All emotions, and that
one particularly, were abhorrent to his cold, precise but admirably
balanced mind. He was, I take it, the most perfect reasoning and
observing machine that the world has seen, but as a lover he would
have placed himself in a false position. He never spoke of the softer
passions, save with a gibe and a sneer. They were admirable things for
the observer-excellent for drawing the veil from men's motives and
actions. But for the trained reasoner to admit such intrusions into
his own delicate and finely adjusted temperament was to introduce a
distracting factor which might throw a doubt upon all his mental
results. Grit in a sensitive instrument, or a crack in one of his own
high-power lenses, would not be more disturbing than a strong emotion
in a nature such as his. And yet there was but one woman to him, and
that woman was the late Irene Adler, of dubious and questionable
memory.
"""

# Sentence Split
document = ' '.join(document.strip().split('\n'))

def textrank(document):
    pst = PunktSentenceTokenizer()
    sentences = pst.tokenize(document)

    # Bag of Words
    from sklearn.feature_extraction.text import CountVectorizer
    cv = CountVectorizer()
    bow_matrix = cv.fit_transform(sentences)

    from sklearn.feature_extraction.text import TfidfTransformer
    normalized_matrix = TfidfTransformer().fit_transform(bow_matrix)

    ## mirrored matrix where the rows and columns correspond to 
    ## sentences, and the elements describe how similar the
    ## sentences are. score 1 means sentences are exactly the same.
    similarity_graph = normalized_matrix * normalized_matrix.T
    similarity_graph.toarray()

    # PageRank
    import networkx as nx
    nx_graph = nx.from_scipy_sparse_matrix(similarity_graph)

    ## mapping of sentence indices to scores. use them to associate
    ## back to the original sentences and sort them
    scores = nx.pagerank(nx_graph)
    ranked = sorted(((scores[i], s) for i,s in enumerate(sentences)), reverse=True)
    print ranked[0][1]

textrank(document)
