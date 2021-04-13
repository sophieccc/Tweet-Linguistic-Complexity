import json
from nltk import tokenize
from nltk.corpus import stopwords
import random
from nltk.tree import Tree
import textstat
from nltk.parse import CoreNLPParser, CoreNLPDependencyParser
from collections import Counter
import string

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
        print("Total sentences: {}".format(sentence_sum))
        print("Sentences per tweet: {}".format(sentence_sum / num_tweets))
        print("Syllables per word: {}".format(syllable_sum / word_sum))
        print("Words per sentence: {}".format(word_sum / sentence_sum))
        print("Characters per word: {}".format(character_sum / word_sum))
        print("Letters per word: {}".format(letter_count / num_tweets))
        print("Polysyllabs per tweet: {}".format(polysyllab_count / num_tweets))
        print("Number of unique words: {}".format(len(uniques)))
        print("Overall Type-token ratio: {}".format(len(uniques)/word_count))

def count_nodes(tree, count, num_s):
    count +=1
    if tree.label().startswith("S"):
        num_s +=1
    for subtree in tree:
        if type(subtree) == Tree:
            count, num_s = count_nodes(subtree, count, num_s)
    return count, num_s

def nltk_stuff(data):
    parser = CoreNLPParser(url='http://localhost:9000')
    num_nodes = 0
    num_s = 0
    height = 0
    subset = dict(random.sample(data.items(), 5000))
    get_lexicon_stats(subset)
    print("\n")
    for _, value in subset.items():  
        parsed = list(parser.parse(value.split()))
        height += parsed[0].height()
        curr_num_nodes, curr_num_s = count_nodes(parsed[0][0], 0, 0)
        num_nodes += curr_num_nodes
        num_s += curr_num_s
    print("Num clauses: {}".format(num_s))
    print("Num nodes: {}".format(num_nodes))
    print("Total height: {}".format(height))
    print("Avg nodes per tweet: {}".format(num_nodes / len(subset.items())))
    print("Avg height of tweet: {}".format(height / len(subset.items())))
    
    # dep_parser = CoreNLPDependencyParser(url='http://localhost:9000')
    # dep_parsed = dep_parser.parse('The quick brown fox jumps over the lazy dog.'.split())
    # dep_results = [[(governor, dep, dependent) for governor, dep, dependent in parse.triples()] for parse in dep_parsed]
    # print(dep_results)

def verb_stats(data):
    pos_tagger = CoreNLPParser(url='http://localhost:9000', tagtype='pos')
    verb_count = 0
    for _, value in data.items():
        pos = list(pos_tagger.tag(value.split()))
        for _,second in pos:
            if second.startswith("V"):
                verb_count +=1
    print(verb_count)    

def top_words():
    with open('politics_full.txt') as text:
        words = tokenize.word_tokenize(text.read())
        no_stopwords = [word for word in words if not (word in stopwords.words()) and not (word in string.punctuation)]
        counter = Counter(no_stopwords)
        total_frequency = sum(counter.values())
        top_frequency = 0
        for word in counter.most_common(50):
            top_frequency += word[1]
        print(total_frequency)
        print(top_frequency)
        print((top_frequency / total_frequency) * 100)
        


def main():
    with open('sports.json') as json_file:
        data = json.load(json_file)
        #position_stats(data)
        #get_lexicon_stats(data)
        #nltk_stuff(data)
        top_words()

if __name__ == "__main__":
    main()