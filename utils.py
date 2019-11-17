from html.parser import HTMLParser
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
from nltk.tokenize import RegexpTokenizer
from index import inverted_index, all_words, idfDict


class MyHTMLParser(HTMLParser):
    def __init__(self):
        self.d = []
        self.info = []  # This list will be useful to get the info from the infobox of wikipedia
        self.tag = []  # We will use that to know when we have to stop retrieving the paragraphs
        super().__init__()

    def handle_starttag(self, tag, attrs):
        self.tag = []
        self.tag.append(tag)
        return (tag)

    def handle_data(self, data):
        if data.startswith('https'):
            self.d.append(data)
        else:
            self.info.append(data)
        return (data)

    def return_data(self):
        return (self.d)

    def return_info(self):
        return (self.info)

    def return_tag(self):
        if len(self.tag) != 0:
            return (self.tag[0])

# To check if it is an url, we check if it begins with "https"


def creationind(folder,valid,tsv,dicti,vocab):
    for k in valid:

        file = open(tsv + str(k) + ".tsv", "r", encoding='utf-8')
        data = list(file)[0]
        data = data.split("\t")
        data = data[1:3]
        data = " ".join(data)
        tokenizer = RegexpTokenizer(r'\w+')

        words = tokenizer.tokenize(data)

        wordsFiltered = []

        stopWords = set(stopwords.words('english'))

        for w in words:
            if w.lower() not in stopWords:  # We used the lower() function because some stopwords can be written with an uppercase in the tsv files.
                wordsFiltered.append(w)

        ps = PorterStemmer()

        for w in wordsFiltered:

            if ps.stem(w) not in vocab:
                vocab.append(ps.stem(w))
                dicti[ps.stem(w)] = ["document"+str(folder)+"_" + str(k)]
            else:
                if "document"+str(folder)+"_" + str(k) not in dicti[ps.stem(w)]:
                    dicti[ps.stem(w)].append("document"+str(folder)+"_" + str(k))
    return(dicti,vocab)


def update_inverted_index(path, folder):
    for k in range(1, 10001):
        try:
            file = open(path+str(k)+".tsv","r",encoding='utf-8')
            data = list(file)[0]
            data = data.split("\t")
            data = data[:3]
            data = " ".join(data)
            tokenizer = RegexpTokenizer(r'\w+')
            words = tokenizer.tokenize(data)
            wordsFiltered = []
            stopWords = set(stopwords.words('english'))

            for w in words:
                if w.lower() not in stopWords: # We used the lower() function because some stopwords can be written with an uppercase in the tsv files.
                    wordsFiltered.append(w)

            word_dict = {}
            ps = PorterStemmer()
            for w in wordsFiltered:
                word_st = ps.stem(w)
                if  word_st not in word_dict:
                    word_dict[word_st] = 1
                else:
                    word_dict[word_st] += 1

            #compute tf and tfidf
            for word, count in word_dict.items():
                tf = count/float(len(wordsFiltered))
                tfidf = tf * idfDict[word]
                word_index = all_words[word]
                #update the inverted index
                inverted_index[str(word_index)].append(('Document' + str(folder) + "_" + str(k), tfidf))
        except:
            pass

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


