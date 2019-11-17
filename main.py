import pandas as pd
import json
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
from nltk.tokenize import RegexpTokenizer
import math
from sklearn.metrics.pairwise import cosine_similarity
import heapq
import re


def scoring_function1(query, info):
    if len(query) == 0 or info == 'NA':
        similarity = 0.5  # If the user doesn't specify any parameter we consider similarity .5
    else:
        cnt = 0
        for item in query:
            if item.lower() in info.lower():
                cnt += 1
        similarity = cnt / len(query)
    return similarity




def scoring_function2(difference, normalization):
    # for quantitative parameters we're going to use a negetive exponential function
    # to calculate the similarity between the query and the actual value
    # the function is similarity = exp (-(difference)/(normalization))
    # when the release year is equal to the query the difference is 0 and similarity is 1
    return math.exp(-(difference / normalization))


def get_results(subresult):
    results = []
    for i in range(len(subresult)):
        similarity = {}  # a number between 0 and 1
        similarity['name'] = scoring_function1(query['name'], subresult[i][0][3])
        similarity['director'] = scoring_function1(query['director'], subresult[i][0][4])
        similarity['producer'] = scoring_function1(query['producer'], subresult[i][0][5])
        similarity['writer'] = scoring_function1(query['writer'], subresult[i][0][6])
        similarity['starring'] = scoring_function1(query['starring'], subresult[i][0][7])
        similarity['music'] = scoring_function1(query['music'], subresult[i][0][8])
        similarity['country'] = scoring_function1(query['country'], subresult[i][0][11])
        similarity['language'] = scoring_function1(query['language'], subresult[i][0][12])

        if len(query['release_date']) == 0 or subresult[i][0][9] == 'NA':
            similarity['release_date'] = 0.5
        else:
            year = re.search(r'\d{4}', subresult[i][0][9])
            if year != None:
                year = int(year.group(0))
                similarity['release_date'] = scoring_function2(abs(year - int(query['release_date'][0])), 10)
            else:
                similarity['release_date'] = 0.5

        if len(query['runtime']) == 0 or subresult[i][0][10] == 'NA':
            similarity['runtime'] = 0.5
        else:
            runtime = re.search(r'\d+', subresult[i][0][10])
            if year != None:
                runtime = int(runtime.group(0))
                similarity['runtime'] = scoring_function2(abs(runtime - int(query['runtime'][0])), 25)
            else:
                similarity['runtime'] = 0.5

        #     print(subresult[i][0][3])
        #     print(similarity)
        final_value = 0
        for key, value in similarity.items():
            if key == 'name':
                final_value += 2 * value
            else:
                final_value += value
        results.append((final_value / 12, subresult[i]))
    return results




print("Which search engine do you want to use ? Please enter a number")

search_engine = int(input())

print("Please enter the 3 paths to access the tsv files of the 3 folders (ex : C:/Users/chari/HW3ADMGR12/tsv3/urls3output)")

tsv1 = input()
tsv2 = input()
tsv3 = input()

print("Please enter the 3 paths to access the URLs files of the 3 folders")

links1 = input()
links2 = input()
links3 = input()


with open(links1) as json_file:
    urls1 = json.load(json_file)

with open(links2) as json_file:
    urls2 = json.load(json_file)

with open(links3) as json_file:
    urls3 = json.load(json_file)


