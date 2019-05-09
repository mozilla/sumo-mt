## Description

This script uses Google Cloud Translate API to translate mediwiki markup files.

## Requirements

### Dependencies

```
$ pip install --upgrade google-cloud-translate
```

### Google Cloud Translate set-up
[Set-up Google Cloud translate](https://cloud.google.com/translate/docs/quickstart-v3)
- Create a project
- Enable Translation API
- Create a service account with Translate permissions
- Download the private key as credentials.json in this same folder

### Settings

Rename ``settings_example`` into ``settings`` and change your project_id.

## Usage

Usage examples:

You don't need to specify a language we can just default to Spanish
``$ ./mediawiki.py --input orig_input.txt``

Specify a specific single language
```
$ ./mediawiki.py --input orig_input.txt --lang es
$ ./mediawiki.py --input orig_input.txt --lang ru
```

Specify multiple languages for a single file
```
$ ./mediawiki.py --input orig_input.txt --lang 'es,ru'
```

Or you can specify a weird language and the error message shall tell you what are supported
```
$ ./mediawiki.py --input orig_input.txt --lang unknown
```

For multiple files in a single directory and we want to generate multiple output languages.
```
$ ./mediawiki.py --dir mydir/ --lang 'ru,es'
```

## Other notes

Overview
Translate an input mediawiki file of Spanish and generate an output mediawiki file of English.
orig_input.txt -> script -> orgi_output.txt

Inputs
- input file
- Language of output file (default: Spanish)
- Language of output files can be a list of languages eg 'ru,es' would be for Russian and Spanish.
- input directory - so need to get a list of all files in that directory and then parse each one of them.

Outputs
- output file with the name of the file "myfile-es.txt' if the input is "myfile.txt"
- status
  - success (zero) or
  - failure (non-zero)


## Design

### Control Flow

1. Open and read input file
2. Parse input file into a data structure
3. Send requests to Cloud Translation to perform the language conversion
4. Create and write to output file

Error conditions
- Cannot find input file
- Empty input file
- Format of input file not valid according to mediawiki
- Unable to send requests to Cloud Translation
- Unable to create output file

Data structure(s)

List of objects
- Object
  - Line number - Line number of the input file.
  - Sequence - The unique sequence to indicate the special sequence that we don't want to translate.
  - Original - The original text (in English, say).

### Detailed Design

#### Control Flow
- Start with the parsing of the input arguments to verify them.
- Parse over the input file
- Look at one line at a time
- Look for specific patterns of interest in the input file and if they are special then remove them from the line and replace them with a unique tag.
- Then send the remaining line to Google Cloud Translate API
- Each of the special unique tags replace them with the original content
- OR some of the special unique tags we need to still translate them but just a bit of their content
- write the line to the output file

#### Data Flow
- Need to add more details here.

### Testcases

Run the local script called runTest.sh

``$ ./runTests.sh``

This local script uses the package pytest in order to run a suite of unit tests.
