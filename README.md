# KeystrokeDeidentifier

KeystrokeDeidentifier is a tool for locating and masking identifiable information in keystroke data. It is implemented specifically for programming process data, but should be suitable for other forms of keystroke data.

## Setup
```
$ python3 -m pip install -r requirements.txt$
$ cd KeystrokeDeidentifier
$ npm install
```

## Preprocessing data (Lexeme Identification)
Before masking, you will need to run a python script to preprocess the data, and locate all possible words that could need masked. To do so, run the below command. This process may take a while, depending on the dataset size. 
`$ python3 lexemeIdentification.py filename [--output outfile, --keywords keywordFile]`

filename: Filepath to a csv containing keystroke data in ProgSnap2 format.
-o, --output: Project identifier, should match the identifiers used in preprocessing and the `.env` file.
-k, --keywords: Filepath to a file of keywords to be ignored by the identification algorithms. Optional.

## KeystrokeDeidentifier
The KeystrokeDeidentifier software consists of a web app and a backend server. These will be ran in seperate terminals simultaneously.

### Web App
In one terminal, navigate to `./KeystrokeDeidentifer/`

Before running the web app, define a `.env` file, following the structure of the provided `.env.example`. This defines an identifier for deidentifcation project (which should match the --output argument for the preprocessing and backend server). You will also define a programming language for syntax highlighting.

To start the web app, run
`$ npm start`

### Backend Masking Server
In a seperate terminal, run the following command.
`$ python3 backend.py filename [--output outfile]`

-o, --output: Project identifier, should match the identifiers used in preprocessing and the `.env` file.

This local server will upload the keystroke data to the web app, perform the masking of data, and save the masked data.

## Using the Web App
Upon starting the frontend web app, it should automatically navigate to the webpage. Once the backend server is running, load the keystroke data using the button at the top of the screen. 

On the left, there is a list of words found by the preprocessing script. Navigate this list using the arrow buttons, or hotkeys 'd' and 'f'. Click on one to view it in more detail. In the middle, the word will be shown in it's context, in the last keystroke it exists in full. Use the playback slider, or left and right arrows to view the surrounding keystrokes. 

The right shows all instances of this word in the whole dataset. Navigate between instances by clicking on a file in this list of instances, or use hotkeys 'e' and 'r' to navigate through consecutively.

There are two masking options, 'Mask Word' and 'Mask Assignment'. Mask Word will mask all instances of the selected word, while Mask Assignment only masks those in the same student/assignment as the currently selected instance. 

Use the blue 'Save' button in the bottom right to save any masked changes you've made. Changes are saved on the server, so restarting or refreshing the web app shouldn't lose changes. Changes are not stored automatically on server shutdown. On a save, a new csv file will be saved in the `./Output` folder. 