class Lexeme: 
    def __init__(self,  subject, assignment, file, lastPosition = None, space = 0, charList = None,):
        self.space = space
        if charList == None:
            self.charList = []
        else:
            self.charList = charList
        self.lastPosition = lastPosition
        self.subject = subject
        self.assignment = assignment
        self.file = file

    def getSize(self): return len(self.charList)

    def getSpace(self): return self.space
    def setSpace(self, space): self.space = space
    def incrementSpace(self): self.space += 1
    def decrementSpace(self): self.space -= 1

    def getFull(self): return self.getSize() + self.space

    def printSize(self): return f"{self.getSize()}:{self.space}"

    def __add__(self, other):
        return Lexeme(
            space = other.space,
            charList = self.charList + other.charList,
            subject = self.subject,
            assignment = self.assignment,
            file = self.file
        )

    def __str__(self): 
        msg = "["
        for i, char in enumerate(self.charList):
            msg += str(char)
            if i < len(self.charList) - 1:
                msg += ", "
        msg += "]"
        return msg

    def printWord(self):
        msg = ""
        for char in self.charList:
            msg += char.getChar()
        return msg
    
    def printSize(self):
        return f"{self.getSize()}:{self.space}"
    
    def getChar(self, index):
        return self.charList[index]
    
    def getCharList(self):
        return self.charList
    
    def getCharListSubset(self, start=None, end=None):
        if end == None:
            return self.charList[start:]
        elif start == None:
            return self.charList[:end]
        return self.charList[start:end]
    
    def insertChar(self, sum, row, location, char, index):
        self.charList.insert(sum, LexemeChar(
            row,
            location,
            char,
            index
        ))
    
    def deleteChar(self, sum, row, index):
        self.charList[sum].delete(row, index)
        self.charList.pop(sum)

    def getSaved(self):
        saved = True
        for char in self.charList:
            saved = saved and char.getSaved()
            if saved == False: break
        return saved

    def save(self):
        for char in self.charList:
            char.save()

    def getFileDesc(self):
        return f"{self.subject} {self.assignment} {self.file}"
    
    def getDict(self):   
        deleteList = []     
        for char in self.charList:
            if char.deleteRow != None:
                deleteList.append(char.deleteRow)
        if len(deleteList) == 0:
            deleteRow = None
        else:
            deleteRow = min(deleteList)
        dictionary = {
            'deleteRow': deleteRow,
            'subject': self.subject,
            'assignment': self.assignment,
            'file': self.file,
            'masked': False,
            'lastPosition': self.lastPosition
        }
        return dictionary


class LexemeChar:
    def __init__(self, row, location, char, index):
        self.row = row
        self.location = location
        self.char = char
        self.index = index
        self.saved = False
        self.deleteRow = None
        self.deleteIndex = None
        self.deleted = False
        self.masked = False
        self.maskedChar = None

    def getRow(self): return self.row

    def getLocation(self): return self.location

    def getChar(self): return self.char

    def __str__(self): return f"{self.row}.{self.location}"

    def getSaved(self): return self.saved

    def save(self): self.saved = True

    def getInsertLocation(self): return self.row, self.index

    def isDeleted(self): return self.deleted

    def delete(self, row, index):
        self.deleteRow = row
        self.deleteIndex = index
        self.deleted = True

    def getDeleteLocation(self):
        if self.deleted == False:
            return None, None
        else:
            return self.deleteRow, self.deleteIndex
        
    def getMasked(self):
        return self.masked
    
    def mask(self, maskedChar):
        self.masked = True
        self.maskedChar = maskedChar

    def getMaskedChar(self):
        return self.maskedChar
    