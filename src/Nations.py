from .Functions import functions

functions = functions()

class nations:
    def __init__(self):
        self.methodsArray = ["all", "get"]
    def methods(self): return self.methodsArray
    def all(self): return "Not created yet."