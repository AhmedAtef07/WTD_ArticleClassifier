import os
from os import path
from collections import Counter

data_path = 'bbc_train'
data_words = {}

d = [',', '.', '!', '?', '/', '&', '-', ':', ';', '@', '"', "'", '...']
stopping_words = []
with open('stopwords.txt') as f:
  stopping_words = f.read().split()

for article_type in os.listdir(data_path):
  # For each type, within a single type
  article_type_dir_path = path.join(data_path, article_type)
  article_words = []
  for article in os.listdir(article_type_dir_path):
    # For each article in that type, within a single file
    article_path = path.join(article_type_dir_path, article)
    with open(article_path) as f:
      curr_words = f.read().split()
      article_words.extend([''.join(c for c in cw.lower() if c not in d) for cw in curr_words])
  article_counter = Counter(article_words)
  # Remove unwanted counted keys.
  article_counter.pop('', None) # Remove empty tokens, generated after removing delimiters
  for stopping_word in stopping_words: # Remove stopping words
    article_counter.pop(stopping_word, None)
  # Save this counter with in the dict with the type as the key
  data_words[article_type] = article_counter.most_common(70)
  print article_type, '\n', data_words[article_type]
  print "=" * 50
