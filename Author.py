
class Author:
    def __init__(self, name, avgrating, about):
        self.name = name
        self.avgrating = avgrating
        self.about = about

    def __str__(self):
        return "About {}: \n {} \n\n Average Rating for {}'s Books: {}'".format(self.name, self.about, self.name, self.avgrating)
