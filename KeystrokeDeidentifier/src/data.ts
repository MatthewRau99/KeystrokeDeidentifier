import { Word, Instance } from './words/words'
import { Subject } from './instances/instances'

import { DataFrame, IDataFrame, ISeries } from "data-forge";
import { watch } from "@aurelia/runtime-html";


export class Edit {
    public location: number = 0;
    public insertText: string = "";
    public deleteText: string = "";

    constructor(location: number, insertText: string, deleteText: string) {
        this.location = location;
        this.insertText = insertText;
        this.deleteText = deleteText;
    }
}

export class CodeHighlight {
    public startLineNumber: number = 0;
    public startColumn: number = 0;
    public endLineNumber: number = 0;
    public endColumn: number = 0;
}

export class Data {
    public file: any;
    public filteredFile: IDataFrame;
    public codeStates: Array<string> = [""];
    public rows: Array<number> = [];

    private range = -30;

    public cachedSubjects: any = {};
    public subjectId: string;
    public assignmentId: string;
    public taskId: string;
    public word: Word;

    public playbackEnabled: boolean = false;
    public playback: number = 0;
    public code: string = "";
    public edits: Array<Edit> = [];
    public codeHighlights: Array<CodeHighlight> = [];

    public fileLoading: boolean = false;

    public combinedId: string;
    public currentInstance: number = 0;
    public instance: Instance;
    public instances: Subject[];

    constructor() {
        this.file = require("/static/correspondence.csv");
        this.fileLoaded();

        setInterval(() => {
            if (!this.playbackEnabled) return;

            if (this.playback >= this.codeStates.length - 1) return;
            this.playback += 1;
        }, 84);
    }

    public fileLoaded() {
        this.filteredFile = new DataFrame(this.file).where(row => row.EventType == "File.Edit");
        this.createFakeStudent();
        this.cacheStudentAssignments();

        this.file = null;
        this.filteredFile = null;
    }

    private createFakeStudent() {
        (this.filteredFile.where(row => row.SubjectID === null)).forEach(row => {
            row.SubjectID = "";
        });
        (this.filteredFile.where(row => row.AssignmentID === null)).forEach(row => {
            row.AssignmentID = "";
        });
        (this.filteredFile.where(row => row.TaskID === null)).forEach(row => {
            row.TaskID = "";
        });
    }

    public loadData(data) {
        const parsedData = JSON.parse(data)
        var subjectID: string;
        var assignmentID: string;
        var taskID: string;

        const rows = []

        for (const index of Object.keys(parsedData.index)) {
            if (rows.length == 0) {
                subjectID = parsedData.SubjectID[index]
                assignmentID = parsedData.AssignmentID[index]
                taskID = parsedData.CodeStateSection[index]
            }
            const row = []
            for (const key of Object.keys(parsedData)) {
                row.push(parsedData[key][index])
            }
            row.push(Number(index)) 
            rows.push(row) 
        }
        const columnNames: string[] = Object.keys(parsedData)
        columnNames.push("")
        const df = new DataFrame({columnNames: columnNames, rows: rows})

        this.cachedSubjects[subjectID][assignmentID][taskID] = df;
    }

    public updateMasked(data) {
        const parsedData = JSON.parse(data)
        const columnNames: string[] = Object.keys(parsedData)

        console.log(parsedData)
        var rows = []
        for (var i of Object.keys(parsedData['index'])) {
            const row = []
            for (const key of columnNames) {
                row.push(parsedData[key][i])
            }
            row.push(parsedData['Unnamed: 0'][i])
            rows.push(row)
        }

        columnNames.push("")
        
        const df = new DataFrame({columnNames:columnNames, rows:rows})
        // console.log(df)
        const subjectID = df.at(0).SubjectID
        const assignmentID = df.at(0).AssignmentID

        var files = {}
        for (const row of df) {
            if (!(row.CodeStateSection in files)) {
                files[row.CodeStateSection] = []
            }
            files[row.CodeStateSection].push(Object.values(row))
        }
        // console.log(this.rows)
        for (const [key, file] of Object.entries(files)) {
            if (Array.isArray(file)) {

                const taskID = key
                const filedf = new DataFrame({columnNames: columnNames, rows: file})
                
                this.cachedSubjects[subjectID][assignmentID][taskID] = filedf

                if (subjectID==this.subjectId && assignmentID== this.assignmentId && taskID==this.taskId) {
                    this.extractStudentData();
                    this.code = this.codeStates[this.playback];
                }

            
            
            }
        } 
    }

    // this will be called by the dashboard when the webpage loads
    // and we know what student to show
    public studentFileLoaded() {
        if (this.subjectId === null) return;
        if (this.assignmentId === null) return;
        if (this.taskId === null) return;

        this.extractStudentData();

        // initial file load, show first state
        this.playback = 0;
        this.playbackChanged();
    }

    private extractStudentData() {
        const selection = this.cachedSubjects[this.subjectId][this.assignmentId][this.taskId];
        console.log(selection)

        let state = "";
        this.codeStates = [];
        this.rows = [];
        this.edits = [];

        selection.forEach((row: any, eventNumber: number) => {
            let i = row.SourceLocation;

            //------------------------------------------------------------
            // Update the code reconstruction
            //------------------------------------------------------------
            let insertText = row.InsertText != null ? String(row.InsertText) : "";
            let deleteText = row.DeleteText != null ? String(row.DeleteText) : "";
            state = state.slice(0, i) + insertText + state.slice(i + deleteText.length);
            
            this.rows.push(row["index"]);
            this.codeStates.push(state);
            const edit = new Edit(i, insertText, deleteText)
            this.edits.push(new Edit(i, insertText, deleteText));
        });
    }

    private cacheStudentAssignments() {
        // TODO: HIGH PRIORITY - REMOVE OLD CACHE
        // this.cachedSubjects = {};

        // cache every student ID, but don"t fill anything in
        const students = this.filteredFile.groupBy(row => row.SubjectID);
        this.cachesubjectIds(students);
        // go through every student and cache their assignments

        students.forEach(student => {
            const assignments = student.groupBy(row => row.AssignmentID);
            this.cacheAssignmentIds(assignments);

            // go through every task and cache the df-window for that task
            //  attaching it to the respective student-assignment
            assignments.forEach(assignment => {
                const tasks = assignment.groupBy(row => row.CodeStateSection);
                this.cacheTasks(tasks);
            });
        });

    }

    private cachesubjectIds(students: ISeries) {
        const subjectIds = students
            .select(group => group.first().SubjectID)
            .inflate()
            .toArray();

        subjectIds.forEach(subjectId => this.cachedSubjects[subjectId] = {});
    }

    private cacheAssignmentIds(assignments: ISeries) {
        const assignmentIds = assignments
            .select(group => ({
                subjectId: group.first().SubjectID,
                assignmentId: group.first().AssignmentID,
            }))
            .inflate()
            .toArray();

        assignmentIds.forEach(assignment => {
            this.cachedSubjects[assignment.subjectId][assignment.assignmentId] = {}
        });
    }

    private cacheTasks(tasks: ISeries) {
        tasks.forEach(task => {
            const content = task.content.pairs[0][1];
            const subjectId = content.SubjectID;
            const assignmentId = content.AssignmentID;
            const taskId = content.CodeStateSection;

            this.cachedSubjects[subjectId][assignmentId][taskId] = task;
        });
    }

    @watch("playback")
    playbackChanged() {
        this.code = this.codeStates[this.playback];
    }

    @watch('currentInstance')
    instanceChanged() {
        this.instance = this.word.instances[this.currentInstance]
    }
}