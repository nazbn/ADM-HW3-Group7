from bs4 import BeautifulSoup
import csv
from parser_utils import MyHTMLParser
from collector import urls1,urls2,urls3


att = ["Directed by","Produced by","Written by","Starring","Music by","Release date","Running time","Country","Language","Budget"]

print("Please enter the 3 paths to the articles (like 'C:/Users/chari/HW3ADMGR12/tsv1/article_')")

path1 = input()
path2 = input()
path3 = input()

print("Please enter the 3 paths to create the tsv files (like 'C:/Users/chari/HW3ADMGR12/tsv1/urls1output')")

pathtsv1 = input()
pathtsv2 = input()
pathtsv3 = input()

valid1 = []
valid2 = []
valid3 = []


for k in range(1,10001):

    tot = []
    A = []
    B = []
    name = path1 + str(k) + ".html"
    try:
        file = open(name, encoding='utf8')
        soup = BeautifulSoup(file, 'html.parser')

        # We have to check if the page refers to a film or is a disambiguous page. We do not want to save the disambiguous ones.
        disambiguous = soup.find("table", {"id" : "disambigbox"})

        if disambiguous is not None :
            continue


        right_table = soup.find("table", attrs={"class":"infobox vevent"})

        # We get the title of the film

        # We put a condition to ONLY retrieve the title of the film, without the parenthesis containing the word "movie" and the year

        if soup.select_one('#firstHeading').find("i") != None:

            title = soup.select_one('#firstHeading').find("i").text

        else:

            title  = soup.select_one('#firstHeading').text

        tot.append(title)

        # We get the intro and the plot (1st and 2nd sections)

        intro = ''
        plot = ''


        # We get the intro first

        tag  = soup.select_one('p')

        if tag != None:

            if tag.find_parent('table') == None and tag.text!="\n": # We get the intro if it is not a simple "\n".
                while tag.name == 'p':
                    intro+=tag.text
                    tag = tag.find_next_sibling()


            else: # If the paragraph is in the infobox, we don't append the text but look for the next section

                while tag.text == "\n" or tag.find_parent('table') != None :
                    tag = tag.find_next("p")


                while tag.name == 'p': # While we encounter <p> tags, we add them to the intro. Once a different tag is found, it would mean that we reached the end of the intro
                    intro+=tag.text
                    tag = tag.find_next_sibling()


            # We can now retrieve the second section

            tag = tag.find_next("p") # Now that we left the loop, we are looking for the first p, which would mean we entered the second section

            if tag!= None:

                if tag.find_parent('table') == None and tag.next!="\n" and tag.find_parent('blockquote') == None: # We added a condition on blockquote : we mustn't add quotes as a paragraph ! It's important since some wikipedia pages have an intro in which there is a quote.
                    while tag.name == 'p':
                        plot+=tag.text
                        tag = tag.find_next_sibling()


                else:
                    while tag.text == "\n" or tag.find_parent('table') != None or tag.find_parent('blockquote') != None:
                        tag = tag.find_next("p")


                    while tag.name == 'p':
                        plot+=tag.text
                        tag = tag.find_next_sibling()
            else:
                pass

        else :
            pass


        if intro != "":
            intro = intro.replace("\n", "")
            tot.append(intro)
        else :
            tot.append("NA") # If we didn't find an intro, we simply write NA

        if plot != "":
            plot = plot.replace("\n", "")
            tot.append(plot)
        else :
            tot.append("NA")  # If we didn't find a plot, we simply write NA


        # We now want to get the elements from the infobox

        if right_table != None :
            checkcat = 0 # This will enable us to check if a category is linked to some text. It is really important since, sometimes, an image is put instead
            for row in right_table.findAll("tr"):
                cells = row.findAll('td')
                states=row.findAll('th') #To store second column data
                col = MyHTMLParser()
                val = MyHTMLParser()
                if len(states)>=1:
                    col.feed(str(states[0]))
                    a = col.return_info()
                    if len(a)>=1:
                        A.append(a[0])
                    if len(cells)>=1:
                        val.feed(str(cells[0]))
                        b = val.return_info()
                        if len(b)>=1:
                            B.append(b)
                        else:
                            if checkcat != 0: # We want to keep the first element of the infobox, which is the title of the film
                                A.remove(a[0])
                    else:
                        if checkcat != 0: # We want to keep the first element of the infobox, which is the title of the film
                            A.remove(a[0])
                checkcat+=1


            tot.append(A[0]) # We first append the title of the film

            for i in range(len(att)):
                if att[i] in A[1:]: # We check if we have each piece of information in A and B. If not, we will write "NA".
                    ind = A.index(att[i])
                    if A[ind] == "Release date":
                        if len(B[ind-1])>1:
                            date = ''.join(B[ind-1][2:len(B[ind-1])-1]) # We join all the dates (American date and European date for instance)
                            date = date.replace("\n"," ")
                            tot.append(date)
                        else:
                            tot.append(B[ind-1][0])
                    else:
                        text = " ".join(B[ind-1])
                        text = text.replace("\n", "")
                        tot.append(text)
                else:
                    tot.append("NA")
        else :
            tot = tot + ["NA"]*11 # If we haven't found the infobox, we just append 11 times "NA", as asked on the instructions.


        nametsv = pathtsv1+str(k)+".tsv"
        with open(nametsv, 'w', newline='',encoding = 'utf-8') as f_output:
            tsv_output = csv.writer(f_output, delimiter='\t')
            tsv_output.writerow(tot)
        valid1.append(k)
    except Exception:
        urls1[k - 1] = None
        pass

