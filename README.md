## Description

This script uses Google Cloud Translate API to translate mediwiki markup files.

## Requirements

### Python version

```
$ python --version
Python 2.7.5
```

### Dependencies

```
$ pip install --upgrade google-cloud-translate
$ pip install configparser
```

### Google Cloud Translate set-up
[Set-up Google Cloud translate](https://cloud.google.com/translate/docs/quickstart-v3)
- Create a project
- Enable Translation API
- Create a service account with Translate permissions
- Download the private key as ``credentials.json`` in this same folder

### Settings

Rename ``settings_example`` into ``settings``.

## Usage

Usage examples:

You don't need to specify a language we can just default to Spanish.
```
$ ./mediawiki.py --input orig_input.txt
```

Specify a specific single language.
```
$ ./mediawiki.py --input orig_input.txt --lang es
$ ./mediawiki.py --input orig_input.txt --lang ru
```

Specify multiple languages for a single file.
```
$ ./mediawiki.py --input orig_input.txt --lang 'es,ru'
```

Or you can specify a weird language and the error message shall tell you what are supported.
```
$ ./mediawiki.py --input orig_input.txt --lang unknown
```

For multiple files in a single directory and we want to generate multiple output languages.
```
$ ./mediawiki.py --indir myinputdirectory/ --lang 'ru,es'
```

If you want to send the translated files to a different directory you can specify an outdir (note that you don't need the slash on the end of the directory names).
```
$ ./mediawiki.py --indir myinputdirectory/ --lang 'ru,es' --outdir myoutputdirectory/
```

Note that if the output directory does not already exist, then it is created.

## Other notes

### Overview
Translate an input mediawiki file of Spanish and generate an output mediawiki file of English.
orig_input.txt -> script -> orgi_output.txt

### Inputs
- input file
- Language of output file (default: Spanish)
- Language of output files can be a list of languages eg 'ru,es' would be for Russian and Spanish.
- input directory - so need to get a list of all files in that directory and then parse each one of them.
- output directory - place the translated files into the output directory.

### Outputs
- output file with the name of the file "myfile-es.txt' if the input is "myfile.txt", for a target language of es.
- status
  - success (zero) or
  - failure (non-zero)


## Design

### Control Flow

1. Open and read input file.
1. Parse input file into a data structure.
1. Process each line one at a time.
1. For each line replace special text sequences with a symbol as we may want to translate these separately.
1. Send requests to Cloud Translation to perform the language conversion.
1. Create and write to output file.

#### Error conditions
- Cannot find input file.
- Empty input file.
- Format of input file not valid according to mediawiki.
- Unable to send requests to Cloud Translation.
- Unable to create output file.

#### Data structure(s)

##### List of objects
- Object - for each line in the input file.
  - Original Line - Original line of text from the input file, in English, say.
  - Translated Line - The final translated line of text into the requested output language.
  - Line number - Line number of the input file.
  - Sequence Line - After special sequences of interest within the original line have been replaced with a special squences so that we don't want to translate these.
  - Sequences - List of the unique sequences in the current line, we may or may not want to translate individually.
  - Empty Line - Boolean true or false so that we don't ask Google to translate an empty string.

- Object - for each unique sequence for a given line.
  - sequence - This is a special sequence that looks like 123-456, say.
  - original - This is the original string before any translations.
  - translate - Boolean true or false if we would like to translate the sting or leave it in the original language.


### Detailed Design

#### Control Flow
1. Start with the parsing of the input arguments to verify them.
1. Parse over the input file.
1. Look at one line at a time.
1. Look for specific patterns of interest in the input file and if they are special then remove them from the line and replace them with a unique tag.
1. Then send the remaining line to Google Cloud Translate API.
1. Each of the special unique tags replace them with the original content.
1. OR some of the special unique tags we need to still translate them but just a bit of their content.
1. write the line to the output file.

#### Data Flow
- Need to add more details here.

### Test-cases

Run the local script called runTest.sh.

```
$ ./runTests.sh
```

This local script uses the package pytest in order to run a suite of unit tests.

#### Run a test suite

Or to run the test suite in verbose mode, for a suite of tests, you can say,

```
$ pytest -v test_wikiparser.py
```

### Run a single test-case

Or to run just a single testcase called test_filepath_directive, from the test suite TestWikiParser, in verbose mode, you can say,

```
$ pytest -v test_wikiparser.py::TestWikiParser::test_filepath_directive
```

