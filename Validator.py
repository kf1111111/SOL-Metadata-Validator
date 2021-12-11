from DuplicateChecker import MetadataDuplicateChecker
from RarityChecker import RarityChecker
import glob, os
from termcolor import cprint
import pathlib
import json


class MetadataValidator:

    def __init__(self):
        cprint('SOL Metadata Validation tool by Foxxy#0001\n', 'magenta')
        self.fileCount = 0
        self.duplicateChecker = MetadataDuplicateChecker()
        self.rarityChecker = RarityChecker()
        self.royaltyOk = True
        self.walletOk = True

    def loadFileNames(self, metadataPath):
        fileNames = []
        cprint('Loading Filenames...', 'yellow')
        os.chdir('{}{}'.format(pathlib.Path().resolve(), metadataPath))
        for file in glob.glob("*.json"):
            fileNames.append(file)
        cprint('Filenames Loaded!', 'green')
        self.fileCount = len(fileNames)
        return fileNames

    def walletCheck(self, walletFromUser, walletFromFile, fileName):
        if walletFromUser and walletFromFile != walletFromUser:
            cprint('[{}] WARNING! Wrong wallet in metadata: {}'.format(fileName, walletFromFile))
            self.walletOk = False

    def royaltyCheck(self, royaltyFromUser, royaltyFromFile, fileName):
        if royaltyFromUser and int(royaltyFromUser) != int(royaltyFromFile) / 100:
            cprint('[{}] WARNING! Wrong royalty value: {}'.format(fileName, royaltyFromFile))
            self.royaltyOk = False

    def displayWalletCheckResult(self, wallet):
        if wallet and not self.walletOk:
            cprint('WALLET CHECK NOT PASSED! Please see above for details', 'red')
        elif wallet:
            cprint('Wallet check OK', 'green')

    def displayRoyaltyCheckResult(self, royaltyPercentage):
        if royaltyPercentage and not self.royaltyOk:
            cprint('ROYALTY CHECK NOT PASSED! Please see above for details', 'red')
        elif royaltyPercentage:
            cprint('Royalty check OK', 'green')

    def processMetadata(self, metadataPath='/input', wallet='', royaltyPercentage=''):
        fileNames = self.loadFileNames(metadataPath)
        cprint('Processing Metadata...', 'yellow')
        for fileName in fileNames:
            # todo: add filename consecutivity check
            with open('{}/{}'.format(pathlib.Path().resolve(), fileName)) as json_file:
                data = json.load(json_file)

                self.walletCheck(wallet, data['properties']['creators'][0]['address'], fileName)
                self.royaltyCheck(royaltyPercentage, data['seller_fee_basis_points'], fileName)
                attributes = data['attributes']
                self.rarityChecker.processAtributeSet(attributes)
                self.duplicateChecker.processAtributeSet(attributes, fileName)

        cprint('Metadata Processed! Results Below:', 'green')

        self.displayWalletCheckResult(wallet)
        self.displayRoyaltyCheckResult(royaltyPercentage)
        self.duplicateChecker.displayDuplicateTable()
        self.rarityChecker.displayAttributeCategories()
        self.rarityChecker.displayRarityTables(self.fileCount)
