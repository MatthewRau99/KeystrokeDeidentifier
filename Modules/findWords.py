from Modules.Lexeme import Lexeme, LexemeChar
from Modules.cummulativeSum import getCummulativeSum, getDelimiterInsertSum, getPosition
from Modules.utilFunctions import printLexemeSizes, printReport, printWordsReport

DELIMINERS = {
    " ", ",", ".", "(", ")", "[", "]", "{", "}",
    ":", ";", "\n", "\t", "#", '=', "+", '-', '*',
    "/", "~", "|", "<", ">", '"', "'", "_", "%", "!",
    '?', '\ '.strip(), '^', '&', '@', '`', '$'
}
# printInsert = True
# printDelete = True
# printSizes = True
# printEndReport = False
# printTesting = True

printInsert = False
printDelete = False
printSizes = False
printEndReport = False
printTesting = False


def insertDeliminer(lexemes, row, keystroke, position, char):
    index, sum = getDelimiterInsertSum(keystroke.SourceLocation + position, lexemes)
    if printTesting:
        print(f"Insert Delminer- Index:{index}, Sum: {sum}, char: {char}, location: {keystroke.SourceLocation + position}")
        print(f"{len(lexemes)} lexemes")


    # Insert delimiter at the end of a Lexeme    
    if sum >= lexemes[index].getSize():
        # Add a new empty Lexeme if delimiter is at the end of the file
        if lexemes[index].getSpace() == 0:
            lexemes.insert(index + 1, Lexeme(
                subject = keystroke.SubjectID,
                assignment = keystroke.AssignmentID,
                file = keystroke.CodeStateSection
            ))
        lexemes[index].incrementSpace()
    # Insert delimiter in the middle of a Lexeme, creating two Lexemes
    else:
        temp1 = lexemes[index].getCharListSubset(start = 0, end = sum)
        temp2 = lexemes[index].getCharListSubset(start = sum)
        
        tempLexeme = lexemes[index]
        lexemes[index] = Lexeme(
            space = 1, 
            charList = temp1,
            subject = keystroke.SubjectID,
            assignment = keystroke.AssignmentID,
            file = keystroke.CodeStateSection
        )
        lexemes.insert(index + 1, Lexeme(
            space = tempLexeme.getSpace(), 
            charList = temp2,
            subject = keystroke.SubjectID,
            assignment = keystroke.AssignmentID,
            file = keystroke.CodeStateSection
        ))

    if printTesting:
        print(f"{lexemes[index - 1].printWord()} {lexemes[index].printWord()} {str(lexemes[index - 1])} {str(lexemes[index])}")
        # printLexemeSizes(lexemes[index-1:index+2])
        printLexemeSizes(lexemes[index-1:])


def insertChar(lexemes, row, keystroke, position, char):
    index, sum = getCummulativeSum(keystroke.SourceLocation + position, lexemes)
    if printTesting:
        print(f"Insert Char- Index:{index}, Sum: {sum}, char: {char}, location: {keystroke.SourceLocation + position}")

    # Insert a new Lexeme if needed at the end of the file
    if index > len(lexemes) - 1:
        lexemes.append(Lexeme(
            subject = keystroke.SubjectID,
            assignment = keystroke.AssignmentID,
            file = keystroke.CodeStateSection
        ))
    # Insert character between multiple delimiters, creating a new Lexeme
    if (sum >= lexemes[index].getSize() + 1):
        firstSpace = sum - lexemes[index].getSize()
        secondSpace = lexemes[index].getSpace() - firstSpace

        lexemes[index].setSpace(firstSpace)
        lexemes.insert(index + 1, Lexeme(
            space = secondSpace, 
            charList = [LexemeChar(
                row = row, 
                location = keystroke.SourceLocation + position, 
                char = char,
                index = position)],
            subject = keystroke.SubjectID,
            assignment = keystroke.AssignmentID,
            file = keystroke.CodeStateSection
        ))
        
    # Insert character inside an existing lexeme
    else: 
        lexemes[index].insertChar(
            sum,
            row,
            keystroke.SourceLocation + position,
            char,
            position
        )
        
    if printTesting:
        print(f"{lexemes[index - 1].printWord()} {lexemes[index].printWord()}  {str(lexemes[index - 1])} {str(lexemes[index])}")
        printLexemeSizes(lexemes[index-1:])
        # printLexemeSizes(lexemes[index-1:index+2])



