#!/usr/bin/python
# -*- coding: utf-8 -*-


"""
  mediawiki - Translate the language of a mediawiki file.

Usage:
  mediawiki.py (--input <input-filename>|--indir <input-directory-name>) [--settings <settings-filename>] [--lang <output-languages> ] [--outdir <output-directory-name> ]
  mediawiki.py -h | --help

Options:
  --input <input-filename>            Input mediawiki file.
  --indir <input-directory-name>      Input directory that has one or more input mediawiki files in it.
  --lang <output-languages>           The name of the output target language to translate into.
  --outdir <output-directory-name>    Output directory where the translated output files are written to.
  --settings <settings-filename>      Mediawiki settings file, copy example_settings to get started. [default: settings]
  -h --help                           Show this help menu.
"""

# Parse input arguments into this script.
import docopt

# Access operating system libraries to check if file or directory exist.
import os

# Custom common data.
import WikiData

# Custom settings.
import WikiSettings

# Custom Mediawiki file package.
import WikiParser


# Non-zero error codes.
ERROR_FILE_DOES_NOT_EXIST = 1
ERROR_LANGUAGE_NOT_SUPPORTED = 2
ERROR_DIRECTORY_DOES_NOT_EXIST = 3

#
# Add a slash to the end of the directory name,
# if a slash does not already exist.
# Example:
#  'mydirectory' => 'mydirectory/'
#
def addSlashToDir(inDir):

    # Assume the out directory name is the
    # same as the input directory name,
    # until we know otherwise.
    outDir = inDir

    # Look for the slash on the end.
    if not outDir.endswith('/'):
        outDir += '/'

    return outDir


#
# Create a friendly human readable string of the currently supported languages.
#
def supportedLanguagesString():


    # Create friendly human readable string to read.
    friendlySupportedLanguages = ""

    # Sort the list of supported languages by their human readable value not their key.
    # As some languages have a weird key like Spanish='es' or German='de'
    for supportedLangKey, supportedLangVal in sorted(WikiData.SUPPORTED_LANGUAGES.iteritems(), key=lambda x: x[1]):
        # Only report the languages that we have name for otherwise we have not idea
        # what language this is.
        if supportedLangVal != "":
            friendlySupportedLanguages += supportedLangVal + "(" + supportedLangKey + ")" + ","

    # Remove the last comma off the end.
    return friendlySupportedLanguages[:-1]



#
# Translate the language of the mediawiki file.
#
def main():

    # Get the input file from the user.
    inputArgs = docopt.docopt(__doc__)

    # Deal with the settings file.
    try:
        inputLangDefault, outputLangDefault, location, projectId = WikiSettings.extractSettings(inputArgs["--settings"])
    except ValueError as exception:
        print exception
        return ERROR_FILE_DOES_NOT_EXIST

    # Add a slash to the end of the output dir if it has been provided.
    if inputArgs["--outdir"]:
        inputArgs["--outdir"] = addSlashToDir(inputArgs["--outdir"])

    # Start with the default output language from the settings file.
    multiLang = outputLangDefault.rsplit(',')

    # Build up a list of languages.
    if inputArgs["--lang"]:
        multiLang = inputArgs["--lang"].rsplit(',')

    # Build up a list of input filenames.
    multiFiles = []

    # User has asked for an output target language just need to verify it is allowed.
    for currentLang in multiLang:

        if not (currentLang in WikiData.SUPPORTED_LANGUAGES.keys()):
            print "Error: Language (" + currentLang + ") not supported."
            print "Supported are: " + str(supportedLanguagesString())
            return ERROR_LANGUAGE_NOT_SUPPORTED

    # Get a single input filename, if provided.
    if inputArgs['--input']:
        multiFiles.append(inputArgs['--input'])

    # Get several input filenames from the directory, if provided.
    if inputArgs["--indir"]:
        if not os.path.exists(inputArgs["--indir"]):
            print "Error: Input directory (" + str(inputArgs["--indir"]) + ") does not exist."
            return ERROR_DIRECTORY_DOES_NOT_EXIST

        if not os.path.isdir(inputArgs["--indir"]):
            print "Error: Input directory (" + str(inputArgs["--indir"]) + ") is not a directory."
            return ERROR_DIRECTORY_DOES_NOT_EXIST

        # Get a list of files in the dir.
        inputDir = addSlashToDir(inputArgs["--indir"])

        # Find the list of all the files in the input directory so that we can parse them one at a time.
        multiFiles = ['{0}{1}'.format(inputDir, element) for element in os.listdir(inputDir)]

    # Finally perform the translation for each input file for each language.
    try:
        for currentFile in multiFiles:
            for currentLang in multiLang:
                mediawikiParser = WikiParser.WikiParser(inputFilename = currentFile,
                                                        outputLanguage = currentLang,
                                                        inputLanguage = inputLangDefault,
                                                        location = location,
                                                        projectId = projectId,
                                                        outputDirname= inputArgs.get("--outdir", None))

                # Read and process the input file, then translate the data to the target output language.
                # Then write the translated information to the output file.
                mediawikiParser.readProcessTranslateWrite()

    except ValueError as exception:
        print exception
        return ERROR_FILE_DOES_NOT_EXIST

    # DEBUG: Report the data structure of special sequences.
    # mediawikiParser.printWikiParser()

    # End of main.
    return


#
# Main driver.
#
if __name__ == '__main__':
    main()
