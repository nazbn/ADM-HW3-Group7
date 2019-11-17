import urllib.request
import urllib.error
import time
from collector_utils import MyHTMLParser

print("Please enter the 3 paths to download the links")
l1 = input()
l2 = input()
l3 = input()

link1 =open(l1, 'r')
link2 =open(l2, 'r')
link3 =open(l3, 'r')



urls1 = []
urls2 = []
urls3 = []

parser = MyHTMLParser()
for item in list(link1):
    parser.feed(item)
    urls1 += parser.return_data()
parser.close()

parser = MyHTMLParser()
for item in list(link2):
    parser.feed(item)
    urls2 += parser.return_data()
parser.close()

parser = MyHTMLParser()
for item in list(link3):
    parser.feed(item)
    urls3 += parser.return_data()
parser.close()

print("Please enter the 3 paths to download each movie")
path1 = input()
path2 = input()
path3 = input()

for k in range(1,len(urls1)+1):
    try:
        name = path1+str(k)+'.html'
        urllib.request.urlretrieve(urls3[k-1], name)
    except urllib.error.HTTPError as err:
        print(err.code)
    except Exception :
        print("error")
        time.sleep(1200)
        urllib.request.urlretrieve(urls3[k-1], name)
    time.sleep(2)

for k in range(1,len(urls2)+1):
    try:
        name = path2+str(k)+'.html'
        urllib.request.urlretrieve(urls3[k-1], name)
    except urllib.error.HTTPError as err:
        print(err.code)
    except Exception :
        print("error")
        time.sleep(1200)
        urllib.request.urlretrieve(urls3[k-1], name)
    time.sleep(2)

for k in range(1,len(urls3)+1):
    try:
        name = path3+str(k)+'.html'
        urllib.request.urlretrieve(urls3[k-1], name)
    except urllib.error.HTTPError as err:
        print(err.code)
    except Exception :
        print("error")
        time.sleep(1200)
        urllib.request.urlretrieve(urls3[k-1], name)
    time.sleep(2)
