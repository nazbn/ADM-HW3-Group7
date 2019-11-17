from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
from nltk.tokenize import RegexpTokenizer
from index import idfDict,all_words,inverted_index


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


