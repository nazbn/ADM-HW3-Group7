import json
import math
from index_utils import creationind, update_inverted_index

print("Please enter the 3 paths to access the list of valid URLs (like C:/Users/chari/HW3ADMGR12/links1)")


links1 = input()
links2 = input()
links3 = input()


print("Please enter the 3 paths to access the list of valid URLs (like C:/Users/chari/HW3ADMGR12/links1)")


val1 = input()
val2 = input()
val3 = input()

with open(links1) as json_file:
    urls1 = json.load(json_file)

with open(links2) as json_file:
    urls2 = json.load(json_file)

with open(links3) as json_file:
    urls3 = json.load(json_file)

with open(val1) as json_file:
    valid1 = json.load(json_file)

with open(val2) as json_file:
    valid2 = json.load(json_file)

with open(val3) as json_file:
    valid3 = json.load(json_file)

print("Please enter the 3 paths to access the tsv files")

tsv1 = input()
tsv2 = input()
tsv3 = input()





#-------------- FOR THE FIRST SEARCH ENGINE -------------------


vocab = []
dicti = {} # This dictionary will enable us to fill the index dictionary (for the Inverted index)
index = {} # This dictionary will contain the "patterns" of words as keys and the name of the documents in which they are

folder = 1

allinfos = creationind(folder,valid1,tsv1,dicti,vocab)
dicti = allinfos[0]
vocab = allinfos[1]

# We got the updated version of the vocabulary, so that we can continue updating it with movies2 and 3



folder = 2

allinfos = creationind(folder,valid2,tsv2,dicti,vocab)
dicti = allinfos[0]
vocab = allinfos[1]



folder = 3

allinfos = creationind(folder,valid3,tsv3,dicti,vocab)
dicti = allinfos[0]
vocab = allinfos[1]



# We can now create the inverted index :

voc = {}  # We will store the vocabulary into a json file, thanks to a dictionary

# Finally, we got the inverted index and the vocabulary.

for k in range(len(vocab)):
    voc[vocab[k]] = k
    index[k] = dicti[vocab[k]]

print("Please enter a path to create the file for the vocabulary")

vocabulary = input()

with open(vocabulary, 'w') as f:
    json.dump(voc, f)


print("Please enter a path to create the file for the vocabulary")

indexn = input()

with open(indexn, 'w') as f:
    json.dump(index, f)





# ------------------ FOR THE SECOND SEARCH ENGINE ------------------------

print("Please enter the path to get the vocabulary of the 1st search engine(ex : 'C:/Users/chari/HW3ADMGR12/vocabulary.json')")

all_words = input()

print("Please enter the path to get the indices of the first search engine")

indices = input()

with open(all_words) as json_file:
    all_words = json.load(json_file)

with open(indices) as json_file:
    indices = json.load(json_file)



N = 29501 # total number of documents
#compute IDF
idfDict = {}
for word in all_words.keys():
    word_index = all_words[word]
    df = len(indices[str(word_index)])
    idfDict[word] = math.log(N/float(df))

print("Please enter a path to save the idf scores")
idfpath = input()

with open(idfpath, 'w') as f:
    json.dump(idfDict, f)

inverted_index = {k: [] for k in indices.keys()}

update_inverted_index(tsv1, 1)
update_inverted_index(tsv2, 2)
update_inverted_index(tsv3, 3)


with open('inverted_index.json', 'w') as f:
    json.dump(inverted_index, f)



# ---------------------- FOR THE THIRD SEARCH ENGINE ------------------