def saveWords(wordsToVerify, lexemes, keystroke, keywords):
    for k, char in enumerate(keystroke.DeleteText.replace("\n", " ")):
        if char not in DELIMINERS:
            index, sum = getCummulativeSum(keystroke.SourceLocation + k, lexemes)
            tempLexeme = lexemes[index]
            if not tempLexeme.getSaved() and tempLexeme.printWord() not in keywords:
                if tempLexeme.printWord() in wordsToVerify:
                    wordsToVerify[tempLexeme.printWord()].append(
                        Lexeme(
                            space = tempLexeme.getSpace(),
                            charList = tempLexeme.charList.copy(),
                            subject = tempLexeme.subject,
                            assignment = tempLexeme.assignment,
                            file = tempLexeme.file,
                            lastPosition = getPosition(tempLexeme, lexemes)
                        ))
                else:
                    wordsToVerify[tempLexeme.printWord()] = [Lexeme(
                            space = tempLexeme.getSpace(),
                            charList = tempLexeme.charList.copy(),
                            subject = tempLexeme.subject,
                            assignment = tempLexeme.assignment,
                            file = tempLexeme.file,
                            lastPosition = getPosition(tempLexeme, lexemes)
                            )]
                lexemes[index].save()
        

def saveFinalWords(wordsToVerify, lexemes, keywords):
    for lexeme in lexemes:
        if not lexeme.getSaved() and lexeme.printWord() not in keywords:
            if lexeme.printWord() in wordsToVerify:
                wordsToVerify[lexeme.printWord()].append(
                    Lexeme(
                        space = lexeme.getSpace(),
                        charList = lexeme.charList.copy(),
                        subject = lexeme.subject,
                        assignment = lexeme.assignment,
                        file = lexeme.file,
                        lastPosition = getPosition(lexeme, lexemes)
                    ))
            else:
                wordsToVerify[lexeme.printWord()] = [Lexeme(
                        space = lexeme.getSpace(),
                        charList = lexeme.charList.copy(),
                        subject = lexeme.subject,
                        assignment = lexeme.assignment,
                        file = lexeme.file,
                        lastPosition = getPosition(lexeme, lexemes)
                        )]
            lexeme.save()

def deleteDeliminer(lexemes, row, keystroke, position, char):
    index, sum = getCummulativeSum(keystroke.SourceLocation + position, lexemes)
    if printTesting:
        print(f"Delete Deliminer- Index:{index}, Sum: {sum}, char: {char}, location: {keystroke.SourceLocation + position}")

    # Delete a delimiter where there are multiple
    if lexemes[index].getSpace() > 1 or index + 1 > len(lexemes) - 1:
        lexemes[index].decrementSpace()
    # Delete the only delimiter between two Lexemes, causing them to be combined
    else: 
        lexemes[index] = lexemes[index] + lexemes[index + 1]
        lexemes.pop(index + 1)

    if printTesting:
        print(f"{lexemes[min(index, len(lexemes)-1)].printWord()}  {str(lexemes[min(index, len(lexemes)-1)])}")
        printLexemeSizes(lexemes[max(index-1,0):])
        # printLexemeSizes(lexemes[max(index-1,0):min(index+2, len(lexemes))])



def deleteChar(lexemes, row, keystroke, position, char):
    index, sum = getCummulativeSum(keystroke.SourceLocation + position, lexemes)
    if printTesting:
        print(f"Delete Char- Index:{index}, Row: {row}, Position: {position}, Charlist: {len(lexemes[index].charList)}, Sum: {sum}, char: {char}, location: {keystroke.SourceLocation + position}")

    # Delete character in a multi-character Lexeme
    if lexemes[index].getSize() > 1 or index == 0:
        lexemes[index].deleteChar(sum, row, position)
    # Delete only character in a Lexeme, removing that Lexeme and combining space with the previous Lexeme
    else:
        newSpace = lexemes[index - 1].getSpace() + lexemes[index].getSpace()
        lexemes[index].deleteChar(sum, row, position)
        lexemes[index - 1].setSpace(newSpace)
        lexemes.pop(index)
    if printTesting:
        print(f"{lexemes[max(index-1,0)].printWord()} {lexemes[min(index, len(lexemes)-1)].printWord()} {str(lexemes[max(index-1,0)])} {str(lexemes[min(index, len(lexemes)-1)])}")
        # printLexemeSizes(lexemes[max(index-1,0):min(index+2, len(lexemes))])
        printLexemeSizes(lexemes[max(index-1,0):])



