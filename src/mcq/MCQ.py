import spacy
import nltk

import pprint
import itertools
import re

import requests
import json


from pywsd.similarity import max_similarity
from pywsd.lesk import adapted_lesk
from pywsd.lesk import simple_lesk
from pywsd.lesk import cosine_lesk
from nltk.corpus import wordnet as wn


class MCQ:
    def __init__(self):
        self.syn = None
        self.word = ""
        self.sentence = ""

    def get_wordsense(self):
        word = self.word.lower()

        if len(word.split()) > 0:
            word = word.replace(" ", "_")

        synsets = wn.synsets(word, 'n')
        print(word)
        print(synsets)

        if synsets:
            wup = max_similarity(self.sentence, word, 'wup', pos='n')
            adapted_lesk_output = adapted_lesk(self.sentence, word, pos='n')
            lowest_index = min(synsets.index(wup), synsets.index(adapted_lesk_output))
            self.syn = synsets[lowest_index]
        else:
            self.syn = None

    def get_distractors_wordnet(self):
        distractors = []
        word = self.word.lower()
        orig_word = word
        if len(word.split()) > 0:
            word = word.replace(" ", "_")
        hypernym = self.syn.hypernyms()
        if len(hypernym) == 0:
            return distractors
        for item in hypernym[0].hyponyms():
            name = item.lemmas()[0].name()
            # print ("name ",name, " word",orig_word)
            if name == orig_word:
                continue
            name = name.replace("_", " ")
            name = " ".join(w.capitalize() for w in name.split())
            if name is not None and name not in distractors:
                distractors.append(name)
        return distractors

    def get_distractors_conceptnet(self):
        word = self.word.lower()
        original_word = word
        if (len(word.split()) > 0):
            word = word.replace(" ", "_")
        distractor_list = []
        url = "http://api.conceptnet.io/query?node=/c/en/%s/n&rel=/r/PartOf&start=/c/en/%s&limit=5" % (word, word)
        obj = requests.get(url).json()

        for edge in obj['edges']:
            link = edge['end']['term']

            url2 = "http://api.conceptnet.io/query?node=%s&rel=/r/PartOf&end=%s&limit=10" % (link, link)
            obj2 = requests.get(url2).json()
            for edge in obj2['edges']:
                word2 = edge['start']['label']
                if word2 not in distractor_list and original_word.lower() not in word2.lower():
                    distractor_list.append(word2)

        return distractor_list