for k in range(1,10001):

    tot = []
    A = []
    B = []
    name = path2 + str(k) + ".html"
    try:
        file = open(name, encoding='utf8')
        soup = BeautifulSoup(file, 'html.parser')

        # We have to check if the page refers to a film or is a disambiguous page. We do not want to save the disambiguous ones.
        disambiguous = soup.find("table", {"id" : "disambigbox"})

        if disambiguous is not None :
            continue


        right_table = soup.find("table", attrs={"class":"infobox vevent"})

        # We get the title of the film

        # We put a condition to ONLY retrieve the title of the film, without the parenthesis containing the word "movie" and the year

        if soup.select_one('#firstHeading').find("i") != None:

            title = soup.select_one('#firstHeading').find("i").text

        else:

            title  = soup.select_one('#firstHeading').text

        tot.append(title)

        # We get the intro and the plot (1st and 2nd sections)

        intro = ''
        plot = ''


        # We get the intro first

        tag  = soup.select_one('p')

        if tag != None:

            if tag.find_parent('table') == None and tag.text!="\n": # We get the intro if it is not a simple "\n".
                while tag.name == 'p':
                    intro+=tag.text
                    tag = tag.find_next_sibling()


            else: # If the paragraph is in the infobox, we don't append the text but look for the next section

                while tag.text == "\n" or tag.find_parent('table') != None :
                    tag = tag.find_next("p")


                while tag.name == 'p': # While we encounter <p> tags, we add them to the intro. Once a different tag is found, it would mean that we reached the end of the intro
                    intro+=tag.text
                    tag = tag.find_next_sibling()


            # We can now retrieve the second section

            tag = tag.find_next("p") # Now that we left the loop, we are looking for the first p, which would mean we entered the second section

            if tag!= None:

                if tag.find_parent('table') == None and tag.next!="\n" and tag.find_parent('blockquote') == None: # We added a condition on blockquote : we mustn't add quotes as a paragraph ! It's important since some wikipedia pages have an intro in which there is a quote.
                    while tag.name == 'p':
                        plot+=tag.text
                        tag = tag.find_next_sibling()


                else:
                    while tag.text == "\n" or tag.find_parent('table') != None or tag.find_parent('blockquote') != None:
                        tag = tag.find_next("p")


                    while tag.name == 'p':
                        plot+=tag.text
                        tag = tag.find_next_sibling()
            else:
                pass

        else :
            pass


        if intro != "":
            intro = intro.replace("\n", "")
            tot.append(intro)
        else :
            tot.append("NA") # If we didn't find an intro, we simply write NA

        if plot != "":
            plot = plot.replace("\n", "")
            tot.append(plot)
        else :
            tot.append("NA")  # If we didn't find a plot, we simply write NA


        # We now want to get the elements from the infobox

        if right_table != None :
            checkcat = 0 # This will enable us to check if a category is linked to some text. It is really important since, sometimes, an image is put instead
            for row in right_table.findAll("tr"):
                cells = row.findAll('td')
                states=row.findAll('th') #To store second column data
                col = MyHTMLParser()
                val = MyHTMLParser()
                if len(states)>=1:
                    col.feed(str(states[0]))
                    a = col.return_info()
                    if len(a)>=1:
                        A.append(a[0])
                    if len(cells)>=1:
                        val.feed(str(cells[0]))
                        b = val.return_info()
                        if len(b)>=1:
                            B.append(b)
                        else:
                            if checkcat != 0: # We want to keep the first element of the infobox, which is the title of the film
                                A.remove(a[0])
                    else:
                        if checkcat != 0: # We want to keep the first element of the infobox, which is the title of the film
                            A.remove(a[0])
                checkcat+=1


            tot.append(A[0]) # We first append the title of the film

            for i in range(len(att)):
                if att[i] in A[1:]: # We check if we have each piece of information in A and B. If not, we will write "NA".
                    ind = A.index(att[i])
                    if A[ind] == "Release date":
                        if len(B[ind-1])>1:
                            date = ''.join(B[ind-1][2:len(B[ind-1])-1]) # We join all the dates (American date and European date for instance)
                            date = date.replace("\n"," ")
                            tot.append(date)
                        else:
                            tot.append(B[ind-1][0])
                    else:
                        text = " ".join(B[ind-1])
                        text = text.replace("\n", "")
                        tot.append(text)
                else:
                    tot.append("NA")
        else :
            tot = tot + ["NA"]*11 # If we haven't found the infobox, we just append 11 times "NA", as asked on the instructions.


        nametsv = pathtsv2+str(k)+".tsv"
        with open(nametsv, 'w', newline='',encoding = 'utf-8') as f_output:
            tsv_output = csv.writer(f_output, delimiter='\t')
            tsv_output.writerow(tot)
        valid2.append(k)
    except Exception:
        urls2[k - 1] = None
        pass

