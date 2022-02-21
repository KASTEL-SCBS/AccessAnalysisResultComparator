import argparse
from typing import List
import re
parser = argparse.ArgumentParser(description='ArgumentParser')
parser.add_argument('--pathFirst', type=str, required=True, help="Absolute path to the first Access Analysis result file")
parser.add_argument('--pathSecond', type=str, required=True, help="Absolute path to the second Access Analysis result file to compare against one")
parser.add_argument('--outputDir', type=str, required=True, help="The absolute path to the output directory")
parser.add_argument('--removeCodes', type=bool, default=True, help="Determines if the codes in haskalladio with _h are removed")

testPath2 = "C:/Users/Freddy/git/Diss/PCM2Java4Joana/material/analysisresults/AccessAnalysis/queries-justify-backprojected.result.pretty"
testPath1 = "C:/Users/Freddy/git/Diss/PCM2Java4Joana/material/analysisresults/AccessAnalysis/queries-justify-origin.result.pretty"
testOutputPath = "C:/Users/Freddy/git/Diss/PCM2Java4Joana/material/analysisresults/AccessAnalysis"


class Comparator:

    pathFirst: str
    pathSecond: str
    outputPath: str
    removeHaskCodes: bool = True

    contentFirst: str
    contentSecond: str

    splitFirst: List[str]
    splitSecond: List[str]

    different: List[str] = []
    commons: List[str] = []

    adv = "adversary("
    commonsFileName= "commonEntries.txt"
    differentFileNames= "differentEntries.txt"

    def __init__(self, pathFirst:str, pathSecond:str, outputPath:str, removeCodes:bool):
        self.pathFirst = pathFirst
        self.pathSecond = pathSecond
        self.outputPath = outputPath
        self.removeHaskCodes = removeCodes

    def read(self, pathFirst, pathSecond):

        with open(pathFirst, 'r') as firstFile:
            self.contentFirst = firstFile.read()

        with open(pathSecond, 'r') as secondFile:
            self.contentSecond = secondFile.read()

        if self.removeHaskCodes:
            self.contentFirst = removeHaskalladioCodes(self.contentFirst)
            self.contentSecond = removeHaskalladioCodes(self.contentSecond)


    def splitAAResults(self):
        self.splitFirst = self.splitAAResult(self.contentFirst)
        self.splitSecond = self.splitAAResult(self.contentSecond)

    def splitAAResult(self, content: str) -> List[str]:
        splitResults: List[str] = []
        allLines = content.split("\n")

        statement = ""
        parsingElement = False

        for line in allLines:
            if line.startswith(self.adv):
                parsingElement = True
                statement = ""

            if isBlank(line):
                parsingElement = False
                splitResults.append(statement)

            if parsingElement:
                statement += (line + "\n")

        return splitResults

    def calculateElementRelations(self):

        self.read(self.pathFirst, self.pathSecond)
        self.splitAAResults()
        self.calculateElementsRelations(self.splitFirst, self.splitSecond)

    def calculateElementsRelations(self, first: List[str], second: List[str]):

        common = False

        for elementInSecond in second:
            for elementInFirst in first:
                if elementInFirst == elementInSecond:
                    common = True

            if common:
                self.commons.append(elementInSecond)
            else:
                self.different.append(elementInSecond)

            common = False

    def writeToFile(self):
        with open("{path}/{fileName}".format(path= self.outputPath, fileName=self.differentFileNames),'w') as diff:
            diff.write(concatinateWithEmptyLine(self.different))

        with open("{path}/{fileName}".format(path= self.outputPath, fileName=self.commonsFileName),'w') as comm:
            comm.write(concatinateWithEmptyLine(self.commons))



def isBlank(myString: str):
    return not (myString and myString.strip())

def removeHaskalladioCodes(result: str):
    return re.sub(r"_h\d+(,)?", "", result)

def concatinateWithEmptyLine(strings: List[str]):
    result = ""

    for string in strings:
        result += string + "\n"

    return result

if __name__ == '__main__':
    args = parser.parse_args()
    pathFirst = args.pathFirst
    pathSecond = args.pathSecond
    pathOut = args.outputDir
    removeCodes = args.removeCodes

    comp = Comparator(pathFirst, pathSecond, pathOut, removeCodes)
    comp.calculateElementRelations()
    comp.writeToFile()
    print("Done")

