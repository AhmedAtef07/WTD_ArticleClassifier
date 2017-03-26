import os
from os import path
from collections import Counter

####### CONSTANTS #######

DATA_PATH = 'bbc_test'
DELIMITERS = [',', '.', '!', '?', '/', '&', '-', ':', ';', '@', '"', "'", '...']
STOPPING_WORDS = open('stopwords.txt').read().split()


####### GLOBAL VARIABLES #######

data_words = {}


####### FUNCTIONS #######

def read_train_data(data_path):
  for article_type in os.listdir(data_path):
    # For each type, within a single type
    article_type_dir_path = path.join(data_path, article_type)
    article_type_words = []
    for article in os.listdir(article_type_dir_path):
      # For each article in that type, within a single file
      article_path = path.join(article_type_dir_path, article)
      article_string = open(article_path).read()
      article_type_words.extend(listify_article(article_string))
    data_words[article_type] = get_most_common_words(article_type_words, 70)
    print article_type, '\n', data_words[article_type]
    print "=" * 50


def listify_article(whole_article):
  words = whole_article.split()
  return ([''.join(c for c in cw.lower() if c not in DELIMITERS) for cw in words])


# This function removes unwanted words and return counter with max k keys
def get_most_common_words(words, most_common_k):
  article_counter = Counter(words)
  # Remove unwanted counted keys.
  article_counter.pop('', None) # Remove empty tokens, generated after removing delimiters
  for stopping_word in STOPPING_WORDS: # Remove stopping words
    article_counter.pop(stopping_word, None)
  # Save this counter with in the dict with the type as the key
  return article_counter.most_common(70)


####### MAIN #######

if __name__ == '__main__':
  read_train_data(DATA_PATH)