import { Data } from './../data';
import { parse } from 'papaparse';
import { inject } from 'aurelia';
import { watch } from '@aurelia/runtime-html';


const enum LoadingState {
    unloaded   = 'unloaded',
    loading = 'loading',
    loaded = 'loaded',
    unknown    = 'unknown',
  }

@inject(Data)
export class Header {
    private data: Data;
    private fileUpload: any;
    private sliderValue: number;

    public students: Array<string>;
    public assignments: Array<string>;
    public tasks: Array<string>;
    public word: string;
    
    private loadState: LoadingState = LoadingState.unloaded;

    private files = require(`./../../../PreProcessedData/${process.env.output}-files.json`)
    
    constructor(data: Data) {
        this.data = data;
    }

    async attached() {
        this.fileLoaded();
    
    }

    async loadData() {
        console.log(Object.keys(this.files))
        console.log('loading')
        this.loadState = LoadingState.loading
        for (const [subject, assignments] of Object.entries(this.files)) {
            this.data.cachedSubjects[subject] = {}
            for (const [assignment, files] of Object.entries(assignments)) {
                this.data.cachedSubjects[subject][assignment] = {}
                const url: string = `http://localhost:8000/loadassign?subjectId=${subject}&assignmentId=${assignment}` 
                fetch(url)
                    .then(response => response.json())
                    .then(json => {
                        this.data.updateMasked(json)
                        if (subject == Object.keys(this.files)[Object.keys(this.files).length - 1]) {
                            this.loadState = LoadingState.loaded
                        }
                    })
            }
            await new Promise(f => setTimeout(f, 1000));
        }
        console.log('loaded')
    }

    fileLoaded() {
        if (this.data.cachedSubjects === null) return;

        this.students = Object.keys(
            this.data.cachedSubjects
        );

        // re-trigger file loading
        this.data.subjectId = null;
    }

    public async maskAll(word: string) {
        for (const subject of this.data.instances) {
            for (const assignment of subject.assignments) {
                const maskUrl: string = `http://localhost:8000/maskassign/${word}?subjectId=${subject.subject}&assignmentId=${assignment.assignment}`
                fetch(maskUrl)
                    .then(response => response.json())
                    .then(json => {
                        this.data.updateMasked(json)
                    }
                )
            }
        }
    }

    public async maskAssignment( word: string, subjectId: string, assignmentId: string) {
        const maskUrl: string = `http://localhost:8000/maskassign/${word}?subjectId=${subjectId}&assignmentId=${assignmentId}`
        fetch(maskUrl)
            .then(response => response.json())
            .then(json => {
                this.data.updateMasked(json)
            })
    }

    incrementInstance() {    
        if (this.data.currentInstance < this.data.word.instances.length - 1) {
            this.data.currentInstance += 1
        }
    }

    decrementInstance() {
        if (this.data.currentInstance > 0) {
            this.data.currentInstance -= 1
        }
    }

    @watch("data.subjectId")
    newSubjectSelected() {
        if (this.data.subjectId === null) return;

        // re-trigger file loading
        this.data.assignmentId = null;
    }

    @watch("data.assignmentId")
    newAssignmentSelected() {
        if (this.data.assignmentId === null) return;

        // re-trigger file loading
        this.data.taskId = null;
    }

    @watch("data.taskId")
    newFileSelected() {
        if (this.data.taskId === null) return;

        this.sliderValue = 0;
        this.data.studentFileLoaded();
    }

    // Sometimes our playback changes without the use of the slider
    @watch("data.playback")
    dataPlaybackChanged() {
        this.sliderValue = this.data.playback;
    }


    @watch("fileUpload")
    async fileUploaded(fileList: FileList) {
        const csvConfig = {
            delimiter: ",",
            header: true,
            dynamicTyping: true,
            skipEmptyLines: true,
        }

        this.data.fileLoading = true;

        const file = fileList.item(0);
        const data = await file.text().then(data => parse(data, csvConfig));

        this.data.file = data.data;
        this.data.fileLoaded();

        this.newSubjectSelected();
        this.newAssignmentSelected();
        this.newFileSelected();
        this.fileLoaded();

        this.data.fileLoading = false;
    }

    @watch("sliderValue")
    sliderChanged() {
        this.data.playback = Number(this.sliderValue);
        this.data.playbackChanged();
    }

}
