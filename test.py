

import re
import random


#nltk.download('stopwords')
#nltk.download('popular')
from src.mcq.MCQ import MCQ
from src.mcq.Summarize import Summarize



def generate():
    filename = "MachineLearning.pdf"
    start = 2
    end = 3
    summarize = Summarize(filename)
    summarize.start = start
    summarize.end = end
    summary = summarize.summarize()
    mcq = MCQ()

    key_distractor_list = {}
    print("#############################################################################")
    for keyword in summary:
        if not summary[keyword]:
            continue
        mcq.sentence = summary[keyword][0]
        mcq.word = keyword
        wordsense = mcq.get_wordsense()
        mcq.word = keyword
        if wordsense:
            mcq.syn = wordsense
            distractors = mcq.get_distractors_wordnet()
            # print(keyword)
            # print(distractors)

            if len(distractors) == 0:
                distractors = mcq.get_distractors_conceptnet()
            if len(distractors) != 0:
                key_distractor_list[keyword] = distractors
        else:
            distractors = mcq.get_distractors_conceptnet()
            if len(distractors) != 0:
                key_distractor_list[keyword] = distractors

    #print(key_distractor_list)

    # index = 1
    # print("#############################################################################")
    # print(
    #     "NOTE::::::::  Since the algorithm might have errors along the way, wrong answer choices generated might not be correct for some questions. ")
    # print("#############################################################################\n\n")
    # for each in key_distractor_list:
    #     if not summary[each]:
    #         continue
    #     sentence = summary[each][0]
    #     pattern = re.compile(each, re.IGNORECASE)
    #     output = pattern.sub(" _______ ", sentence)
    #     print("%s)" % (index), output)
    #     choices = [each.capitalize()] + key_distractor_list[each]
    #     top4choices = choices[:4]
    #     random.shuffle(top4choices)
    #     optionchoices = ['a', 'b', 'c', 'd']
    #     for idx, choice in enumerate(top4choices):
    #         print("\t", optionchoices[idx], ")", " ", choice)
    #     print("\nMore options: ", choices[4:20], "\n\n")
    #     index = index + 1

generate()









