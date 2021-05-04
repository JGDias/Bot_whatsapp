import spacy

nlp = spacy.load('en_core_web_sm')
doc = nlp(u'This is a test')
print(doc)