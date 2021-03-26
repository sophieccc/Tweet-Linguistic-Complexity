import requests
import os
import json

# To set your enviornment variables in your terminal run the following line:
# export 'BEARER_TOKEN'='<your_bearer_token>'

# Needed to use the API.
def auth():
    return os.environ.get("BEARER_TOKEN")

# This decides what tweets we are retrieving.
def create_url(token, query):
    max_results = "max_results=10"
    tweet_fields = "tweet.fields=author_id"
    next_token = ""
    if token != None:
        next_token = "&next_token=" + token
    url = "https://api.twitter.com/2/tweets/search/recent?query={}&{}&{}&{}".format(
        query, tweet_fields, max_results, next_token
    )
    return url


def create_headers(bearer_token):
    headers = {"Authorization": "Bearer {}".format(bearer_token)}
    return headers

# Retrieves the tweets and metadata.ß
def connect_to_endpoint(url, headers):
    response = requests.request("GET", url, headers=headers)
    if response.status_code != 200:
        raise Exception(response.status_code, response.text)
    return response.json()


def main():
    tweets = []
    bearer_token = auth()
    headers = create_headers(bearer_token)
    valid_token = True
    token = None
    index = 0
    # Will have to do 'contexts' in terms of Entity annotations, 
    # or just in terms of entities in general.
    queries = ["entity:Donald Trump lang:en -is:retweet"]
    for query in queries:
        # When actually retrieving data, remove index and set max_results = 100.
        while valid_token and index < 2:
            url = create_url(token, query)
            json_response = connect_to_endpoint(url, headers)
            data = json_response["data"]
            meta = json_response["meta"]
            if "next_token" in meta:
                token = meta["next_token"]
            else:
                valid_token = False
            for tweet in data:
                tweets.append(tweet)
            index +=1
        with open('tweets.json', 'a') as f:
            json.dump(tweets,f)



if __name__ == "__main__":
    main()