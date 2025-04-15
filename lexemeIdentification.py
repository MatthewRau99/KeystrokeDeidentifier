import pandas as pd
import json
import argparse
import pickle

from Modules.utilFunctions import wordsDict
from Modules.findWords import findAllWords

parser = argparse.ArgumentParser(
    prog='LexemeIdentification',
    description=''
)
parser.add_argument('filename')
parser.add_argument('-o', '--output')
parser.add_argument('-k', '--keywords')

args = parser.parse_args()

keystrokesFile = args.filename
outputFile = args.output if args.output is not None else "out"
keywordsFile = args.keywords

keywords = set()

with open(r'Modules/keywords.txt', 'r') as fp:
    for line in fp:
        x = line[:-1]
        keywords.add(x)
for i in range(0, 100):
    keywords.add(str(i))
if keywordsFile is not None:
    try:
        with open(rf'{keywordsFile}', 'r') as fp:
            for line in fp:
                x = line.strip()
                keywords.add(x)
    except:
        pass

keystrokes = pd.read_csv(keystrokesFile,
                        #  dtype = {
                        #      "EventID":int,
                        #      "SubjectID":str,
                        #      "AssignmentID":str,
                        #      "CodeStateSection":str,
                        #      "EventType":str,
                        #      "SourceLocation":float,
                        #      "EditType":str,
                        #      "InsertText":str,
                        #      "DeleteText":str,
                        #      "ClientTimestamp":float,
                        #      "X-Metadata":str,
                        #      "X-Compilable":int,
                        #      "ToolInstances":str,
                        #      "CodeStateID":str,
                        #      "x-DND":float,
                        #      "x-CourseID":str
                        #  }
                    )

keystrokes.InsertText = keystrokes.InsertText.apply(lambda x: str(x) if x != None else x)
keystrokes.DeleteText= keystrokes.DeleteText.apply(lambda x: str(x) if x != None else x)
keystrokes.SourceLocation = keystrokes.SourceLocation.fillna(0)
keystrokes.SourceLocation = keystrokes.SourceLocation.apply(lambda x : int(x))

wordsToVerify = findAllWords(keystrokes, keywords)

with open(f'./PreprocessedData/{outputFile}.dat', 'wb') as f:
    pickle.dump(wordsToVerify, f)

temp = wordsDict(wordsToVerify)
json_str = json.dumps(temp, indent = 3)
with open(f"PreprocessedData/{outputFile}-wordsFormatted.json", "w") as outfile:
    outfile.write(json_str)

words = []
for key in wordsToVerify.keys():
    words.append(key)
temp = {"words":words}
json_str = json.dumps(temp, indent = 3)
with open(f"./PreprocessedData/{outputFile}-words.json", "w") as outfile:
    outfile.write(json_str)

subjects = {}
for subject in keystrokes.SubjectID.unique():
    subjects[str(subject)] = {}
    studentDF = keystrokes[(keystrokes.SubjectID == subject)]
    for assignment in studentDF.AssignmentID.unique():
        subjects[str(subject)][str(assignment)] = []
        assignmentDF = studentDF[(studentDF.AssignmentID == assignment)]
        for file in assignmentDF.CodeStateSection.unique():
            subjects[str(subject)][str(assignment)].append(str(file))
json_str = json.dumps(subjects, indent = 3)
with open(f"./PreprocessedData/{outputFile}-files.json", "w") as outfile:
    outfile.write(json_str)

