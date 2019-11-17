from html.parser import HTMLParser

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
