import json, requests

class nations:
    def __init__(self):
        self.methods = ["all", "get"]
    def printMethods(self):
        for method in self.methods:
            print('\t%s ' % method)