import { Data } from './../data';

import { inject } from "aurelia";
import { watch } from '@aurelia/runtime-html';
import { Word } from './../words/words'

export type Subject = {
    subject: string,
    assignments: Assignment[],
}

type Assignment = {
    assignment: string,
    files: File[],
} 

type File = {
    fileName: string,
    count: number
}


@inject(Data)
export class Instances {
    private data: Data;

    private wordList: Word[] = require(`./../../../PreprocessedData/${process.env.output}-wordsFormatted.json`)['wordList'];
    private word: Word;
    
    private instances: Subject[];

    public instanceItems: HTMLElement[] = []


    constructor(data: Data) {
        this.data = data
    }

    clickInstance(subject, assignment, file) {
        var count = 0
        for (var instance of this.word.instances) {
            if (instance.subject == subject.subject 
                && instance.assignment == assignment.assignment
                && instance.file == file.fileName) {
                break
            } else {
                count += 1
            }
        }
        this.data.currentInstance = count
        this.updateHeader()
        this.styleInstances()
    }

    @watch('data.word')
    resetInstanceItems() {
        this.instanceItems = []
    }

    @watch('data.instance')
    styleInstances() {
        for (const fileNode of this.instanceItems) {
            const assignmentNode = fileNode.parentNode.parentNode.parentNode.childNodes[1]
            const subjectNode = assignmentNode.parentNode.parentNode.parentNode.childNodes[1]
            if (fileNode.childNodes[1].textContent == this.data.instance.file &&
                assignmentNode.childNodes[1].textContent == this.data.instance.assignment &&
                subjectNode.textContent == this.data.instance.subject) {
                fileNode.classList.add("selected")
                fileNode.classList.remove("unselected")
            } else {
                fileNode.classList.add("unselected") 
                fileNode.classList.remove("selected")
            }
         }
    }

    @watch('data.currentInstance')
    updateHeader() {
        let instance = this.word.instances[this.data.currentInstance]

        this.data.subjectId = instance.subject;
        this.data.assignmentId = instance.assignment;
        this.data.taskId = instance.file;
        this.data.combinedId = instance.subject + instance.assignment + instance.file + this.word.word

        

        if (instance.deleteRow === null) {
            this.data.playback = this.data.codeStates.length - 1;
        } else {
            let playback = this.data.rows.findIndex(x => x === instance.deleteRow);
            if (playback < 0) playback = 0;
            this.data.playback = playback - 1;
        
        }
        this.data.instance = instance
        
    }

    
    @watch("data.word")
    newWord() {
        this.word = this.wordList.find(x => x.word == this.data.word.word)
        this.instances = this.mapWordInstanceToSubject(this.word)
        this.data.instances = this.instances
    }

    
    mapWordInstanceToSubject(wordInstance: Word): Subject[] {
        const uniqueSubjects = new Set<string>();
        const subjects: Subject[] = [];

        wordInstance.instances.forEach(instance => {
            if (!uniqueSubjects.has(instance.subject)) {
                uniqueSubjects.add(instance.subject);
                const newSubject: Subject = {
                    subject: instance.subject,
                    assignments: [],
                };
                subjects.push(newSubject);
            }
        });

        subjects.forEach(subject => {
            const uniqueAssignments = new Set<string>();
            wordInstance.instances
                .filter(i => i.subject === subject.subject)
                .forEach(instance => {
                    if (!uniqueAssignments.has(instance.assignment)) {
                        uniqueAssignments.add(instance.assignment);
                        const newAssignment: Assignment = {
                            assignment: instance.assignment,
                            files: [],
                        };
                        subject.assignments.push(newAssignment);
                    }

                    const assignment = subject.assignments.find(a => a.assignment === instance.assignment);
                    if (assignment) {
                        const existingFile = assignment.files.find(f => f.fileName === instance.file);
                        if (existingFile) {
                            existingFile.count += 1;
                        } else {
                            assignment.files.push({ fileName: instance.file, count: 1 });
                        }
                    }
                });
        });

        return subjects;
    }

}