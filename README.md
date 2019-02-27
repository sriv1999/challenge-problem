# Challenge Problem

The purpose of this program is to create a function that takes a wikipedia page and answer as input and return a real value that corresponds to how likely the answer is to be correct. The implementation was primarily done through means of scraping each wikipedia page summary (using the wikipedia api) and processing each word and document to be applied to tf-idf.


To call the function simply input your parameters of the wikipedia page and answer as string in find_likeliness()

```
print find_likeliness('page', 'answer')
```

There also exist two preprocessing methods. The first preprocessing method creates a dictionary mapping of every word in all documents in the Qanta dataset with its document frequency (in how many documents does the word appear), term_frequency (how many times the word appears in each document), and the weight (a word's weight in its respective document calculated using tf-idf).