if search_engine == 1:

    print("Please enter the path to access the vocabulary file for the 1st search engine")
    vocabulary = input()

    print("Please enter the path to access the index file for the 1st search engine")
    indexn = input()

    with open(indexn) as json_file:
        index = json.load(json_file)

    with open(vocabulary) as json_file:
        voc = json.load(json_file)

    print("Please enter a query")
    query = input()

    allquery = query.split()

    # ---------- We have to apply the same process (stemming,removing stopwords...) on the words of the query :

    wordsFiltered = []

    allquery = query.split()

    tokenizer = RegexpTokenizer(r'\w+')

    stopWords = set(stopwords.words('english'))

    for w in allquery:
        if w.lower() not in stopWords:  # We used the lower() function because some stopwords can be written with an uppercase in the tsv files.
            wordsFiltered.append(w.lower())

    allquery = []
    ps = PorterStemmer()
    for w in wordsFiltered:
        allquery.append(ps.stem(w))

    # -----------------------------------------------------------

    subresult = []  # This list will contain each result of the query, before storing it in the dataframe "result".
    d = []

    if all(elem in voc.keys() for elem in allquery):

        for i in range(len(allquery)):
            d.append(index[str(list(voc.keys()).index(allquery[i]))])

        alldocs = list(set(d[0]).intersection(
            *d))  # We get the intersection of all the documents that contain ALL the words of the query.

        for k in range(len(alldocs)):

            iddoc = int(list(set(d[0]).intersection(*d))[k].split("_")[
                            1])  # This is the id of the document. We can now retrieve the info from the targeted movie

            if list(set(d[0]).intersection(*d))[k].split("_")[
                0] == 'document1':  # If the document in which we find the word has that name (+"_k"), we retrieve the tsv files from the set of movies1
                file = open(tsv1 + str(iddoc) + ".tsv", "r", encoding='utf-8')
                url = urls1[iddoc - 1]

            elif list(set(d[0]).intersection(*d))[k].split("_")[0] == 'document2':
                file = open(tsv2 + str(iddoc) + ".tsv", "r", encoding='utf-8')
                url = urls2[iddoc - 1]


            else:
                file = open(tsv3 + str(iddoc) + ".tsv", "r", encoding='utf-8')
                url = urls3[iddoc - 1]

            data = list(file)[0]
            data = data.split("\t")
            subresult.append([data[0], data[1], url])

    # Let us also create a dataframe to present the result of the query

    result = pd.DataFrame(subresult, columns=["Title", "Intro", "Url"])
    print(result)


elif search_engine == 2 :

    print("Please enter the path to the inverted index")
    inverted_index = input()

    print("Please enter the path to the vocabulary")
    all_words = input()

    print("Please enter the path to the index of the 1st search engine")
    indices = input()

    with open(inverted_index) as json_file:
        inverted_index = json.load(json_file)

    with open(all_words) as json_file:
        all_words = json.load(json_file)

    with open(indices) as json_file:
        indices = json.load(json_file)

    N = 29501  # total number of documents
    # compute IDF
    idfDict = {}
    for word in all_words.keys():
        word_index = all_words[word]
        df = len(indices[str(word_index)])
        idfDict[word] = math.log(N / float(df))

    print("Please enter a query")
    query = input()

    # now that we have inverted_index we can handle the queries

    allquery = query.split()
    # ---------- We have to apply the same process (stemming,removing stopwords...) on the words of the query :
    wordsFiltered = []
    allquery = query.split()
    tokenizer = RegexpTokenizer(r'\w+')
    stopWords = set(stopwords.words('english'))

    for w in allquery:
        if w.lower() not in stopWords:  # We used the lower() function because some stopwords can be written with an uppercase in the tsv files.
            wordsFiltered.append(w.lower())
    allquery = []
    ps = PorterStemmer()
    for w in wordsFiltered:
        allquery.append(ps.stem(w))

    subresult = []  # This list will contain each result of the query
    d = []

    if all(elem in all_words.keys() for elem in allquery):
        for w in allquery:
            d.append(indices[str(all_words[w])])
        alldocs = list(set(d[0]).intersection(*d))

        for k in range(len(alldocs)):
            name = alldocs[k].split("_")
            iddoc = int(name[1])  # This is the id of the document.
            folder = int(name[0][-1])
            # We can now retrieve the info from the targeted movie
            if folder == 1:
                file = open(tsv1 + str(iddoc) + ".tsv", "r", encoding='utf-8')
                url = urls1[iddoc - 1]
            elif folder == 2:
                file = open(tsv2 + str(iddoc) + ".tsv", "r", encoding='utf-8')
                url = urls2[iddoc - 1]
            elif folder == 3:
                file = open(tsv3 + str(iddoc) + ".tsv", "r", encoding='utf-8')
                url = urls3[iddoc - 1]
            data = list(file)[0]
            data = data.split("\t")
            subresult.append([data[0], data[1], url, iddoc, folder])

    # first we compute tf-idf for each word in the query
    if len(subresult) != 0:
        word_dict = {}
        query_tfidf = []  # vector to store all tf-idf scores
        # compute tf-idf for each word in the query
        for w in allquery:
            if w not in word_dict:
                word_dict[w] = 1
            else:
                word_dict[w] += 1
        for w in allquery:
            count = word_dict[w]
            tf = count / float(len(allquery))
            tfidf = tf * idfDict[word]
            query_tfidf += [tfidf]

    # now we need to create the same vector for each result
    results = []
    for item in subresult:
        word_dict = {}
        tfidf_vector = []
        for w in allquery:
            for elem in inverted_index[str(all_words[w])]:
                if elem[0] == 'Document' + str(item[4]) + '_' + str(item[3]):
                    tfidf_vector.append(elem[1])
        # now that we have the tf-idf vector we can calculate similarity
        similarity = cosine_similarity([query_tfidf], [tfidf_vector])[0][0]
        results.append((similarity, item))
    k = 10  # how many results are we going to show
    results = heapq.nlargest(10, results)
    final_results = []
    for item in results:
        final_results.append([item[1][0], item[1][1], item[1][2], item[0]])
    result = pd.DataFrame(final_results, columns=["Title", "Intro", "Url", "Similarity"])
    print(result)