for k in range(1,10001):

    tot = []
    A = []
    B = []
    name = path3 + str(k) + ".html"
    try:
        file = open(name, encoding='utf8')
        soup = BeautifulSoup(file, 'html.parser')

        # We have to check if the page refers to a film or is a disambiguous page. We do not want to save the disambiguous ones.
        disambiguous = soup.find("table", {"id" : "disambigbox"})

        if disambiguous is not None :
            continue


        right_table = soup.find("table", attrs={"class":"infobox vevent"})

        # We get the title of the film

        # We put a condition to ONLY retrieve the title of the film, without the parenthesis containing the word "movie" and the year

        if soup.select_one('#firstHeading').find("i") != None:

            title = soup.select_one('#firstHeading').find("i").text

        else:

            title  = soup.select_one('#firstHeading').text

        tot.append(title)

        # We get the intro and the plot (1st and 2nd sections)

        intro = ''
        plot = ''


        # We get the intro first

        tag  = soup.select_one('p')

        if tag != None:

            if tag.find_parent('table') == None and tag.text!="\n": # We get the intro if it is not a simple "\n".
                while tag.name == 'p':
                    intro+=tag.text
                    tag = tag.find_next_sibling()


            else: # If the paragraph is in the infobox, we don't append the text but look for the next section

                while tag.text == "\n" or tag.find_parent('table') != None :
                    tag = tag.find_next("p")


                while tag.name == 'p': # While we encounter <p> tags, we add them to the intro. Once a different tag is found, it would mean that we reached the end of the intro
                    intro+=tag.text
                    tag = tag.find_next_sibling()


            # We can now retrieve the second section

            tag = tag.find_next("p") # Now that we left the loop, we are looking for the first p, which would mean we entered the second section

            if tag!= None:

                if tag.find_parent('table') == None and tag.next!="\n" and tag.find_parent('blockquote') == None: # We added a condition on blockquote : we mustn't add quotes as a paragraph ! It's important since some wikipedia pages have an intro in which there is a quote.
                    while tag.name == 'p':
                        plot+=tag.text
                        tag = tag.find_next_sibling()


                else:
                    while tag.text == "\n" or tag.find_parent('table') != None or tag.find_parent('blockquote') != None:
                        tag = tag.find_next("p")


                    while tag.name == 'p':
                        plot+=tag.text
                        tag = tag.find_next_sibling()
            else:
                pass

        else :
            pass


        if intro != "":
            intro = intro.replace("\n", "")
            tot.append(intro)
        else :
            tot.append("NA") # If we didn't find an intro, we simply write NA

        if plot != "":
            plot = plot.replace("\n", "")
            tot.append(plot)
        else :
            tot.append("NA")  # If we didn't find a plot, we simply write NA


        # We now want to get the elements from the infobox

        if right_table != None :
            checkcat = 0 # This will enable us to check if a category is linked to some text. It is really important since, sometimes, an image is put instead
            for row in right_table.findAll("tr"):
                cells = row.findAll('td')
                states=row.findAll('th') #To store second column data
                col = MyHTMLParser()
                val = MyHTMLParser()
                if len(states)>=1:
                    col.feed(str(states[0]))
                    a = col.return_info()
                    if len(a)>=1:
                        A.append(a[0])
                    if len(cells)>=1:
                        val.feed(str(cells[0]))
                        b = val.return_info()
                        if len(b)>=1:
                            B.append(b)
                        else:
                            if checkcat != 0: # We want to keep the first element of the infobox, which is the title of the film
                                A.remove(a[0])
                    else:
                        if checkcat != 0: # We want to keep the first element of the infobox, which is the title of the film
                            A.remove(a[0])
                checkcat+=1


            tot.append(A[0]) # We first append the title of the film

            for i in range(len(att)):
                if att[i] in A[1:]: # We check if we have each piece of information in A and B. If not, we will write "NA".
                    ind = A.index(att[i])
                    if A[ind] == "Release date":
                        if len(B[ind-1])>1:
                            date = ''.join(B[ind-1][2:len(B[ind-1])-1]) # We join all the dates (American date and European date for instance)
                            date = date.replace("\n"," ")
                            tot.append(date)
                        else:
                            tot.append(B[ind-1][0])
                    else:
                        text = " ".join(B[ind-1])
                        text = text.replace("\n", "")
                        tot.append(text)
                else:
                    tot.append("NA")
        else :
            tot = tot + ["NA"]*11 # If we haven't found the infobox, we just append 11 times "NA", as asked on the instructions.


        nametsv = pathtsv3+str(k)+".tsv"
        with open(nametsv, 'w', newline='',encoding = 'utf-8') as f_output:
            tsv_output = csv.writer(f_output, delimiter='\t')
            tsv_output.writerow(tot)
        valid3.append(k)
    except Exception:
        urls3[k-1] = None
        pass


