import json
import re

def write_unique_tweets(data):
    unique_tweets = {}
    for key, value in data.items():
        unique_tweets[key] = value
    return unique_tweets

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
        tweets[key] = " ".join(no_emojis.split())
    return tweets

def remove_links(data):
    tweets = {}
    for key, value in data:
        replaced = re.sub('https://t.co/[a-zA-Z0-9]*', '  ', value)
        tweets[key] = re.sub(' {2,}', ' ', replaced)
    return tweets

def main():
    with open('sports_pre.json') as json_file:
        data = json.load(json_file)
        #write_unique_tweets()
        tweets = remove_usernames_and_emojis(data)
        tweets2 = remove_links(tweets.items())
        with open('sports.json', 'a') as f:
            json.dump(tweets2,f)

if __name__ == "__main__":
    main()