import json
import re
from autocorrect import Speller

def write_unique_tweets(data):
    unique_tweets_id = {}
    for key, value in data.items():
        unique_tweets_id[key] = value

    unique_tweets_tweet = {}
    for key, value in unique_tweets_id.items():
        unique_tweets_tweet[value] = key

    unique_tweets_final = {}
    for key, value in unique_tweets_tweet.items():
        unique_tweets_final[value] = key
    return unique_tweets_final

# This function removes any emojis and replaces usernames  
# with a person's name ('Sophie'). If there are multiple usernames
# in a row, they will all be replaced by one name.
def remove_usernames_and_emojis(data):
    tweets = {}
    for key, value in data.items():
        no_user = " ".join(value.split())
        no_user2 = re.sub('@[a-zA-Z0-9_]*', '  ', no_user)
        no_user3 = re.sub(' {2,}', ' Sophie ', no_user2)
        no_emojis = no_user3.encode('ascii', 'ignore').decode('ascii')
        no_extra_spaces = " ".join(no_emojis.split())
        tweets[key] = re.sub('^Sophie', '', no_extra_spaces)
    return tweets

def remove_links(data):
    tweets = {}
    for key, value in data:
        replaced = re.sub('https://[a-zA-Z]*.[a-zA-Z0-9/?&.;=-]*', '  ', value)
        tweets[key] = re.sub(' {2,}', ' ', replaced)
    return tweets

def correct_spelling(data):
    spell = Speller(fast=True)
    tweets = {}
    for key, value in data:
        no_sym_emojis = re.sub(r' \:\) | \:\( | \:D | \:P | \:o | xD | \:\/ ', ' ', value)
        corrected = spell(no_sym_emojis)
        tweets[key] = " ".join(corrected.split())
    return tweets

def remove_hashtags(data):
    tweets = {}
    for key, value in data:
        no_hashtags = value
        no_hashtags = re.sub(r'(#[a-zA-Z]*[\. ]*)+\Z', '', value)
        no_hash_symbols = re.sub('#', '', no_hashtags)
        normal_spaces = " ".join(no_hash_symbols.split())
        if (normal_spaces.endswith('.') or normal_spaces.endswith('!') or normal_spaces.endswith('?')) is not True:
            normal_spaces += "."
        tweets[key] = normal_spaces
    return tweets

def main():
    with open('politics_pre.json') as json_file:
        data = json.load(json_file)
        # tweets3 = write_unique_tweets(data)
        tweets = remove_usernames_and_emojis(data)
        tweets2 = remove_links(tweets.items())
        tweets3 = correct_spelling(tweets2.items())
        tweets4 = remove_hashtags(tweets3.items())
        with open('politics.json', 'a') as f:
            json.dump(tweets4,f)

if __name__ == "__main__":
    main()