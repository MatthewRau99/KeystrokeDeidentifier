import { Data } from './../data';
import { inject } from "aurelia";


export type Instance = {
    deleteRow: number,
    subject: string,
    assignment: string,
    file: string,
    finalSpot: number,
    lastPosition: number
}

export type Word = {
    word: string,
    instances: Instance[],
    instanceCount: number
}


@inject(Data)
export class Words {  
    private data: Data;
    
    private wordList: string[] = require(`./../../../PreprocessedData/${process.env.output}-wordsFormatted.json`)['wordList'];

    private page: number = 1;
    private wordsPerPage: number = 24;
    private pageCount: number = Math.ceil(this.wordList.length / this.wordsPerPage);
    private pageWords: string[] = this.wordList.slice(0,24);

    public word: Word;

    public wordsItems: HTMLElement[] = []

    constructor(data: Data) {
        this.data = data;
    }

    incrementPage() {
        if (this.page < this.pageCount) {
            this.page += 1;
            let firstWord = this.wordsPerPage * (this.page - 1);
            this.pageWords = this.wordList.slice(firstWord, firstWord + this.wordsPerPage);
        }
        this.styleWords()
    }

    decrementPage() {
        if (this.page > 1) {
            this.page -= 1;
            let firstWord = this.wordsPerPage * (this.page - 1);
            this.pageWords = this.wordList.slice(firstWord, firstWord + this.wordsPerPage);
        }
        this.styleWords()
    }

    wordClick(word: Word) {
        this.word = word
        this.data.word = word
        this.data.currentInstance = 0;
        this.updateHeader();
        
        this.styleWords()
    }

    styleWords() {
        if (this.word != null) {
            for (const word of this.wordsItems) {
                if (word == null) continue
                if (word.textContent.split(' ')[0] ==this.word.word) {
                    word.classList.add("selected")
                    word.classList.remove("unselected")
                } else {
                    word.classList.add("unselected") 
                    word.classList.remove("selected")
                }
             }
        }
    }


    
    updateHeader() {
        let instance = this.word.instances[this.data.currentInstance]


        this.data.subjectId = instance.subject;
        this.data.assignmentId = instance.assignment;
        this.data.taskId = instance.file;
        this.data.combinedId = instance.subject + instance.assignment + instance.file + this.word.word

        console.log(this.data.codeStates)
        console.log(instance)
        if (instance.deleteRow === null) {
            this.data.playback = this.data.codeStates.length - 1;
        } else {
            let playback = this.data.rows.findIndex(x => x === instance.deleteRow);
            console.log(this.data.rows)
            console.log(playback)
            this.data.playback = playback - 1;
        }
        this.data.instance = instance
    }



    
}