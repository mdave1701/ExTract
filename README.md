# ExTract

## Description

ExTract is an extractive text summarization project that utilizes relatively simple Natural Language Processing (NLP) algorithms (Bag of Words and TextRank) to give the user a summary of web based articles of thier choice.

Instead of giving a summary of a standard length, ExTract gives the user the choice to choose how long they want the summary to be (in number of sentences). <br>**[Assumption: The user has a rough idea of how long the article is in number of sentences.]**

## Algorithms Used
1. **Bag of Words (BoW)**: This algorithm is based on the simple concept of word frequencies. It does not understand context (arrangement of words and, therefore, their meanings). Essentially, it tokenizes the text by word and makes a frequency distribution. Individual sentences are then given scores based on the number of highly-frequent words they contain. The summary is created by concatenating _n_ (as entered by the user) of the highest ranked sentences. 

2. **TextRank**: The TextRank algorithm is a bit different than the BoW model, in that it loosely takes into account the ordering of the words (thus giving it a somewhat better approach to take into account context). It uses GloVe word embeddings, a vectorization of words, that groups together "related" words. It uses cosine-similarity to determine the "distance" between a set of words. It applies this step to the whole corpus and generates a similarity matrix gruped by sentences. The summary is created by concatenating _n_ sentences with the highest similarity scores. 

## Usage
Please refer to the "HOW_TO_RUN.md" file for instructions on how to use this program.

## Scope for Further Improvement
Currently, I am trying to improve the quality of the summaries by implementing abstractive text summarization techniques like GPT-2 and/or BERT. I am also trying to convert the jupyter notebook file to a command-line app, so that the users get some sort of UI and don't have to start jupyter notebook every time. 

A more long term goal for this project is to be able to handle texts in PDF format, in addition to web-based articles. This is especially useful for academics and researchers, who need to understand the gist of an article quickly to decide whether it will be useful in their research.

I am always open to collaboration. If you would like to contribute to this project, then please email me at malavdave@lewisu.edu :blush:. 
