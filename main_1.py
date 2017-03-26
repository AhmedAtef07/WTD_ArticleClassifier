import os
from os import path
from collections import Counter

d = [',', '.', '!', '?', '/', '\\', '&', '-', ':', ';', '@', '"', "'"]

stopping_words = []
with open('stopwords.txt') as f:
  stopping_words = f.read().split()

words = []
for article in os.listdir('bbc/business'):
    article_path = path.join('bbc/business', article)
    with open(article_path) as f:
      curr_words = f.read().split()
      words.extend([''.join(c for c in cw.lower() if c not in d) for cw in curr_words])
words = Counter(words)

words.pop('', None) # Remove empty tokens, generated after removing delimiters
# Remove stopping words
for stopping_word in stopping_words:
  words.pop(stopping_word, None)

print 'words\n', words