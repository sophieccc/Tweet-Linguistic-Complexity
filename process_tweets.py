import json
import re

def write_unique_tweets():
    unique_tweets = {}
    with open('sports_pre.json') as json_file:
        data = json.load(json_file)
        for key, value in data.items():
            unique_tweets[key] = value

    with open('sports.json', 'a') as f:
        json.dump(unique_tweets,f)

# This function removes any emojis and replaces usernames  
# with a person's name ('Sophie'). If there are multiple usernames
# in a row, they will all be replaced by one name.
def remove_usernames_and_emojis():
    tweets = {}
    with open('politics_pre.json') as json_file:
        data = json.load(json_file)
        for key, value in data.items():
            no_user = " ".join(value.split())
            no_user2 = re.sub('@[a-zA-Z0-9_]*', '  ', no_user)
            no_user3 = re.sub(' {2,}', ' Sophie ', no_user2)
            no_emojis = no_user3.encode('ascii', 'ignore').decode('ascii')
            tweets[key] = " ".join(no_emojis.split())

    with open('politics.json', 'a') as f:
        json.dump(tweets,f)

def main():
    #write_unique_tweets()
    remove_usernames_and_emojis()

if __name__ == "__main__":
    main()