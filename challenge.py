import re
import math
import json
import wikipedia
# Crawl Part
with open('question_data.json') as f:
    data = json.load(f)

#URL = 'https://en.wikipedia.org/wiki/{url}'
all_docs = {}
doc_frequency = {}
term_frequency = {}
weights = {}

def preprocessing():
    i = 0
    for q in data['questions']:
        if i == 25:
            break;
        wiki_page = q['page']
        i += 1
        try:
            summary = wikipedia.summary(wiki_page).strip().lower()
            summary = re.sub(r'[^\w\s]', '', summary)
            wiki_page = wiki_page.lower().encode('utf-8')
            all_docs[wiki_page] = summary
        except:
            pass

    for doc in all_docs:
        text = all_docs[doc].split()
        text = [word.encode('utf-8') for word in text]
        term_frequency[doc] = {}
        weights[doc] = {}
        for word in text:
            if word not in doc_frequency:
                doc_frequency[word] = doc_count(word, all_docs)
            if word not in term_frequency[doc]:
                term_frequency[doc][word] = frequency_count(word, doc)
            if word not in weights[doc]:
                weights[doc][word] = weight(word, doc)

def preprocessing2(answer):
    for q in data['questions']:
        wiki_page = q['page']
        try:
            summary = wikipedia.summary(wiki_page).strip().lower()
            summary = re.sub(r'[^\w\s]', '', summary)
            wiki_page = wiki_page.lower().encode('utf-8')
            all_docs[wiki_page] = summary
        except:
            pass

    for doc in all_docs:
        term_frequency[doc] = {}
        weights[doc] = {}
        for word in answer.split():
            if word not in doc_frequency:
                doc_frequency[word] = doc_count(word, all_docs)
            if word not in term_frequency[doc]:
                term_frequency[doc][word] = frequency_count(word, doc)
            if word not in weights[doc]:
                weights[doc][word] = weight(word, doc)

def doc_count(word, doc_list):
    result = 0
    for doc in doc_list:
        text = all_docs[doc].split()
        if word in text:
            result += 1
    return result

def frequency_count(word, doc):
    return all_docs[doc].lower().split().count(word.lower())

def weight(word, doc):
    return frequency_count(word, doc) * math.log10(len(all_docs) / doc_frequency[word])

def find_likeliness(page, answer):
    preprocessing2(answer)
    result = 0.0;
    for word in answer.lower().split():
        weight = 0.0
        tf = 0.0
        if page.lower() in weights and word in weights[page.lower()]:
            weight = weights[page.lower()][word]
        if page.lower() in term_frequency and word in weights[page.lower()]:
            tf = term_frequency[page.lower()][word]
        result += weight * tf
    return result

preprocessing()
print find_likeliness('Queequeg', 'Queequeg')
