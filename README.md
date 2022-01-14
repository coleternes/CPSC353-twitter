# udpclient

This repository contains a twitterexample.py program and a sentiment.py program.
The sentiment.py program does the following:
1. Prompts the user to enter two search terms.
2. Searches the twitter stream for the first 1000 tweets that contains the first search term.
3. Calculates a sentiment score for the first search term
4. Searches the twitter stream for the first 1000 tweets that contains the second search term.
5. Calculates a sentiment score for the second search term.
6. Determines which search term currently has the most positive sentiment on twitter and prints the results.

## Identifying Information

* Name: Cole Ternes
* Student ID: 2323955
* Email: ternes@chapman.edu
* Course: CPSC-353
* Assignment: PA03 Sentiment Analysis

## Source Files

* AFINN-111.txt
* requirements.txt
* sentiment.py
* twitterexample.py
* sentiment.input

## References

*

## Known Errors

*

## Build Instructions

* flake8 sentiment.py

## Execution Instructions

* python sentiment.py < sentiment.input
