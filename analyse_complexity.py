import json
from nltk import tokenize
import textstat
from nltk.parse import CoreNLPParser, CoreNLPDependencyParser

def combine_tweets(data):
    file = open("pls.txt","w")
    for _, value in data.items():
        file.write(value + " ")

def get_lexicon_stats(data):
        uniques = set()
        word_count = 0
        word_sum,sentence_sum = 0, 0
        syllable_sum, letter_count, polysyllab_count, character_sum  = 0, 0, 0, 0
        num_tweets = len(data.items())
        for _, value in data.items():
            syllable_sum += textstat.textstat.syllable_count(value)
            word_sum += textstat.textstat.lexicon_count(value)
            sentence_sum += textstat.textstat.sentence_count(value)
            character_sum += textstat.textstat.char_count(value)
            letter_count += textstat.textstat.avg_letter_per_word(value)
            polysyllab_count += textstat.textstat.polysyllabcount(value)
            tokens = tokenize.word_tokenize(value)
            for token in tokens:
                word_count +=1
                uniques.add(token)  
        print("Number of tweets: {}".format(num_tweets))
        print("Syllables per tweet: {}".format(syllable_sum / num_tweets))
        print("Words per tweet: {}".format(word_sum / num_tweets))
        print("Sentences per tweet: {}".format(sentence_sum / num_tweets))
        print("Syllables per word: {}".format(syllable_sum / word_sum))
        print("Words per sentence: {}".format(word_sum / sentence_sum))
        print("Characters per word: {}".format(character_sum / word_sum))
        print("Letters per word: {}".format(letter_count / num_tweets))
        print("Polysyllabs per tweet: {}".format(polysyllab_count / num_tweets))
        print("Number of unique words: {}".format(len(uniques)))
        print("Overall Type-token ratio: {}".format(len(uniques)/word_count))

def nltk_stuff():
    parser = CoreNLPParser(url='http://localhost:9000')
    dep_parser = CoreNLPDependencyParser(url='http://localhost:9000')

    dep_parsed = dep_parser.parse('The quick brown fox jumps over the lazy dog.'.split())
    dep_results = [[(governor, dep, dependent) for governor, dep, dependent in parse.triples()] for parse in dep_parsed]
    print(dep_results)

    basic_parsed = list(parser.raw_parse('The quick brown fox jumps over the lazy dog.'))
    print(basic_parsed)

    tokenised = list(parser.tokenize('The quick brown fox jumps over the lazy dog.'))
    print(tokenised)

    pos_tagger = CoreNLPParser(url='http://localhost:9000', tagtype='pos')
    pos = list(pos_tagger.tag('The quick brown fox jumps over the lazy dog.'.split()))
    print(pos)

def main():
    with open('politics.json') as json_file:
        data = json.load(json_file)
        get_lexicon_stats(data)

if __name__ == "__main__":
    main()