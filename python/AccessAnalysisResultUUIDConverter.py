import argparse
from typing import List
import re
parser = argparse.ArgumentParser(description='ArgumentParser')
parser.add_argument('--path', type=str, required=True, help="Absolute path to the access analysis result file")
parser.add_argument('--outputPath', type=str, required=False, help="Absolute path for writing output, when not provided override input file")

byteArrayRegex = "(list\(([0-9]+,?)+(\)))"

def read(path):
    content = ""
    with open(path, 'r') as firstFile:
       content = firstFile.read()
    return content

def extractStringFromByteListEntry(content:str):
    tmp = content.replace("list(", "")
    tmp = tmp.replace(")", "")
    numbersStrings = tmp.split(',')

    myInts = []

    for number in numbersStrings:
        myInts.append(int(number));

    ret = bytes(myInts).decode()

    return ret;

def writeToFile(path:str, content:str):
    with open(path, 'w') as output:
        output.write(content)

if __name__ == '__main__':
    args = parser.parse_args()
    sourcePath = args.path
    outputPath = args.outputPath

    content = read(sourcePath);
    regexes = re.findall(byteArrayRegex, content);

    contentMod = content;

    for byteArrayContent in regexes:
       byteListEntry = byteArrayContent[0];
       elementId = extractStringFromByteListEntry(byteListEntry)
       contentMod = contentMod.replace(byteListEntry, elementId)




    if outputPath is None:
        outputPath = sourcePath

    writeToFile(outputPath, contentMod);


