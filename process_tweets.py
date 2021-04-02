import json

def main():
    unique_tweets = {}
    with open('politics.json') as json_file:
        data = json.load(json_file)
        for key, value in data.items():
            unique_tweets[key] = value

    with open('politics_final.json', 'a') as f:
        json.dump(unique_tweets,f)
if __name__ == "__main__":
    main()