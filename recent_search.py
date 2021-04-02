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
    max_results = "max_results=100"
    tweet_fields = "tweet.fields=author_id,id,text"
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
        # raise Exception(response.status_code, response.text)
        return None
    return response.json()

def get_queries():
    file1 = open('sports.txt', 'r')
    Lines = file1.readlines()
    queries = []
    for line in Lines:
        queries.append("entity:" + line.strip() +  " lang:en -is:retweet")
    return queries

def main():
    bearer_token = auth()
    headers = create_headers(bearer_token)
    queries = get_queries()
    for query in queries:
        tweets = []
        valid_token = True
        token = None
        count = 0
        while valid_token and count < 1500:
            url = create_url(token, query)
            json_response = connect_to_endpoint(url, headers)
            if json_response !=None:
                data = json_response.get("data")
                meta = json_response.get("meta")
                if data:
                    for tweet in data:
                        tweets.append(tweet)
                    if "next_token" in meta:
                        token = meta["next_token"]
                    else:
                        valid_token = False
                    count +=100
                else:
                    valid_token = False
                    print(query)
            else:
                valid_token = False
                print(query)
        if tweets:
            with open('tweets.json', 'a') as f:
                json.dump(tweets,f)



if __name__ == "__main__":
    main()