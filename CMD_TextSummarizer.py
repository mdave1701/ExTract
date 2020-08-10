#!/usr/bin/env python3
# coding: utf-8

# # Text Summarization Using Bag of Words and TextRank

# Just a lil' something to make terminal output prettier. 
print("")
print("Loading...")

# In[15]:

from sys import argv
import nltk
import bs4 as bs
import urllib.request
import re
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
import networkx as nx
import lxml

from IPython.core.interactiveshell import InteractiveShell
InteractiveShell.ast_node_interactivity = "all"


# ### Read GloVe Embeddings For TextRank

# In[16]:


# This function reads the GloVe embeddings that will be used for the TextRank model later
def read_GloVe_embeddings(path='glove.6B.100d.txt'):
    embeddings = {}
    file = open('glove.6B.100d.txt', encoding='utf-8')
    for line in file:
        values = line.split()
        word = values[0]
        coefs = np.asarray(values[1:], dtype='float32')
        embeddings[word] = coefs
    file.close()
    
    return embeddings

embeddings = read_GloVe_embeddings()


# ### Get Input and Parse the Articles

# In[17]:


# This function gets the article links and number of sentences to include in the summary from the user
def get_input(stdin):
    article_links = []
    num_sents = None
    stdin_args = stdin[1:] # for some reason the script itself counts as a stdin argument 
    # Interactive inputs are triggered if no arguments are passed in the command line.
    if len(stdin_args) == 0: 
        print("Please enter the article links you wish to summarize:")
        print("Enter -1, if you are done entering links.")
        while True:
            link = input()
            if link == "-1":
                break
            article_links.append(link)
        print("\nPlease enter the number of sentences you want in the summary:")
        num_sents = int(input())
    else: # if arguments are given they are taken as inputs instead
        for argument in stdin_args:
            if "http" in argument: # Making sure that the input is a link
                # There are probably better ways to do it, but this is a quick solution.
                article_links.append(argument)
            elif argument == "-s": # -s flag stands for 'sentences'
                n_termination = stdin_args.index(argument) 
                num_sents = int(stdin_args[n_termination + 1])
                break
            else:
                print(argument + " is not a valid link.")
                continue
        if num_sents == None: 
            print("No argument was given for number of sentences.")
            print("Defaulting to 5 sentence summaries.")
            num_sents = 5 # setting a default value
    
    return article_links, num_sents

# This function parses the raw xml text into string format
def parse_articles(articles):
    article_text_lst = []
    for article in articles:
        raw_article = urllib.request.urlopen(article).read()
        parsed_article = bs.BeautifulSoup(raw_article, 'lxml')
        paragraphs = parsed_article.find_all('p')
        article_text = ""
        for p in paragraphs:
            article_text += p.text
        article_text_lst.append(article_text)
    
    return ' '.join(article_text_lst)


# ### Preprocess the Text

# In[18]:


# This function preproccesses the text for the bag of words model
def preprocess_text_wf(corpus):
    corpus = re.sub(r'\[[0-9]*\]', ' ', corpus)     # removes any brackets with numbers in them (for citations)
    corpus = re.sub(r'\s+', ' ', corpus) # removes any extra spaces
    formatted_corpus = re.sub(r'[^a-zA-Z]', ' ', corpus)   # removes any characters that are non-alphabetic
    formatted_corpus = re.sub(r'\s+', ' ', formatted_corpus) # removes any extra spaces
    
    # tokenize the original corpus which will be used to generate the summary
    sentences_wf = nltk.sent_tokenize(corpus)        
    return formatted_corpus, sentences_wf

# This function preproccesses the text for the TextRank model
def preprocess_text_textrank(corpus):
    # get rid of citation brackets and extra spaces from the corpus
    corpus = re.sub(r'\[[0-9]*\]', ' ', corpus)
    corpus = re.sub(r'\s+', ' ', corpus)
    
    # tokenize the original corpus which will be used to generate the summary
    sentences_glove = nltk.sent_tokenize(corpus)
    formatted_sents = []
    
    # remove non-alphabetic characters for computation of similarity matrix
    for s in sentences_glove:
        formatted_sent = re.sub(r'[^a-zA-Z]', ' ', s)
        formatted_sent = re.sub(r'\s+', ' ', formatted_sent)
        formatted_sents.append(formatted_sent.lower())
        
    return sentences_glove, formatted_sents
    
# This function removes stopwords from a give sentence
def remove_stopwords(sent):
    stopWords = nltk.corpus.stopwords.words('english')
    new_sent = " ".join([word for word in sent if word not in stopWords])
    return new_sent    


# ### Bag of Words Model

# In[19]:


# This function build a normalized frequency distribution of words in the corpus
def build_freqDist(corpus):
    words = nltk.word_tokenize(corpus)
    word_freqs = nltk.FreqDist(words)
    max_freq = max(word_freqs.values())
    word_freqs_normalized = {k:v/max_freq for k,v in word_freqs.items()}
      
    return word_freqs_normalized

