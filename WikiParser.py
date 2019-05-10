#!/usr/bin/python
# -*- coding: utf-8 -*-

# Access operating system libraries to check if file or directory exist.
import os

# Perform pattern matching through regular expressions.
import re

# Imports the Google Cloud client library
#from google.cloud import translate
from google.cloud import translate_v3beta1 as translate

# So we can generate some random number ranges.
import random

# Parsing of JSON file(s).
import json

# Setup environment using project settings.
import configparser

# Name of the project settings file.
SETTINGS_FILENAME = 'settings'
# Settings sub-section within the settings file.
SETTINGS_SECTION = 'settings'

# Local parser to process the project settings.
parser = configparser.ConfigParser()
dataset = parser.read(SETTINGS_FILENAME)

# Verify that the user has set up their settings environment.
if len(dataset) != 1:
    errMsg = "Error: Missing settings file (" + SETTINGS_FILENAME
    errMsg += ") copy settings_example to " + SETTINGS_FILENAME
    raise ValueError(errMsg)

section = parser[SETTINGS_SECTION]

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = section['GOOGLE_APPLICATION_CREDENTIALS']
DEFAULT_INPUT_LANGUAGE = section['DEFAULT_INPUT_LANGUAGE']
DEFAULT_OUTPUT_LANGUAGE = section['DEFAULT_OUTPUT_LANGUAGE']
location = section['location']

# Verify that the credentials file exists.
if not os.path.exists(section['GOOGLE_APPLICATION_CREDENTIALS']):
    errMsg = "Error: Missing input settings Google App Credentials file ("
    errMsg += section['GOOGLE_APPLICATION_CREDENTIALS'] + ")"
    raise ValueError(errMsg)

# Get the Google Cloud Project ID from the private key credentials file.
with open(section['GOOGLE_APPLICATION_CREDENTIALS'], 'r') as googleCredentialsFile:

    # Parse the credential's JSON file into dictionary.
    googleCredentialsJson = json.load(googleCredentialsFile)

# Google Application Project ID.
project_id = googleCredentialsJson['project_id']

