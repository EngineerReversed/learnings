# Quora Question pairs
This repository contains code snippet for detecting duplicate pairs of Questions in given dataset.

## Problem statement
Many people on Quora ask questions with same intent in different wordings. For better user experience on quora, these questions should be merged together so that writers do not need to answer same question multiple times. Also it will make discovery of content easier on quora. Your task is to create a deep learning model to identify duplicate questions.

## Dataset
You can download dataset from this
[link](https://s3-us-west-2.amazonaws.com/nanonets/datasets/quora-task/train.csv) <br>
For GoogleWord2Vec : [link](https://drive.google.com/file/d/0B7XkCwpI5KDYNlNUTTlSS21pQmM/edit) <br>


## Code snipppets:
**train.py** : It contains code snippet for training the GoogleWord2Vec + LSTM model + MLP in keras with backend as tensorflow. It trains the model on the Quora question pairs dataset.

**test.py**: It contains code snippet for testing whether a pair of questions are semantically same or not (Threshold = 0.5). It asks the user to enter two pair of sentences and gives the output

**embedding.py**: It contains code snippet for converting GoogleWord2Vec bin file to numpy file for faster loading using mmap.


## Implementation
For implementation, following steps should be followed:
1. Download Quora question pairs dataset and Google word2vec neural word embeddings and place them inside data folder.
2. Run the embedding.py file and it will downsize word2vec model for faster loading during inference.
3. Run the train.py file and it will start training the network. The best network will be saved based on validation accuracy.
4. Run the test.py file and give two questions as input. The model will give prediction whether they are duplicate or not (Yes/No).

### Model
We used Google Word2vec neural network embedding as input followed by LSTMs and multi-layer perceptrons stacked on top of it.

### Data pre-processing:
Several data augmentation techniques were applied on input data
- Removing stop words in English
- Removing special characters and short representations of words
- Tokenizing sentences into words
- Question pairs are swapped there by making sure there are no issues with symmetry
- Forming embedding matrix of tokenized data to be fed into neural network

### Data bias:
There were 37% positives or duplicates and 63% negatives or non-duplicates. Some questions were of single word and some questions were of length more than 30 words (about some kind of love affair question!).  After searching the internet, we also found that there were missing nouns in word2vec embedding which were also hampering the process of learning features from our Quora dataset.

### Word embeddings:
There are three types of neural word embeddings: Word2Vec, Doc2Vec and Glove embeddings. We went ahead with Word2Vec

_Word2Vec_: The purpose and usefulness of Word2vec is to group the vectors of similar words together in vectorspace. That is, it detects similarities mathematically. Word2vec creates vectors that are distributed numerical representations of word features, features such as the context of individual words. It does so without human intervention. It uses cosine similarity for similarity measure. It's amusing feature of equations to produce results is what intersted us and we decided to go ahead with it since it preserves semantic similarities.

Reason for changing word2vec vectors of Google to numpy array: we saw in the documentation that 'init_sims' can save a lot of memory. So, it will save a lot of time.
A faster way is to use gensim's save/load functionality. It uses a binary format and supports memory-mapping the large arrays into virtual memory directly, so loading should be pretty much instant.

### Techniques tried:
_Stacking LSTMs_: I tried stacking LSTM layers on top of each other but it did not result in high accuracy on validation dataset. The training data is less and one layer LSTM can easily overfit the data. Since, stacking LSTM layers results in learning different types of features at holistic level, it wasn't required here. The sentences were short and question oriented. If it was a long story, then stacking LSTMs could have been beneficial.

_Optimizers_: Different optimizers like Adam, Nadam, RMSprop were tried and we achieved faster convergence through Nadam(Nesterov Adam optimizer). Much like Adam is essentially RMSprop with momentum, Nadam is Adam RMSprop with Nesterov momentum.

_Loss_: Since, it was a classification problem, binary cross entropy function was used.

_Batch normalization_: It improved generalization accuracy on validation dataset.


## Future works
What else can be done? 
- Glove vectors can be tried as neural word embeddings instead of Word2Vec embeddings.
- Other architectures like 1-D convolution, GRU, BiLSTMs etc. can be tried and they can be further ensembled to give higher accuracy.
- Since the datset was biased, we can give weightage to duplicate class in loss function and achieve better performance.
- ROC-AUC curve can be drawn to determine a good value of threshold.
