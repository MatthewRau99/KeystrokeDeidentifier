import pandas as pd

def reconstruct(df):
    s = ''
    for _,row in df[df.EventType=='File.Edit'].iterrows():
        i = int(row.SourceLocation)
        insert = '' if pd.isna(row.InsertText) else row.InsertText
        delete = '' if pd.isna(row.DeleteText) else row.DeleteText
        s = s[:i] + insert + s[i+len(delete):]
    return s

def printLexemeSizes(lexemes): 
    a = ""
    for i, item in enumerate(lexemes):
        a += item.printSize() + ", "
    print(a)

def printReport(lexemes, msg = ""):
    a = msg
    for i, item in enumerate(lexemes):
        a += f"{str(item)}"
        if i < len(lexemes) - 1:
            a += ", "
    print(a)

def printWordsReport(lexemes):
    # a = "Words: "
    # for item in lexemes:
    #     a += item.printWord()
    #     a += " "
    # print(a)

    print("Words:")
    for item in lexemes:
        # print(f"{item.printWord()}: {str(item)}")
        print(f"{item}: {len(lexemes[item])}")

def wordsDict(wordsToVerify):
    dictionary = {}
    words = []

    for key, value in wordsToVerify.items():
        instances = []
        for word in value:
            instances.append(word.getDict())

        instanceCount = 0
        uniqueFiles = set()
        for instance in instances:
            fileName = str(instance['subject']) + str(instance['assignment']) + str(instance['file'])
            if fileName not in  uniqueFiles:
                instanceCount += 1
                uniqueFiles.add(fileName)

        finalSpot = None
        lastFileName = None
        for instance in instances:
            fileName = str(instance['subject']) + str(instance['assignment']) + str(instance['file'])

            if instance['deleteRow'] != None:
                finalSpot = None
            elif lastFileName == None or lastFileName != fileName or (lastFileName == fileName and finalSpot == None):
                finalSpot = 0
            else:
                finalSpot += 1
            instance['finalSpot'] = finalSpot
            lastFileName = fileName



        wordDict = {}
        wordDict["word"] = key
        wordDict["instances"] = instances
        wordDict['instanceCount'] = instanceCount
        words.append(wordDict)

    words = sorted(words, key=lambda x: x['instanceCount'])

    dictionary["wordList"] = words
    return dictionary