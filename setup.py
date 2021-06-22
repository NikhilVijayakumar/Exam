from setuptools import setup

setup(name='Exam',
      version='1.0',
      install_requires=[
        'Flask',
        'gensim',
        'spacy',
        #'git+https://github.com/boudinfl/pke.git',
        'bert-extractive-summarizer',
        'nltk',
        'pdfminer',
        'pywsd',
        'summarizer',
          'flashtext',
          'sentencepiece',
          'torchvision',
          'wn==0.0.23'
    ]
      )