def findWords(df, wordsToVerify, keywords):
    lexemes = []

    for i, keystroke in df.iterrows():
        if len(lexemes) == 0:
            lexemes.append(Lexeme(
                subject = keystroke.SubjectID,
                assignment = keystroke.AssignmentID,
                file = keystroke.CodeStateSection
            ))
        if len(keystroke.DeleteText) > 0 and keystroke.DeleteText != 'nan':
            saveWords(
                wordsToVerify,
                lexemes,
                keystroke,
                keywords
            )

            for j, char in enumerate(keystroke.DeleteText.replace("\n", " ")[::-1]):
                if char in DELIMINERS:
                    deleteDeliminer(
                        lexemes = lexemes,
                        row = i,
                        keystroke = keystroke,
                        position = len(keystroke.DeleteText) - 1 - j,
                        char = char 
                    )

                else:
                    deleteChar(
                        lexemes = lexemes,
                        row = i,
                        keystroke = keystroke,
                        position = len(keystroke.DeleteText) - 1 - j,
                        char = char 
                    )

                if printSizes:
                    printLexemeSizes(lexemes)
                if printDelete:
                    printReport(lexemes, msg= f"Delete [Line {i}, char {char}]: ")    
        if len(keystroke.InsertText) > 0 and keystroke.InsertText != 'nan':
            for j, char in enumerate(keystroke.InsertText.replace("\n", " ")):
                
                if char in DELIMINERS:
                    insertDeliminer(
                        lexemes = lexemes,
                        row = i,
                        keystroke = keystroke,
                        position = j,
                        char = char
                    )

                else: 
                    insertChar(
                        lexemes = lexemes,
                        row = i,
                        keystroke = keystroke,
                        position = j,
                        char = char,
                    )
                

                if printSizes:
                    printLexemeSizes(lexemes) 
                if printInsert:
                    printReport(lexemes, msg= f"Insert [Line {i}, char {char}]: ")                    




    saveFinalWords(wordsToVerify, lexemes, keywords)

    if printEndReport:
        printReport(lexemes)
        printLexemeSizes(lexemes)
        printReport(wordsToVerify, "Word Lexemes:")
        printWordsReport(wordsToVerify)


from alive_progress import alive_bar
def findAllWords(keystrokes, keywords):
    printInsert = False
    printDelete = False
    printSizes = False
    printEndReport = False
    printTesting = False
    wordsToVerify = {}

    filecount = len(keystrokes.groupby(['SubjectID','AssignmentID', 'CodeStateSection']))
    print(filecount)

    i = 0
    # widgets = ['Loading: ', progressbar.AnimatedMarker()]
    # bar = progressbar.ProgressBar(max_value=filecount).start()
    with alive_bar(filecount, title="Running", spinner=None) as bar:
        for subject in keystrokes.SubjectID.unique():
            # print(f"Working on {subject}")
            studentDF = keystrokes[(keystrokes.SubjectID == subject)]
            for assignment in studentDF.AssignmentID.unique():
                assignmentDF = studentDF[(studentDF.AssignmentID == assignment)]
                for file in assignmentDF.CodeStateSection.unique():
                    fileDF = assignmentDF[assignmentDF.CodeStateSection == file]
                    try:
                        findWords(fileDF, wordsToVerify, keywords)
                        i += 1
                        bar()
                    # bar.update(i)
                    #     print(f"Success: {subject}, {assignment}, {file}")
                    except Exception as error:
                        print(f"Failure: {subject}, {assignment}, {file}, {error}")

    return wordsToVerify