# This function builds a dictionary of sentence scores
def calculate_sent_scores(wordFreqs, sentence_list):
    sent_scores = {}
    
    # looping through the original sentence list to get original sentences in the summary
    for sent in sentence_list:
        for word in nltk.word_tokenize(sent.lower()):
            if word in wordFreqs.keys():
                if len(sent.split()) < 35:   # only grab sentences with less than 35 words in them
                    if sent not in sent_scores.keys():
                        sent_scores[sent] = wordFreqs[word]
                    else:
                        sent_scores[sent] += wordFreqs[word]
    
    return sent_scores

# This function ranks the sentences in descending order of sentence score and 
# returns a summary with desired number of sentences
def generate_summary_wordFreq(sentScores, numSents):
    sorted_scores = sorted(sentScores.items(), key=lambda x: x[1], reverse=True)
    sents_scored = [k for k,v in sorted_scores]
    summary = ' '.join(sents_scored[:numSents])
    return summary


# ### TextRank Model

# In[20]:


# This function vectorizes the sentences
def vectorize_sentences(clean_sents, embeddings):
    sent_vecs = []
    
    for sent in clean_sents:
        if len(sent) > 0:
            # gets the embedding values for the words in the sentence and add them
            # then normalize it by the len of the sent
            vals = sum([embeddings.get(word, np.zeros((100,)))        
                    for word in sent.split()])/(len(sent.split()))
        else:
            vals = np.zeros((100,))
        
        sent_vecs.append(vals)
        
    return sent_vecs

# This function computes the similarity matrix for the PageRank model
def compute_similarity_matrix(sent_vecs, n):
    sim_mat = np.zeros([n, n])
    for i in range(n):
        for j in range(n):
            if i != j:
                sim_mat[i][j] = cosine_similarity(sent_vecs[i].reshape(1,100), sent_vecs[j].reshape(1,100))[0,0]
    
    return sim_mat

# This function calculates the PageRank scores for the sentences
def get_Pagerank_scores(sim_mat):
    graph = nx.from_numpy_array(sim_mat)
    scores = nx.pagerank(graph)
    
    return scores

# This function ranks the sentences and generates the summary
# of the desired number of sentences
def generate_summary_GloVe(scores, sents, numSents):
    ranked_sents_scores = sorted(((scores[i], s) for i, s in enumerate(sents)), reverse=True)
    ranked_sents = [s for i, s in ranked_sents_scores if len(s.split()) < 35]   # only select sentences with <35 words
    summary = ' '.join(ranked_sents[:numSents])
    return summary


# ### Driver Code

# In[21]:


# get the links and parse the articles
links, num_sents = get_input(argv)
corpus = parse_articles(links)

# Bag of words model
formatted_corpus_wf, sentences_wf = preprocess_text_wf(corpus)                      # preprocess the text
sentences_wf_no_sw = remove_stopwords(nltk.word_tokenize(formatted_corpus_wf))      # remove stropwords
weighted_wordFreqs = build_freqDist(sentences_wf_no_sw)                             # build frequency distribution
sent_scores = calculate_sent_scores(weighted_wordFreqs, sentences_wf)               # calculate sentence scores
summary_word_freq = generate_summary_wordFreq(sent_scores, num_sents)               # generate the summary
print("\nBag of Words Model:\n")
print(summary_word_freq)

# TextRank model
orig_sents, clean_sents = preprocess_text_textrank(corpus)                          # preprocess the text 
clean_sents_no_sw = [remove_stopwords(s.split()) for s in clean_sents]              # remove stropwords
sentence_vecs = vectorize_sentences(clean_sents_no_sw, embeddings)                  # vectorize the sentencs
similarity_mat = compute_similarity_matrix(sentence_vecs, len(orig_sents))          # compute the similarity matrix
pageRank_scores = get_Pagerank_scores(similarity_mat)                               # compute the pagerank scores
summary_glove = generate_summary_GloVe(pageRank_scores, orig_sents, num_sents)      # generate the summary
print("\n\nTextRank Model:\n")
print(summary_glove)
print("")


# ## Summary
# 
# ### Purpose
# 
# Due to the increase in data and just the sheer amount of information one needs to keep up with to stay updated with the world, it is essential to summarize news articles or any long texts to save time and understand the essential aspects of the text quickly. The purpose of this project is to do precisely this. This text summarizer takes a corpus of text(s) and gives the user a concise summary in the number of sentences the user specifies.
# 
# ### Functionality
# 
# This text summarizer allows the user to enter either one or more article links and produces a combined summary of the texts for the user to read. This can be used for any text that the user enters, but it works best if the text entered is short to medium in length. If it is too long then the summary may not be reflective of the main ideas of the text. The application also gives the user two summaries generated using two different models, namely, Bag of Words and TextRank. 
# 
# The Bag of Words model generates a very consise summary, but if in the odd case that it does not generate a relevant summary, then the user has the option of looking at the summary generated using the TextRank model. Alternatively, the user can read both summaries to guage an enhanced sense of the texts.
# 
# ### Challenges Faced
# 
# I did not face many challenges, but one of the challenges I faced was that the summaries were appearing with the preprocessed sentences, i.e. without stopwords and non-alphabetic characters. It took me some time to debug and see that the corpus that I was tokenizing was the preprocessed corpus and not the corpus with the original text.
# 
# Another issue that I was facing was associating the sentences with their respective PageRank scores since the scores were stored in a dictionary with integer-based indices, but then I noticed that they correspond to the original sentences list, so I just zipped them together.

# In[ ]:




