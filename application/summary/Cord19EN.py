import application.summary.Cord19 as cord19


class Cord19EN(cord19.Cord19):

    def __init__(self):
        super().__init__("en")
        print("Ready to answer question from the English edition of CORD-19 collection")
    

