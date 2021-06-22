from summarizer import Summarizer
import pke
import string
from nltk.corpus import stopwords
from nltk.tokenize import sent_tokenize
from flashtext import KeywordProcessor
from pdfminer import high_level

class Summarize:

    def __init__(self,filename):
        self.filename = filename
        self.start = 0
        self.end = 0
        self.text = ""
        self.sentences = ""
        self.summarized_text = ""
        self.keywords =  []
        self.filtered_keys = []

    def get_text(self):
        for page in range(self.start, self.end + 1):
            pages = [page]
            self.text += high_level.extract_text(self.filename, "", pages)


    def get_summary(self):
        model = Summarizer()
        result = model(self.text, min_length=60, max_length=500, ratio=0.4)
        self.summarized_text = ''.join(result)


    def get_nouns_multipartite(self):
        out = []

        extractor = pke.unsupervised.MultipartiteRank()
        extractor.load_document(input=self.text)

        pos = {'PROPN'}

        stoplist = list(string.punctuation)
        stoplist += ['-lrb-', '-rrb-', '-lcb-', '-rcb-', '-lsb-', '-rsb-']
        stoplist += stopwords.words('english')
        extractor.candidate_selection(pos=pos, stoplist=stoplist)

        extractor.candidate_weighting(alpha=1.1,
                                      threshold=0.75,
                                      method='average')
        keyphrases = extractor.get_n_best(n=20)

        for key in keyphrases:
            out.append(key[0])

        self.keywords = out

        for keyword in self.keywords:
            if keyword.lower() in self.summarized_text.lower():
                self.filtered_keys.append(keyword)


    def tokenize_sentences(self):
        self.sentences = [sent_tokenize(self.text)]
        self.sentences = [y for x in self.sentences for y in x]
        self.sentences = [sentence.strip() for sentence in self.sentences if len(sentence) > 20]


    def get_sentences_for_keyword(self):
        keyword_processor = KeywordProcessor()
        keyword_sentences = {}
        for word in self.filtered_keys:
            keyword_sentences[word] = []
            keyword_processor.add_keyword(word)
        for sentence in self.sentences:
            keywords_found = keyword_processor.extract_keywords(sentence)
            for key in keywords_found:
                keyword_sentences[key].append(sentence)

        for key in keyword_sentences.keys():
            values = keyword_sentences[key]
            values = sorted(values, key=len, reverse=True)
            keyword_sentences[key] = values
        return keyword_sentences

    def summarize(self):
        self.get_text()
        self.get_summary()
        self.get_nouns_multipartite()
        self.tokenize_sentences()
        return self.get_sentences_for_keyword()
