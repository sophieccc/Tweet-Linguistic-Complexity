from stanza.server import CoreNLPClient
import nltk

def main():
    # with CoreNLPClient(
    #         annotators=['tokenize','ssplit','pos','lemma','ner', 'parse', 'depparse','coref'],
    #         timeout=30000,
    #         endpoint='http://localhost:8000',
    #         memory='16G') as client:
    #         ann = client.annotate(text)
    #         sentence = ann.sentence[0]
    #         constituency_parse = sentence.parseTree
    #         print(constituency_parse)

if __name__ == "__main__":
    main()