def getCummulativeSum(index, lexemesSizes):
    sum = 0
    returnIndex = 0
    # print(index)
    # print(f"{sum} + {lexemesSizes[returnIndex].getSize()} + {lexemesSizes[returnIndex].getSpace()}")
    maxIndex = len(lexemesSizes) - 1
    if lexemesSizes[-1].getFull() == 0:
        # print("OHHHHHHH")
        maxIndex -= 1
    while returnIndex < maxIndex and sum + lexemesSizes[returnIndex].getFull() <= index and lexemesSizes[returnIndex].getSpace() != 0:
        # print(f"{returnIndex} / {maxIndex}")
        # print(f"{lexemesSizes[returnIndex].printWord()}: {sum} + {lexemesSizes[returnIndex].getSize()} + {lexemesSizes[returnIndex].getSpace()}")        
        sum += lexemesSizes[returnIndex].getFull()
        returnIndex += 1
    # print(f"{lexemesSizes[returnIndex].printWord()}: {sum} + {lexemesSizes[returnIndex].getSize()} + {lexemesSizes[returnIndex].getSpace()}")        

    return returnIndex, index - sum

def getDelimiterInsertSum(index, lexemesSizes):
    sum = 0
    returnIndex = 0
    while returnIndex <= len(lexemesSizes) -1 and sum + lexemesSizes[returnIndex].getFull() + 1 <= index and lexemesSizes[returnIndex].getSpace() != 0:
        sum += lexemesSizes[returnIndex].getFull()
        # print(f"{sum} + {lexemesSizes[returnIndex].getSize()} + {lexemesSizes[returnIndex].getSpace()}")
        returnIndex += 1

        
    return returnIndex, index - sum

def getPosition(currLexeme, lexemes):
    sum = 0
    for lexeme in lexemes:
        if lexeme == currLexeme:
            break
        else:
            sum += lexeme.getFull()
    return sum