from gensim.models import KeyedVectors

# This commented code snippet is for converting word2vec bin file to npy file
# This makes loading of word2vec file faster

model = KeyedVectors.load_word2vec_format('data/GoogleNews-vectors-negative300.bin',binary=True)
model.init_sims(replace=True)
model.save('data/word_vectors')

