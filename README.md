# Challenge Problem

The purpose of this program is to create a function that takes a wikipedia page and an answer as input and return a real value that corresponds to how likely the answer is to be correct. The implementation was primarily done through means of scraping each wikipedia page summary (using the wikipedia api) and processing each word and document in order to be applied to the term frequency - inverse document frequency (tf-idf) approach.

To call the function simply input your parameters of the wikipedia page and answer as a string in find_likeliness(). You must have the wikipedia api installed and the question dataset downloaded to the appropriate name ("question_data.json").

```
print find_likeliness('page', 'answer')
```

Furthermore, the user can also call ``` run() ```, which will return the find_likeliness function on the first 1000 values of the Protobowl dataset. The original Protobowl dataset contained 5.2 GB of data; therefore, I have created a reduced dataset of the first 1000 values and converted it to a json file (protobowl_data.json) for convenience and efficiency. The reduced json file was created through means of wrapping it in "responses: {...}" as an array using the "sed" unix command.

There also exist two preprocessing methods.

The first preprocessing method ``` preprocessing() ``` creates a dictionary mapping of every word in all the documents in the Qanta dataset with its document frequency (how many documents does the word appear in), term frequency (how many times the word appears in each document), the weight (a word's weight in its respective document calculated using tf-idf), and creates two joining dictionaries that link the Protobowl dataset answers to the respective question in the question dataset.

The counter in the first preprocessing method, i, was used to speed up testing time by only accumulating data on the first i documents. The counter is not commented out as it will significantly speed up the testing of this program as less data will not need to be processed. However, the limitation is that when a user answers a question to a wikipedia page not yet processed, the find_likeliness() function will default to a real value of 0.0. So, if you know that the wikipedia page for your answer will be processed within the first 500 pages, the counter has been set to finish at 500 pages in order to obtain an answer quickly without having to go through the entire dataset. If using ``` run() ```, the counter set at 500 pages should return likeliness for one of the answers in the Protobowl dataset, specifically "Mickey Mouse", as the answer's appropriate wikipedia page falls within the first 500 processed documents of the question dataset. 

The second preprocessing method ``` preprocessing2('answer') ``` creates a dictionary mapping of only the words in the answer field given by the user to the same as above (document frequency, term frequency, and weights) for an optimized yet not thorough approach.

This program could be significantly optimized by using numpy and nltk, but I used a more general and standard approach to show the crawling, processing, and mapping process more discretely.
