#!/usr/bin/python python3

from pdfminer import high_level

# Input: string with path to pdf
# Purpose: extract text > split by periods > strip tabs and newlines
# Output: presumably a list of sentences, but a lot are probably not

def pdf2sentences(pdf): 
    article_text = high_level.extract_text(pdf)
    sentences = article_text.split('.')
    sentences_strip = [sentence.strip().replace('\n', ' ') for sentence in sentences]
    return sentences_strip

# As far as filtering out sentences from non-sentences, I have an idea that I've yet to try implementing.
#
# We can look at a set of predictors such as:
#   1. number of spaces
#   2. number of commas 
#   3. length of sentence (as in number of characters in each list entry)
#   4. average length of each word (split sentence by space, strip punctuation)
#
# My hunch is that when those factors are all considered, we should be able to predict whether a list entry
# is a body sentence or not. Question is, what do we use to make these predictions? Multiple regression?
# I will look into it more, but feel free to share ideas if something pops to mind!

sents = pdf2sentences('C:\Users\malav\Desktop\spatial-transformer-networks.pdf')
print(sents)