from collections import Counter

words = {}
with open('bbc/business/101.txt') as f:
  article = f.read()
  print 'article\n', article
  print "=" * 50
  words = Counter([current_word.lower() for current_word in article.split()])
print 'words\n', words
print "=" * 50

stopping_words = []
with open('stopwords.txt') as f:
  stopping_words = f.read().split()
print 'stopping_words\n', stopping_words
print "=" * 50

# Remove stopping words
for stopping_word in stopping_words:
  words.pop(stopping_word, None)
print 'words after removing stopping words\n', words
print "=" * 50
