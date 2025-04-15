import { Data } from './data';
import { inject } from 'aurelia';


@inject(Data)
export class Main {
    private data: Data;
    private words;
    private header;
    public savingText: string = "";
    public args;

    constructor(data: Data) {
        this.words = this.words
        this.header = this.header
        this.data = data;
        window.addEventListener("keydown", this.keyPressHandler.bind(this));
    }

    dispose() {
        window.removeEventListener("keydown", this.keyPressHandler.bind(this))
    }

    async save() {
        this.savingText = "Saving..."
        const url: string = `http://localhost:8000/save`
        fetch(url).then(_ => this.savingText = "Saved")
        setTimeout(() => {
            this.savingText = "";
          }, 5000);
    }

    /*
      right-arrow - move forward one event
      left-arrow - move backward one event
      up-arrow - move forward to next checkpoint
      down-arrow - move backward to last checkpoint
      spacebar - replay
    */
    keyPressHandler(event: KeyboardEvent) {
        // Don't handle keypresses inside input fields
        //  BUT -- allow sliders to be handled
        if ((event.target as HTMLInputElement).type === "text") return;

        switch (event.key) {
            case "ArrowRight":
                if (this.data.playback >= this.data.codeStates.length - 1) break;
                this.data.playback += 1; break;

            case "ArrowLeft":
                if (this.data.playback <= 0) break;
                this.data.playback -= 1; break;

            case "ArrowUp":
                console.log(event);
                break;

            case "ArrowDown":
                console.log(event);
                break;

            case " ":
                this.data.playbackEnabled = !this.data.playbackEnabled;
                break;

            case "r":
                this.header.incrementInstance();
                break;

            case "e":
                this.header.decrementInstance();
                break;

            case "f":
                this.words.incrementPage();
                break;

            case "d":
                this.words.decrementPage();
                break;

            // If we do not want to handle the keypress, get out of here!
            default:
                return;
        }

        event.preventDefault();  // prevent handled keys from doing something else
    }
}
