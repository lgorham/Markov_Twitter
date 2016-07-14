import os
import sys
from random import choice
import twitter
import re


def open_and_read_file(file_path1, file_path2):
    """Takes file path as string; returns text as string.

    Takes a string that is a file path, opens the file, and turns
    the file's contents as one string of text.
    """

    corpus_file1 = open(file_path1, 'r')
    corpus_data1 = corpus_file1.read()

    corpus_file2 = open(file_path2, 'r')
    corpus_data2 = corpus_file2.read()

    combined_text = corpus_data1 + corpus_data2

    return combined_text



def make_chains(text_string, n):
    """Takes input text as string; returns _dictionary_ of markov chains.

    A chain will be a key that consists of a tuple of (word1, word2)
    and the value would be a list of the word(s) that follow those two
    words in the input text.

    For example:

        >>> make_chains("hi there mary hi there juanita")
        {('hi', 'there'): ['mary', 'juanita'], ('there', 'mary'): ['hi'], ('mary', 'hi': ['there']}
    """

    chains = {}

    no_digits = re.sub(r'\n+\d+\.', ' ', text_string)
    no_excess_spaces = re.sub(r'\s+', ' ', no_digits)
    split_text = no_excess_spaces.replace('\n',' ').rstrip().split(' ')

    for i in range(len(split_text)-n):
        # chains[(split_text[i], split_text[i+1])] = chains.get((split_text[i], split_text[i+1]), [])
        # chains[(split_text[i], split_text[i+1])].append(split_text[i+2])
        current_key_iteration = []
        index_pos = i
        while len(current_key_iteration) < n:
            current_key_iteration.append(split_text[index_pos])
            index_pos += 1
        final_key = tuple(current_key_iteration)

        # word_pair = (split_text[i], split_text[i+1])
        following_word = split_text[i+n]
        # print "Final Key: ", final_key, "Next Word: ", following_word
        if final_key in chains: 
            chains[final_key].append(following_word)
        else: 
            chains[final_key] = [following_word]

    # for key, value in chains.items():
    #      print key, value 

    return chains

# file_path = open_and_read_file('green-eggs.txt')
# print make_chains(file_path, 5)

def make_text(chains, n):
    """Takes dictionary of markov chains; returns random text.""" 

    cap_keys = []
    for tup_key in chains.keys():
        if tup_key[0][0].isupper():
            cap_keys.append(tup_key)

    current_key = choice(cap_keys)

    text = ""
    for i in range(0, n):
        text += current_key[i] + " " 

    # while current_key in chains.keys():
    while len(text) < 120:
        next_word = choice(chains[current_key])
        text += " " + next_word
        adjusting_key = list(current_key)
        adjusting_key.append(next_word)
        current_key = tuple(adjusting_key[1:])


    truncated_text = re.sub(r"""[.!?;][\sa-zA-Z_"]+$"""," ", text)

    if len(truncated_text) < 140:
        return truncated_text
    else:
        return truncated_text[:-1]


def tweet(chains):
    # Use Python os.environ to get at environmental variables
    # Note: you must run `source secrets.sh` before running this file
    # to make sure these environmental variables are set.
    api = twitter.Api(
        consumer_key = os.environ['TWITTER_CONSUMER_KEY'],
        consumer_secret = os.environ['TWITTER_CONSUMER_SECRET'],
        access_token_key = os.environ['TWITTER_ACCESS_TOKEN_KEY'],
        access_token_secret = os.environ['TWITTER_ACCESS_TOKEN_SECRET'])

    api.VerifyCredentials()

    status = api.PostUpdate(chains)
    print status

# Get the filenames from the user through a command line prompt, ex:
# python markov.py green-eggs.txt shakespeare.txt
first_text = sys.argv[1]

second_text = sys.argv[2]

n_gram = int(sys.argv[3])

# Open the file and turn it into one long string
input_text = open_and_read_file(first_text, second_text)

# Get a Markov chain
chains = make_chains(input_text, n_gram)

# Produce random text
random_text = make_text(chains, n_gram)

generated_tweet = tweet(random_text)



# Your task is to write a new function tweet, that will take chains as input
# tweet(chains)
