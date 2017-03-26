import os
from os import path
from collections import Counter

####### CONSTANTS #######

DATA_TRAIN_PATH = 'bbc_train'
DATA_TEST_PATH = 'bbc_test'
DELIMITERS = [',', '.', '!', '?', '/', '&', '-', ':', ';', '@', '"', "'"]
STOPPING_WORDS = open('stopwords.txt').read().split()


####### GLOBAL VARIABLES #######

types_words_freq = {}


####### FUNCTIONS #######

def read_train_data(data_path):
  data_words = {}
  for article_type in os.listdir(data_path):
    # For each type, within a single type
    article_type_dir_path = path.join(data_path, article_type)
    article_type_words = []
    for article in os.listdir(article_type_dir_path):
      # For each article in that type, within a single file
      article_path = path.join(article_type_dir_path, article)
      article_string = open(article_path).read()
      article_type_words.extend(listify_article(article_string))
    words_freq = count_words_freq(article_type_words, 70)
    types_words_freq[article_type] = words_freq
    # print article_type, '\n', types_words_freq[article_type]
    # print "=" * 50


def run_test_data(data_path):
  for article_type in os.listdir(data_path):
    print article_type,
  print 'correct prediected'

  all_total_iterations = 0
  all_correct_predications = 0

  for article_type in os.listdir(data_path):
    # For each type, within a single type
    article_type_dir_path = path.join(data_path, article_type)

    total_iterations = 0
    correct_predications = 0

    for article in os.listdir(article_type_dir_path):
      # For each article in that type, within a single file
      article_path = path.join(article_type_dir_path, article)
      article_string = open(article_path).read()
      article_words = listify_article(article_string)
      article_wrods_freq = count_words_freq(article_words, 20)

      # For each word in the article_wrods_freq we check with all the types
      is_matched = find_best_match(article_type, article_wrods_freq)

      total_iterations += 1
      if is_matched:
        correct_predications += 1

    print '=' * 25
    print 'article_type', article_type
    print 'total_iterations', total_iterations
    print 'correct_predications', correct_predications
    print 'accuracy', correct_predications / float(total_iterations)
    print '=' * 50

    all_total_iterations += total_iterations
    all_correct_predications += correct_predications


  print ''
  print 'total_iterations', all_total_iterations
  print 'correct_predications', all_correct_predications
  print 'accuracy', all_correct_predications / float(all_total_iterations)


def find_best_match(test_article_type, test_article_freq):
  # print 'test_article_type:', test_article_type
  best_prob = -1
  best_type = ''
  for article_type, article_type_hash in types_words_freq.iteritems():
    # print article_type_hash
    words_freq = article_type_hash['words_freq']
    total_freq = article_type_hash['total_freq']

    prob = 1

    for word, freq in test_article_freq['words_freq'].iteritems():
      if word in words_freq.keys():
        # print words_freq
        # print "$" * 80
        prob *= words_freq[word]
      else:
        prob *= 1 / total_freq

    if prob > best_prob:
      best_prob = prob
      best_type = article_type
    print "%0.ef%%" % prob,
    # print "$" * 80
  print test_article_type, best_type
  return test_article_type == best_type


def listify_article(whole_article):
  words = whole_article.split()
  return ([''.join(c for c in cw.lower() if c not in DELIMITERS) for cw in words])


# This function removes unwanted words and return type_data
def count_words_freq(words, most_common_k):
  article_counter = Counter(words)

  # Remove unwanted counted keys
  article_counter.pop('', None) # Remove empty tokens, generated after removing delimiters
  for stopping_word in STOPPING_WORDS: # Remove stopping words
    article_counter.pop(stopping_word, None)

  # Calculate freq
  freq_sum = float(sum(article_counter.values()))
  freq_len = float(len(article_counter.values()))
  total_freq = freq_sum + freq_len # To avoid 0 prob problem

  article_counter = article_counter.most_common(most_common_k)

  words_freq = {}
  for word, freq in article_counter:
    words_freq[word] = (freq + 1) / total_freq

  type_data = {
    'words_freq': words_freq,
    'total_freq': total_freq
  }
  return type_data


####### MAIN #######

if __name__ == '__main__':
  read_train_data(DATA_TRAIN_PATH)
  run_test_data(DATA_TEST_PATH)
  # print types_words_freq