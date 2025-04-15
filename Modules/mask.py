from string import ascii_letters
import random

def mask(df, word, lexemeList):
    for i, char in enumerate(word):
        charList = []
        maskChar = ''
        for lexeme in lexemeList:
            charList.append(lexeme.getChar(i))
            if lexeme.getChar(i).getMasked():
                maskChar = lexeme.getChar(i).getMaskedChar()
        if maskChar == '':
            maskChar = getRandomChar()

        for char in charList:
            insertRow, insertIndex = char.getInsertLocation()
            insertText = df.loc[insertRow].InsertText
            newInsertText = str(insertText)[:insertIndex] + maskChar + str(insertText)[insertIndex + 1:]
            print(f"Insert {maskChar} at {insertIndex}: {insertText} -> {newInsertText}")
            df.at[insertRow, "InsertText"] = newInsertText

            deleteRow, deleteIndex = char.getDeleteLocation()
            # print(f"Delete {maskChar} at {deleteIndex}")
            if deleteRow != None:
                deleteText = df.loc[deleteRow].DeleteText
                newDeleteText = str(deleteText)[:deleteIndex] + maskChar + str(deleteText)[deleteIndex + 1:]
                print(f"Delete {maskChar} at {deleteIndex}: {deleteText} -> {newDeleteText}")
                df.at[deleteRow, "DeleteText"] = newDeleteText
            
            if not char.getMasked():
                char.mask(maskChar)

def getRandomChar():
    return random.choice(ascii_letters)