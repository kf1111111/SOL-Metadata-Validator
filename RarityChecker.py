from tabulate import tabulate
from termcolor import cprint
import random


class RarityChecker:

    def __init__(self):
        self.rarityCounterDict = {}
        self.attributeLegend = {}
        self.colorPalette = [
            "grey",
            "red",
            "green",
            "yellow",
            "blue",
            "magenta",
            "cyan",
            "white"
        ]

    def processAtributeSet(self, attributes):

        for attr in attributes:
            if attr['trait_type'] not in self.rarityCounterDict.keys():
                self.rarityCounterDict[attr['trait_type']] = {}
            if attr['value'] not in self.rarityCounterDict[attr['trait_type']].keys():
                self.rarityCounterDict[attr['trait_type']][attr['value']] = 1
            else:
                self.rarityCounterDict[attr['trait_type']][attr['value']] += 1

        self.assignColorsToAttributes()

    def displayRawData(self):
        print(self.rarityCounterDict)

    def assignColorsToAttributes(self):
        for attributeCategory in self.rarityCounterDict.keys():
            self.attributeLegend[attributeCategory] = random.choice(self.colorPalette)

    def displayAttributeCategories(self):
        cprint('\n{} ATTRIBUTE CATEGORIES FOUND:'.format(len(self.attributeLegend.keys())), 'white')
        for attributeCategory in self.attributeLegend.keys():
            cprint(attributeCategory, self.attributeLegend[attributeCategory])

    def roundTo2Decimal(self, num):
        return "{:.2f}".format(num)

    def composeRarityTable(self, attributeDict, totalFiles):
        rarityTable = []
        totalAttrs = sum(attributeDict.values())
        for attr in attributeDict.keys():
            attributeRarity = self.roundTo2Decimal((attributeDict[attr] / totalFiles) * 100)
            rarityTable.append([attr, attributeDict[attr], '{}%'.format(attributeRarity)])
        rarityTable.append(['TOTAL', totalAttrs, self.roundTo2Decimal(totalAttrs / totalFiles * 100)])
        return rarityTable

    def displayRarityTables(self, totalFiles):

        cprint('\nRARITY', 'white')
        cprint('*************', 'white')
        for attributeCategory in self.rarityCounterDict.keys():
            rarityTable = self.composeRarityTable(self.rarityCounterDict[attributeCategory], totalFiles)
            cprint(attributeCategory, self.attributeLegend[attributeCategory])
            cprint(tabulate(rarityTable, headers=['Attribute Name', 'Count', 'Rarity %']),
                   self.attributeLegend[attributeCategory])
            print('\n')
