import re
class Book:
    def __init__(self, title, author, genre, rating, num_pages, desc):
        title = title.strip()
        title = re.sub(' +', ' ', title)
        self.title = title.replace("\n","")
        author = author.strip()
        author = re.sub(' +', ' ', author)
        self.author = author.replace("\n","")
        self.genre = genre
        self.rating = rating
        self.num_pages = num_pages
        desc.replace("\n", " ")
        self.description = desc.replace("edit data", "")


    def basics(self):
        return "{} by {} ({} stars) ".format(self.title, self.author, self.rating)

    def __str__(self):
        return "{} by {} \n Genre: {} \n {} stars \n {} pages \n\n Description: {}".format(self.title, self.author, self.genre, self.rating, self.num_pages, self.description)
