import re
import math
import json
import wikipedia

# Crawl and upload of QANTA question dataset
with open('question_data.json') as f:
    data = json.load(f)

all_docs = {}
doc_frequency = {}
term_frequency = {}
weights = {}

'''
This function processes all the words from all wikipedia pages
in the QANTA question dataset and creates the appropriate dictionaries
of all_docs (wiki page name -> summary),
doc_frequency (word -> how many documents word is found in),
term_frequency (wiki page name -> word -> how many times word is found in this wiki page),
weights (wiki page name -> word -> weight of word developed by tf-idf formula).
'''
def preprocessing():
    # README gives more details :
    # The i represents a counter to limit how many documents will be processed
    i = 0
    for q in data['questions']:
        if i == 100:
            break;
        wiki_page = q['page']
        i += 1

        # Try catch statement to avoid unknown or erroneous wikipedia pages
        try:
            # Using wikipedia API to get summary and create mapping after cleaning text
            summary = wikipedia.summary(wiki_page).strip().lower()

            # Remove punctuation, convert unicode to string, lower case
            summary = re.sub(r'[^\w\s]', '', summary)
            wiki_page = wiki_page.lower().encode('utf-8')
            all_docs[wiki_page] = summary
        except:
            pass

    # Create dictionaries for every word found in every wiki page in dataset
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

'''
This function is nearly identical to the first function except it only processes
and looks for the words given by the user's answer.
'''
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

        # Instead of all words in all documents, only the answer's words are mapped
        for word in answer.split():
            if word not in doc_frequency:
                doc_frequency[word] = doc_count(word, all_docs)
            if word not in term_frequency[doc]:
                term_frequency[doc][word] = frequency_count(word, doc)
            if word not in weights[doc]:
                weights[doc][word] = weight(word, doc)

'''
This function counts the number of documents a given word appears in
'''
def doc_count(word, doc_list):
    result = 0
    for doc in doc_list:
        text = all_docs[doc].split()

        if word in text:
            result += 1

    return result

'''
This function counts the number of appearances of a word in a given document
'''
def frequency_count(word, doc):
    return all_docs[doc].lower().split().count(word.lower())

'''
This function applies the tf-idf formula in order to determine the weights
of the words in a given document respective of the dataset
'''
def weight(word, doc):
    return frequency_count(word, doc) * math.log10(len(all_docs) / doc_frequency[word])

'''
This function, after completion of preprocessing, will take in an answer and
a wikipedia page and return a real value denoting the likeliness that the answer
is correct. The lowest score an answer can receive is a 0.0.
'''
def find_likeliness(page, answer):
    preprocessing()
    #preprocessing2(answer)
    result = 0.0;

    # Computing the sum of (every word's frequency  * its weight) in a given page
    for word in answer.lower().split():
        weight = 0.0
        tf = 0.0

        if page.lower() in weights and word in weights[page.lower()]:
            weight = weights[page.lower()][word]
        if page.lower() in term_frequency and word in weights[page.lower()]:
            tf = term_frequency[page.lower()][word]
        result += weight * tf

    return result

print find_likeliness('Maine', 'Maine')
