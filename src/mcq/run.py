from nltk.corpus import wordnet
word = 'linear regression'

syn = wordnet.synsets(word)[0]

print("Synset name :  ", syn.name())

# Defining the word
print("\nSynset meaning : ", syn.definition())

# list of phrases that use the word in context
print("\nSynset example : ", syn.examples())