class WikiParser(object):

    listOfUsedNumbers = []

    # Constructor.
    # Default Language is used if nothing specified.
    def __init__(self, inputFilename, outputLanguage=DEFAULT_OUTPUT_LANGUAGE, inputLanguage=DEFAULT_INPUT_LANGUAGE):

        # Check the input arguments.
        if not inputFilename:
            raise ValueError('Error: Invalid input filename.')

        if not os.path.exists(inputFilename):
            raise ValueError("Error: Input file (" + inputFilename + ") does not exist.")

        if not os.path.isfile(inputFilename):
            raise ValueError("Error: Input file (" + inputFilename + ") is not a file.")

        if os.path.getsize(inputFilename) <= 0:
            raise ValueError("Error: Input file (" + inputFilename + ") is empty.")

        if outputLanguage == inputLanguage:
            raise ValueError("Error: Input Language (" + inputLanguage + ") same as output Language (" + outputLanguage + ")")

        # Extract the raw input filename and its extension.
        rawInputFilename, inputFilenameExtension = os.path.splitext(inputFilename)

        # Construct the output filename.
        self.mOutputFilename = rawInputFilename + '-' + outputLanguage + inputFilenameExtension

        # Keep track of the input filename.
        self.mInputFilename = inputFilename

        # Main data structure is a list of objects.
        self.mMedia = []

        # Get a file handle to the input mediawiki file.
        self.mInputFileFh = open(inputFilename, 'r')

        # Need the output language
        self.mInputLanguage = inputLanguage
        self.mOutputLanguage = outputLanguage

        # Get a file handle to the output mediawiki file.
        self.mOutputFileFh = open(self.mOutputFilename, 'w')

        # Instantiates a translation client.
        self.mTranslateClient = translate.TranslationServiceClient()
        self.mParent = self.mTranslateClient.location_path(project_id, location)

        # Parse the Mediawiki file and load into our data structure.
        self.parseMediaWikiFile()


    #
    # Create a unique random sequence.
    #
    def giveMeUniqueRandomNumber(self):

        bottomRange = 100
        topRange    = 999

        # Create an initial random number in the range.
        currentRandomNumber = str(random.randrange(bottomRange,topRange)) + "-" + str(random.randrange(bottomRange,topRange))

        # If that number has already been used then pick another one.
        while currentRandomNumber in WikiParser.listOfUsedNumbers:
            # Generate another random number in the range.
            currentRandomNumber = str(random.randrange(bottomRange,topRange)) + "-" + str(random.randrange(bottomRange,topRange))

        # Keep track that this number has been used.
        WikiParser.listOfUsedNumbers.append(currentRandomNumber)

        # Returned the special unique number.
        return currentRandomNumber


    #
    # Parse the Mediawiki input file and store into a data structure.
    #
    def parseMediaWikiFile(self):

        # Keep track of the line counter.
        # First line starts at number one.
        lineCounter = 1

        # Loop through the input file and build an internal data structure.
        for currentLine in self.mInputFileFh.readlines():

            # Gobble the end of line character.
            currentLine = currentLine.rstrip()

            # Verify we are not processing an empty line.
            if not currentLine:
                # Write a new line to the output file.
                self.mOutputFileFh.write("\n")

                # Keep track of the current line we are parsing.
                lineCounter = lineCounter + 1

                # Don't process any further as this line is empty.
                continue


            # Look for any special strings in the line and then replace it with a special number
            # Then we can replace the special number later.
            patternsToReplaceOrTranslate = [{"pattern":"(\{for[\s\w\-\_\.\,\'\’\=]+\})",
                                             "translate": False},
                                            {"pattern":"(\{\/for\})",
                                             "translate": False},
                                            {"pattern":"\{(button[\s\w\-\_\.\,\'\’\=]+)\}",
                                             "translate": False},
                                            {"pattern":"\{(menu[\s\w\-\_\.\,\'\’\=]+)\}",
                                             "translate": False},
                                            {"pattern":"(\{note\})",
                                             "translate": False},
                                            {"pattern":"(\{\/note\})",
                                             "translate": False},
                                            {"pattern":"(\{warning\})",
                                             "translate": False},
                                            {"pattern":"(\{\/warning\})",
                                             "translate": False},
                                            {"pattern":"\_\_TOC\_\_",
                                             "translate": False},
                                            {"pattern":"\_\_FORCETOC\_\_",
                                             "translate": False},
                                            {"pattern":"\_\_NOTOC\_\_",
                                             "translate": False},
                                            {"pattern":"\[\[Template\:[\w+\s]+\]\]",
                                             "translate": False},
                                            {"pattern":"\;*\[\[Image\:[\w\-\s\=\/\|]+\]\]",
                                             "translate": False},
                                            {"pattern":"\[\[Video\:[\w\s\:\/\.\_]+\]\]",
                                             "translate": False},
                                            {"pattern":"\[\[([\s\w\-\_\#\,\"]+)\|[\w\s]+\]\]",
                                             "translate": False},
                                            {"pattern":"\[\[T\:[\w\s\-\|\=\_]+\]\]",
                                             "translate": False},
                                            {"pattern":"\[\[[\s\w\-\_\#\,\"\/\.\?]+\]\]",
                                             "translate": False},
                                            {"pattern":"\-\-\-\-",
                                             "translate": False},
                                            {"pattern":"\<\!\-\-",
                                             "translate": False},
                                            {"pattern":"\-\-\>",
                                             "translate": False},
                                            {"pattern":"\<br\ \>",
                                             "translate": False},

                                            #############################
                                            {"pattern":"\(([\s\w]+)\)",
                                             "translate": True},
                                            {"pattern":"\=([\s\w]+)\=",
                                             "translate": True},
                                            {"pattern":"\[\[[\s\d]+\|([\w\s]+)\]\]",
                                             "translate": True},
                                            {"pattern":"(\'\'\'[\s\w\-\_\#\,\"\.\?\:\>\<]+\'\'\')",
                                             "translate": True},
                                            {"pattern":"(\'\'[\s\w\-\_\#\,\"\.\?\:\>\<]+\'\')",
                                             "translate": True},
                                            #################################
                                            {"pattern":"(\"[\s\w\-\_\#\,\.\?\:\>\<]+\")",
                                             "translate": True},
            ]


            # Patterns we want to replace with a special unique tag then we can put it back after
            # into the final translation.
            for replacePattern in patternsToReplaceOrTranslate:

                currentPattern = re.compile(replacePattern["pattern"], re.IGNORECASE)
                currentMatch = re.findall(currentPattern, currentLine)

                if currentMatch:
                    # Deal with multiple matches on the same line.
                    for elementMatch in currentMatch:

                        specialSequence = str(self.giveMeUniqueRandomNumber())
                        currentLine = currentLine.replace(elementMatch, " " + specialSequence + " ")

                        # Store this match so we can refer to it later.
                        self.mMedia.append({"line": lineCounter,
                                            "sequence": specialSequence,
                                            "original": elementMatch,
                                            "translate": replacePattern["translate"]})

            # Translates some text into Spanish 'espanol = es' as default.
            response = self.mTranslateClient.translate_text(parent=self.mParent,
                                                            contents=[currentLine],
                                                            mime_type='text/html',
                                                            source_language_code=self.mInputLanguage,
                                                            target_language_code=self.mOutputLanguage)
            currentLineTranslated = ""
            for currentTanslation in response.translations:
                currentLineTranslated = currentTanslation.translated_text
                break

            # Now I need to replace each of the special sequences.
            # Look through all the special sequences we have discovered so far.
            for currentMedia in self.mMedia:
                # Is this the line we are currently looking at?
                if currentMedia['line'] == lineCounter:
                    # Get it back to its original form.
                    if currentMedia['translate']:

                        response = self.mTranslateClient.translate_text(parent=self.mParent,
                                                                        contents=[currentMedia['original']],
                                                                        mime_type='text/plain',
                                                                        source_language_code=self.mInputLanguage,
                                                                        target_language_code=self.mOutputLanguage)

                        specialTranslated = ""

                        for currentTanslation in response.translations:
                            specialTranslated = currentTanslation.translated_text
                            break

                        currentLineTranslated = currentLineTranslated.replace(str(currentMedia['sequence']),
                                                                              specialTranslated.rstrip())
                    else:
                        currentLineTranslated = currentLineTranslated.replace(str(currentMedia['sequence']),
                                                                              currentMedia['original'].decode('utf8'))

            # Final clean up for "= something =" change to "=something="
            # Clean up the spaces that are inbetween links and discrptions.
            patternsToCleanup = {"^\#\s+": "#",
                                 "^\#\s*\*\s*": "#*",
                                 "^\*\s+": "*",
                                 "^\=\s+": "=",
                                 "^\s*": "",
                                 "\s+\=$": "=",
                                 "\s*\|\s*": "|",
            }

            # Clean up some patterns.
            for cleanupPattern, cleanupSub in patternsToCleanup.iteritems():

                currentPattern = re.compile(cleanupPattern, re.IGNORECASE)
                currentMatch = re.findall(currentPattern, currentLineTranslated)

                if currentMatch:
                    for elementMatch in currentMatch:
                        currentLineTranslated = re.sub(re.escape(elementMatch), cleanupSub, currentLineTranslated)


            # Write the current translated line to the output file.
            self.mOutputFileFh.write(currentLineTranslated.encode('utf8') + "\n")

            # Keep track of the current line we are parsing.
            lineCounter = lineCounter + 1

        # Keep track of the number of lines parsed in the input file.
        self.mLinecount = lineCounter

        self.mOutputFileFh.close()

    #
    #  Helpful to better understand what is inside the data scructure.
    #
    def printWikiParser(self, depth=0):

        print "###"
        print "# Filename:\t" + str(self.mInputFilename)
        for currentElement in self.mMedia:
            print "\tline:\t\t" + str(currentElement["line"])
            print "\tsequence:\t\t" + str(currentElement["sequence"])
            print "\toriginal:\t\t" + str(currentElement["original"])


    # Gettas.
    def getInputFilename(self):
        return self.mInputFilename
