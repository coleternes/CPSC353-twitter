# sentiment.py
# 1. Prompts the user to enter two search terms.
# 2. Searches the twitter stream for the first 1000 tweets that contains the
#    first search term.
# 3. Calculates a sentiment score for the first search term
# 4. Searches the twitter stream for the first 1000 tweets that contains the
#    second search term.
# 5. Calculates a sentiment score for the second search term.
# 6. Determines which search term currently has the most positive sentiment on
#    twitter and prints the results.

# Author: Cole Ternes
# Email: ternes@chapman.edu
# Course: CPSC 353
# Assignment: PA03 Sentiment Analysis
# Version 1.0
# Date: March 5, 2021

import twitter
import sys
import codecs

# -----------------------------------------------------------------------------
# Establish a connection to the Twitter API
sys.stdout = codecs.getwriter("utf-8")(sys.stdout.detach())

CONSUMER_KEY = 'eijX5tFznH7wsNbU1VOa1Z1L5'
CONSUMER_SECRET = 'SWzZJnu1ELj5B3f9ZdogYFRv7XIfjZ55jSKivhocQbdW9sZVPe'
ACCESS_TOKEN = '718597967481933824-3KuEl4rY0TCo5zSNUbnDWZs49EdXHvZ'
ACCESS_TOKEN_SECRET = 'qqXsiJL2sfonGvZEBeua1Fii0emLLcAF8uUWnHSNnbhsO'


auth = twitter.oauth.OAuth(ACCESS_TOKEN, ACCESS_TOKEN_SECRET,
                           CONSUMER_KEY, CONSUMER_SECRET)

twitter_api = twitter.Twitter(auth=auth)

# -----------------------------------------------------------------------------
# Enter the search terms that will be analyzed for sentiment
count = 1000
f_user_input = input('Enter the first search term: ')
s_user_input = input('Enter the second search term: ')

# -----------------------------------------------------------------------------
# Collect the last 1000 tweets that include f_user_input
f_search_results = twitter_api.search.tweets(q=f_user_input, count=count)
f_statuses = f_search_results['statuses']

# Iterate through 5 more batches of results by following the cursor
for _ in range(5):
    try:
        f_next_results = f_search_results['search_metadata']['next_results']
    # except KeyError, e:  # No more results when f_next_results doesn't exist
    except KeyError:
        break
    # Create a dictionary from f_next_results, which has the following form:
    # ?max_id=313519052523986943&q=NCAA&include_entities=1
    f_kwargs = dict([f_kv.split('=')
                    for f_kv in f_next_results[1:].split("&")])
    f_search_results = twitter_api.search.tweets(**f_kwargs)
    f_statuses += f_search_results['statuses']

f_status_texts = [f_status['text']
                  for f_status in f_statuses]

# Compute a collection of all words from all tweets
f_words = [f_w
           for f_t in f_status_texts
           for f_w in f_t.split()]

# -----------------------------------------------------------------------------
# Collect the last 1000 tweets that include s_user_input
s_search_results = twitter_api.search.tweets(q=s_user_input, count=count)
s_statuses = s_search_results['statuses']

# Iterate through 5 more batches of results by following the cursor
for _ in range(5):
    try:
        s_next_results = s_search_results['search_metadata']['next_results']
    # except KeyError, e:  # No more results when s_next_results doesn't exist
    except KeyError:
        break
    # Create a dictionary from s_next_results, which has the following form:
    # ?max_id=313519052523986943&q=NCAA&include_entities=1
    s_kwargs = dict([s_kv.split('=')
                    for s_kv in s_next_results[1:].split("&")])
    s_search_results = twitter_api.search.tweets(**s_kwargs)
    s_statuses += s_search_results['statuses']

s_status_texts = [s_status['text']
                  for s_status in s_statuses]

# Compute a collection of all words from all tweets
s_words = [s_w
           for s_t in s_status_texts
           for s_w in s_t.split()]

# -----------------------------------------------------------------------------
# Calculate the sentiment values from each collection of 1000 tweets
sent_file = open('AFINN-111.txt')

scores = {}  # initialize an empty dictionary
for line in sent_file:
    term, score = line.split("\t")
    # The file is tab-delimited.
    # "\t" means "tab character"
    scores[term] = int(score)  # Convert the score to an integer.

# Calculates the score for the first user input
f_score = 0
for f_word in f_words:
    f_uword = f_word.encode('utf-8')
    if f_word in scores.keys():
        f_score = f_score + scores[f_word]

# Calculates the score for the second user input
s_score = 0
for s_word in s_words:
    s_uword = s_word.encode('utf-8')
    if s_word in scores.keys():
        s_score = s_score + scores[s_word]

print()
if f_score > s_score:
    print(f_user_input + " has more positive sentiment on Twitter.")
elif f_score < s_score:
    print(s_user_input + " has more positive sentiment on Twitter.")
else:
    print(f_user_input + " and " + s_user_input +
          " have equal sentiment on Twitter.")

print(f_user_input + " = " + str(f_score))
print(s_user_input + " = " + str(s_score))