elif search_engine == 3 :

    print("Please enter the path to the vocabulary file")
    pathvoc = input()

    print("Please enter the path to the index file")
    pathindex = input()

    with open(pathvoc) as json_file:
        all_words = json.load(json_file)
    with open(pathindex) as json_file:
        indices = json.load(json_file)

    # now that we have inverted_index we can handle the queries
    print("Please enter a query")
    query = input()
    allquery = query.split()
    # ---------- We have to apply the same process (stemming,removing stopwords...) on the words of the query :
    wordsFiltered = []
    allquery = query.split()
    tokenizer = RegexpTokenizer(r'\w+')
    stopWords = set(stopwords.words('english'))

    for w in allquery:
        if w.lower() not in stopWords:  # We used the lower() function because some stopwords can be written with an uppercase in the tsv files.
            wordsFiltered.append(w.lower())
    allquery = []
    ps = PorterStemmer()
    for w in wordsFiltered:
        allquery.append(ps.stem(w))

    subresult = []  # This list will contain each result of the query
    d = []

    if all(elem in all_words.keys() for elem in allquery):
        for w in allquery:
            d.append(indices[str(all_words[w])])
        alldocs = list(set(d[0]).intersection(*d))

        for k in range(len(alldocs)):
            name = alldocs[k].split("_")
            iddoc = int(name[1])  # This is the id of the document.
            folder = int(name[0][-1])
            # We can now retrieve the info from the targeted movie
            if folder == 1:
                file = open(tsv1 + str(iddoc) + ".tsv", "r", encoding='utf-8')
                url = urls1[iddoc - 1]
            elif folder == 2:
                file = open(tsv2 + str(iddoc) + ".tsv", "r", encoding='utf-8')
                url = urls2[iddoc - 1]
            elif folder == 3:
                file = open(tsv3 + str(iddoc) + ".tsv", "r", encoding='utf-8')
                url = urls3[iddoc - 1]
            data = list(file)[0]
            data = data.split("\t")
            subresult.append([data, url, iddoc, folder])

    query = {'text': allquery, 'name': [], 'director': [], 'producer': [], 'writer': [], 'starring': [],
             'music': [], 'release_date': [], 'runtime': [], 'country': [], 'language': [], 'budget': []}
    number = 1
    while number != 0:
        number = int(input("Enter the number of parameter you wish to add:" +
                           "\n1. Film Name\n2. Director\n3. Producer\n4. Writer\n5. " +
                           "Starring\n6. Music\n7. Release Date\n8. Runtime\n9. " +
                           "Country\n10. Language\n11. Budget\nEnter 0 if you're done.\n"))
        if number == 1:
            name = input("Enter Film Name:\n")
            query['name'] += [name]
        elif number == 2:
            director = input("Enter Director's name:\n")
            query['director'] += [director]
        elif number == 3:
            Producer = input("Enter Producer's name:\n")
            query['producer'] += [Producer]
        elif number == 4:
            Writer = input("Enter Writer's name:\n")
            query['writer'] += [Writer]
        elif number == 5:
            Starring = input("Enter Star's name:\n")
            query['starring'] += [Starring]
        elif number == 6:
            Music = input("Enter Musician's name:\n")
            query['music'] += [Music]
        elif number == 7:
            release_date = input("Enter Release Year:\n")
            query['release_date'] += [release_date]
        elif number == 8:
            runtime = input("Enter Runtime in minutes:\n")
            query['runtime'] += [runtime]
        elif number == 9:
            Country = input("Enter Country:\n")
            query['country'] += [Country]
        elif number == 10:
            Language = input("Enter Language:\n")
            query['language'] += [Language]
        elif number == 11:
            Budget = input("Enter Budget:\n")
            query['budget'] += [Budget]

    results = get_results(subresult)
    k = 10  # how many results are we going to show
    results = heapq.nlargest(10, results)
    final_results = []
    for item in results:
        final_results.append([item[1][0][0], item[1][0][1], item[1][0][2], item[0]])
    result = pd.DataFrame(final_results, columns=["Title", "Intro", "Url", "Similarity"])
    print(result)

else :
    print("You did not enter a valid number")


