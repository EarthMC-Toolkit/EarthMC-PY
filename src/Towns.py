import json, requests

class towns:
    def __init__(self):
        self.methods = ["all", "get"]
    def printMethods(self):
        for method in self.methods:
            print('\t%s ' % method)