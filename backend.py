import pickle 
import pandas as pd
import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from Modules.mask import mask
import os
import argparse

# uvicorn backend:app
app = FastAPI()

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('filename')
    parser.add_argument('-o', '--output')
    args = parser.parse_args()

    origins = ["*"]

    app.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    filename = args.filename
    outputFile = args.output if args.output is not None else f"out"


    if os.path.isfile(f"Output/{outputFile}-masked.csv"):
        keystrokes = pd.read_csv(f"Output/{outputFile}-masked.csv", dtype={"SubjectID":str, "AssignmentID":str, "CodeStateSection":str})
    else:
        keystrokes = pd.read_csv(filename, dtype={"SubjectID":str, "AssignmentID":str, "CodeStateSection":str})
        keystrokes['index'] = keystrokes.index

    with open(f'./PreprocessedData/{outputFile}.dat','rb') as f:
        wordsToVerify = (pickle.load(f))

    @app.get("/mask/{word}")
    async def mask_word(word, subjectId: str = None, assignmentId: str = None, fileId: str = None):
        instances = wordsToVerify[word]
        if subjectId == None:
            maskInstances = instances
        else:
            maskInstances = []    
            for instance in instances:
                if instance.subject == subjectId and instance.assignment == assignmentId and instance.file == fileId:
                    maskInstances.append(instance)

        mask(keystrokes, word, maskInstances)
        
        returnvalue = keystrokes[(keystrokes.AssignmentID == assignmentId) & (keystrokes.SubjectID == subjectId) & (keystrokes.CodeStateSection == fileId)]

        print(f'Masking {word}')
        return returnvalue.to_json()

    @app.get("/maskassign/{word}")
    async def mask_word(word, subjectId: str = None, assignmentId: str = None):

        instances = wordsToVerify[word]
        if subjectId == None:
            maskInstances = instances
        else:
            maskInstances = []    
            for instance in instances:
                if instance.subject == subjectId and instance.assignment == assignmentId:
                    maskInstances.append(instance)

        mask(keystrokes, word, maskInstances)
        
        returnvalue = keystrokes[(keystrokes.AssignmentID == assignmentId) & (keystrokes.SubjectID == subjectId)]

        print(f'Masking {word}, for {subjectId}, {assignmentId}')
        return returnvalue.to_json()

    @app.get("/save")
    async def save():
        keystrokes.to_csv(f'Output/{outputFile}.csv', index=False)

    @app.get('/load')
    async def load(subjectId: str, assignmentId: str, fileId: str):
        returnvalue = keystrokes[(keystrokes.AssignmentID == assignmentId) & (keystrokes.SubjectID == subjectId) & (keystrokes.CodeStateSection == fileId)]
        return returnvalue.to_json()

    @app.get('/loadassign')
    async def loadAssign(subjectId: str, assignmentId: str):
        returnvalue = keystrokes[(keystrokes.AssignmentID == assignmentId) & (keystrokes.SubjectID == subjectId)]
        print(len(returnvalue))
        return returnvalue.to_json()


    #run server
    uvicorn.run(app)