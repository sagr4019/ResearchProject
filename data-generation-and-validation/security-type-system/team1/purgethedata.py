#!/usr/bin/python
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))


def main():
    all_files = list(find_files('./', '.txt'))
    for item in all_files:
        replaceContentOfFiles(item)



def replaceContentOfFiles(dataName):
    data = open(dataName)
    content = ""
    for line in data:
        newstring = replaceString(line)
        content += newstring
    data.close()

    writeDataInFile(dataName,content)

def writeDataInFile(dataName, content):
    data = open(dataName, "w")
    data.write(content)
    data.close()


def find_files(root, ext):
    for root, dirs, files in os.walk(root):
        for f in files:
            if f.lower().endswith(ext):
                f = os.path.join(root, f)
                yield f

def replaceString(string):
    tempString = string
    tempString = tempString.replace("\\n", "")
    tempString = tempString.replace('"', "")
    return tempString

if __name__ == '__main__':
    main()