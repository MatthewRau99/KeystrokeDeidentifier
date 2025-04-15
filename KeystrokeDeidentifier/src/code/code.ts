import { Data } from './../data';

import { inject } from "aurelia";
import { watch } from '@aurelia/runtime-html';

import * as monaco from "monaco-editor";

@inject(Data)
export class Code {
    private data: Data;

    private codeArea: HTMLElement;
    private monacoEditor;

    constructor(data: Data) {
        this.data = data;
    }

    attached() {
        this.monacoEditor = monaco.editor.create(this.codeArea, {
            value: this.data.code,
            language: process.env.language,
            automaticLayout: true,
            readOnly: true,
            minimap: { enabled: false },
        });

        /* 
            When the user selects text, grab the ICursorSelectionChangedEvent
            https://microsoft.github.io/monaco-editor/typedoc/interfaces/editor.ICursorSelectionChangedEvent.html
        */
        this.monacoEditor.onDidChangeCursorSelection((selectionEvent: monaco.editor.ICursorSelectionChangedEvent) => {
            const selection: monaco.Selection = selectionEvent.selection;
            const start = selection.getStartPosition();
            const end = selection.getEndPosition();
        });
    }

    @watch("data.code")
    @watch("data.codeHighlights")
    colorCode() {
        if (this.data.playback < 0 ) {
            console.log("Negative playback");
            return;
        }
        console.log(this.data.playback)
        const lastEdit = this.data.edits[this.data.playback];
        console.log(lastEdit)
        const { lineNumber, column } = this.monacoEditor.getModel().getPositionAt(lastEdit.location);
        console.log(`${lineNumber}, ${column}`)


        const codeHighlights: Array<any> = []
        this.data.codeHighlights.forEach(highlight => {
            codeHighlights.push({
                range: new monaco.Range(
                    highlight.startLineNumber,
                    highlight.startColumn,
                    highlight.endLineNumber,
                    highlight.endColumn
                ),
                options: {
                    isWholeLine: false,
                    className: "highlighHovered"
                }
            })
        });
        const insertEvent = {
            range: new monaco.Range(
                lineNumber,
                column,
                lineNumber,
                column + lastEdit.insertText.length
            ),
            options: {
                isWholeLine: false,
                className: "insert"
            }
        }
        const deleteEvent = {
            range: new monaco.Range(
                lineNumber,
                column - 1,
                lineNumber,
                column
            ),
            options: {
                isWholeLine: false,
                className: "delete"
            }
        }
        const highlightRow = {
            range: new monaco.Range(
                lineNumber,
                0,
                lineNumber,
                0
            ),
            options: {
                isWholeLine: true,
                className: "hightlightRow",
                marginClassName: "hightlightRow"
            }
        };
        const editEvent = lastEdit.insertText.length > 0 ? insertEvent : deleteEvent;

        this.monacoEditor.setValue(this.data.code);
        this.monacoEditor.revealPositionInCenter({ lineNumber: lineNumber, column: column });

        const combinedHighlights = codeHighlights.concat([highlightRow, editEvent])
        this.monacoEditor.createDecorationsCollection(combinedHighlights);
    }

    @watch("data.instance")
    colorNewInstance() {
        const model = this.monacoEditor.getModel()
        const position = this.data.instance.lastPosition
        var lineNum = 1
        var charCount = 0
        while (charCount + model.getLineLength(lineNum) < position) {
            charCount += model.getLineLength(lineNum) + 1
            lineNum += 1
            console.log(lineNum)
        }
        const editEvent = {
            range: new monaco.Range(
                lineNum, 
                position - charCount + 1,
                lineNum,
                position - charCount + this.data.word.word.length + 1
            ),
            options: {
                isWholeLine: false,
                className: "insert"
            }
        }
        const highlightRow = {
            range: new monaco.Range(
                lineNum, 
                0,
                lineNum,
                0
            ),
            options: {
                isWholeLine: true,
                className: "hightlightRow",
                marginClassName: "hightlightRow"
            }
        };
        this.monacoEditor.setValue(this.data.code);
        this.monacoEditor.revealPositionInCenter({ lineNumber: lineNum, column: position - charCount + 1});


        const combinedHighlights = [highlightRow, editEvent]
        this.monacoEditor.createDecorationsCollection(combinedHighlights);
    }
}
