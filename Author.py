
class Author:
    def __init__(self, name, avgrating, about):
        self.name = name
        self.avgrating = avgrating
        self.about = about
        if about.strip() == "edit data":
            self.about = "No information available for this author, sorry :("
        self.about = about.replace("edit data", "")

    def __str__(self):
        return "About {}: \n {} \n\n Average Rating for {}'s Books: {}'".format(self.name, self.about, self.name, self.avgrating)
