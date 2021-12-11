import hashlib
import json
from termcolor import cprint
from tabulate import tabulate

class MetadataDuplicateChecker():

    def __init__(self):
        self.hashDict = {}
        self.duplicateTable = []


    def processAtributeSet(self, attributes, fileName):
        dhash = hashlib.md5()
        # We need to sort arguments so {'a': 1, 'b': 2} is
        # the same as {'b': 2, 'a': 1}
        encoded = json.dumps(attributes, sort_keys=True).encode()
        dhash.update(encoded)
        hexHash = dhash.hexdigest()
        if hexHash in self.hashDict.keys():
            self.duplicateTable.append([self.hashDict[hexHash], fileName])
            # cprint('****************************\nWARNING! Duplicate detected:\nFile1: {}\nFile2: {}'.format(self.hashDict[hexHash], fileName), 'red')
        else:
            self.hashDict[hexHash]= fileName


    def displayDuplicateTable(self):
        cprint('\nDUPLICATES','white')
        cprint('*************','white')
        if len(self.duplicateTable) == 0:
            cprint('Duplicate Check OK - 0 Found', 'green')
        else:
            cprint('WARNING! Following Duplicates Found:', 'red')
            cprint(tabulate(self.duplicateTable, headers=['File 1', 'File 2']),'red')

    #TODO: SORT TABLE