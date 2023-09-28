import argparse
from typing import List
import re
parser = argparse.ArgumentParser(description='ArgumentParser')
parser.add_argument('--pathFirst', type=str, required=True, help="Absolute path to the first Access Analysis result file")
parser.add_argument('--pathSecond', type=str, required=True, help="Absolute path to the second Access Analysis result file to compare against one")
parser.add_argument('--outputDir', type=str, required=True, help="The absolute path to the output directory")
parser.add_argument('--removeCodes', type=bool, default=True, help="Determines if the codes in haskalladio with _h are removed")
parser.add_argument('--handleUUIDs', type=bool, default=False, required=True, help="Provide if pseudo-ids or uuids are used in the results")


class Comparator:

    pathFirst: str
    pathSecond: str
    outputPath: str
    removeHaskCodes: bool = True
    useUUIDs: bool = False

    contentFirst: str
    contentSecond: str

    splitFirst: List[str]
    splitSecond: List[str]

    different: List[str] = []
    commons: List[str] = []

    adv = "adversary("
    byteArrayName = "list("
    commonsFileName= "commonEntries.txt"
    differentFileNames= "differentEntries.txt"

    def __init__(self, pathFirst:str, pathSecond:str, outputPath:str, removeCodes:bool, useUUIDs:bool):
        self.pathFirst = pathFirst
        self.pathSecond = pathSecond
        self.outputPath = outputPath
        self.removeHaskCodes = removeCodes
        self.useUUIDs = useUUIDs

    def read(self, pathFirst, pathSecond):

        with open(pathFirst, 'r') as firstFile:
            self.contentFirst = firstFile.read()

        with open(pathSecond, 'r') as secondFile:
            self.contentSecond = secondFile.read()

        print(self.contentFirst)

        print(self.contentSecond)

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
            #handling in uuid use heavily relies on pretty-print structure.
            if line.startswith(self.adv) or (line.startswith('_') and useUUIDs == True):
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


        #TODO: Do consider line permutations
        for elementInSecond in second:
            for elementInFirst in first:
                if self.removeTreeElements(elementInFirst) == self.removeTreeElements(elementInSecond):
                    common = True

            if common:
                self.commons.append(elementInFirst)
            else:
                self.different.append(elementInFirst)



    def entriesAreEqual(self, firstEntry: str, secondEntry: str) -> bool:

        #entries exactly equal
        if firstEntry == secondEntry:
            return True

        firstEntryLines = firstEntry.splitlines()
        secondEntryLines = secondEntry.splitlines()

        cleanedFirstEntryLines = self.removeTreeElementsAndEmptyLines(firstEntryLines)
        cleanedSecondEntryLines = self.removeTreeElementsAndEmptyLines(secondEntryLines)

        #Length not equal, then the entries cannot be equal
        if not (len(cleanedFirstEntryLines) == len(cleanedSecondEntryLines)):
            return False

        return self.checkLinePermutationEquality(cleanedFirstEntryLines, cleanedSecondEntryLines)




    def checkLinePermutationEquality(self, firstLines: List[str], secondLines: List[str]) -> bool:

        for firstLine in firstLines:
            matches = False
            secondLinesBuffer: List[str] = []
            while secondLines:
                secondLine = secondLines.pop()

                if secondLine == firstLine:
                    matches = True
                    break

                secondLinesBuffer.append(secondLine)

            if not matches:
                return False

            for secondLineForBuffer in secondLines:
                secondLinesBuffer.append(secondLineForBuffer)

            secondLines = secondLinesBuffer

        return True



    def removeTreeElements(self, elementLine : str):

        cleaned = elementLine.replace("`-", '')
        cleaned = cleaned.replace("+-", '')
        cleaned = cleaned.replace('|', '', 1)

        return cleaned

    def removeTreeElementsAndEmptyLines(self, lines: List[str]) -> List[str]:
        cleaned: List[str] = []

        for line in lines:
            cleanedLine = self.removeTreeElements(line)
            cleanedLine = cleanedLine.strip()

            if not isBlank(cleanedLine):
                cleaned.append(cleanedLine)

        return cleaned

    def removeTreeElements(self, elementLine : str):
        cleaned = elementLine
        if cleaned.startswith('|'):
            cleaned = elementLine.replace('|', '')
        else :
            cleaned = cleaned.replace("`-", '')
            cleaned = cleaned.replace("+-", '')

        cleaned = cleaned.strip()

        return cleaned

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
   # args = parser.parse_args()
   # pathFirst = args.pathFirst
   # pathSecond = args.pathSecond
   # pathOut = args.outputDir
   # removeCodes = args.removeCodes

    pathFirst = "C:\\Users\\Frederik Reiche\\git\\casestudies\\Compare\\iflow_new.txt"
    pathSecond = "C:\\Users\\Frederik Reiche\\git\\casestudies\\Compare\\iflow_old.txt"
    pathOut = "C:\\Users\\Frederik Reiche\\git\\casestudies\\Compare\\"
    removeCodes = True
    useUUIDs = True

    comp = Comparator(pathFirst, pathSecond, pathOut, removeCodes, useUUIDs)
    comp.calculateElementRelations()
    comp.writeToFile()
    print("Done")

