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


class WikiParser(object):

    # Constructor.
    # Default Language is used if nothing specified.
    def __init__(self, inputFilename, outputLanguage, inputLanguage, location, projectId, outputDirname=None):

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
            errStr = "Error: Input Language (" + inputLanguage + ")"
            errStr += " same as output Language (" + outputLanguage + ")"
            raise ValueError(errStr)

        if outputDirname is None:

            # Extract the raw input filename and its extension.
            rawInputFilename, inputFilenameExtension = os.path.splitext(inputFilename)

            # Construct the output filename.
            self.mOutputFilename = rawInputFilename + '-' + outputLanguage + inputFilenameExtension

        else:

            # Create the output directory if it does not already exist.
            if not os.path.exists(outputDirname):
                os.makedirs(outputDirname)

            # Extract the file from its current directory.
            rawInputPath, inputFilenameWithExtension = os.path.split(inputFilename)

            # Extract the raw input filename and its extension.
            rawInputFilename, inputFilenameExtension = os.path.splitext(inputFilenameWithExtension)

            self.mOutputFilename = outputDirname + rawInputFilename + '-' + outputLanguage + inputFilenameExtension

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
        self.mParent = self.mTranslateClient.location_path(projectId, location)


    #
    # Perform the work to process the data.
    #
    def readProcessTranslateWrite(self):

        # Read, process, translate and write the media wiki file.
        self.readMediaWikiFile()
        self.processMediaWikiFile()
        self.translateMediaWikiFile()
        self.writeMediaWikiFile()


    #
    # Create a unique random sequence.
    #
    def giveMeUniqueRandomNumber(self, mediaLine):

        bottomRange = 100
        topRange    = 999

        # Create an initial random number in the range.
        currentRandomNumber = str(random.randrange(bottomRange,topRange)) + "-"
        currentRandomNumber += str(random.randrange(bottomRange,topRange))

        # If that number has already been used then pick another one.
        while currentRandomNumber in mediaLine["usedSequenceNumbers"]:
            # Generate another random number in the range.
            currentRandomNumber = str(random.randrange(bottomRange,topRange)) + "-"
            currentRandomNumber += str(random.randrange(bottomRange,topRange))

        # Keep track that this number has been used.
        mediaLine["usedSequenceNumbers"].append(currentRandomNumber)

        # Returned the special unique number.
        return currentRandomNumber


    #
    # Load the media wiki file into an internal data structure.
    #
    def readMediaWikiFile(self):

        # Keep track of the line counter.
        # First line starts at number one.
        lineCounter = 1

        # Loop through the input file and build an internal data structure.
        for currentLine in self.mInputFileFh.readlines():

            # Gobble the end of line character.
            currentLine = currentLine.rstrip()

            # Verify if we are processing an empty line.
            if not currentLine:
                self.mMedia.append({"originalLine": "",
                                    "translatedLine": "",
                                    "lineNumber": lineCounter,
                                    "sequenceLine": "",
                                    "sequences": [],
                                    "usedSequenceNumbers": [],
                                    "emptyLine": True
                                })
            else:
                self.mMedia.append({"originalLine": currentLine,
                                    "translatedLine": "",
                                    "lineNumber": lineCounter,
                                    "sequenceLine": "",
                                    "sequences": [],
                                    "usedSequenceNumbers": [],
                                    "emptyLine": False
                                })

            lineCounter += 1


    #
    # Using divide and conquer approach, lets process the media wiki file to
    # smaller parts that we can translate a bit at a time.
    #
    def processMediaWikiFile(self):

        # Process one line at a time.
        for currentMedia in self.mMedia:
            if not currentMedia["emptyLine"]:
                self.processMediaWikiLine(currentMedia)


    #
    # Perform the Goole Cloud translation of the string sequences
    # that we are interested in and then recconstruct the translated
    # lines with some formatting clean-up.
    #
    def translateMediaWikiFile(self):

        # Translate one line at a time.
        for currentMedia in self.mMedia:
            if not currentMedia["emptyLine"]:
                self.translateMediaWikiLine(currentMedia)
                self.cleanupMediaWikiLine(currentMedia)


    #
    # Write out the media wiki file.
    #
    def writeMediaWikiFile(self):

        # Translate one line at a time.
        for currentMedia in self.mMedia:
            # Write the current translated line to the output file.
            self.mOutputFileFh.write(currentMedia["translatedLine"].encode('utf8') + "\n")

        self.mOutputFileFh.close()


    #
    #  Process one line at a time.
    #
    def processMediaWikiLine(self, mediaLine):

        mediaLine["sequenceLine"] = mediaLine["originalLine"]

        # Look for any special strings in the line and then replace it with a special number
        # Then we can replace the special number later.
        patternsToReplaceOrTranslate = [{"pattern":"(\{for[\s\w\-\_\.\,\'\’\=]+\})",
                                         "translate": False},
                                        {"pattern":"(\{\/for\})",
                                         "translate": False},
                                        {"pattern":"\{(button[\s\w\-\_\.\,\'\’\=]+)\}",
                                         "translate": False},
                                        {"pattern":"(\{filepath[\s\w\-\_\.\,\'\’\=]+\})",
                                         "translate": False},
                                        {"pattern":"(\{key[\s\w\-\_\.\,\'\’\=]+\})",
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
                                        {"pattern":"\[\[([\s\w\-\_\#\,\"\?]+)\|[\w\s\,\"]+\]\]",
                                         "translate": False},
                                        {"pattern":"\[\[T\:[\w\s\-\|\=\_]+\]\]",
                                         "translate": False},
                                        {"pattern":"\[\[[\:\s\w\-\_\#\,\"\/\.\?]+\\=]\]",
                                         "translate": False},
                                        {"pattern":"\[[\:\s\w\-\_\#\,\"\/\.\?\=]+\]",
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
                                        {"pattern":"(\'\'[\s\w\-\_\#\,\"\.\?\:\>\<\’]+\'\')",
                                         "translate": True},
                                        #################################
                                        {"pattern":"(\"http[\s\w\-\_\#\,\.\?\:\>\<\/]+\")",
                                         "translate": False},
                                        {"pattern":"(\"[\s\w\-\_\#\,\.\?\:\>\<\/]+\")",
                                         "translate": True},
                                        {"pattern":"(\'\'http[\s\w\-\_\#\,\.\?\:\>\<\/]+\'\')",
                                         "translate": False},
                                    ]

        # Patterns we want to replace with a special unique tag then we can put it back after
        # into the final translation.
        for replacePattern in patternsToReplaceOrTranslate:

            currentPattern = re.compile(replacePattern["pattern"], re.IGNORECASE)
            currentMatch = re.findall(currentPattern, mediaLine["sequenceLine"])

            if currentMatch:
                # Deal with multiple matches on the same line.
                for elementMatch in currentMatch:

                    specialSequence = str(self.giveMeUniqueRandomNumber(mediaLine))
                    mediaLine["sequenceLine"] = mediaLine["sequenceLine"].replace(elementMatch,
                                                                                  " " + specialSequence + " ")

                    # Store this match so we can refer to it later.
                    mediaLine["sequences"].append({"sequence": specialSequence,
                                                   "original": elementMatch,
                                                   "translate": replacePattern["translate"]})


    #
    # Perform the Google Translation on the requested line of information.
    #
    def translateMediaWikiLine(self, mediaLine):

        # Translate the sequence line.
        # Then we shall translate each of the sequences.
        # Then finally we need to replace the sequences.

        # Google Cloud Translate.
        # For the whole line we need to use html otherwise get
        # some unprintable characters in the translated string.
        response = self.mTranslateClient.translate_text(parent=self.mParent,
                                                        contents=[mediaLine["sequenceLine"]],
                                                        # Mime types: text/plain, text/html.
                                                        mime_type='text/html',
                                                        source_language_code=self.mInputLanguage,
                                                        target_language_code=self.mOutputLanguage)

        for currentTanslation in response.translations:
            mediaLine["translatedLine"] = currentTanslation.translated_text
            break

        # Reverse the list, so roll back the sequence replacements.
        for currentSequence in reversed(mediaLine["sequences"]):
            if currentSequence["translate"]:
                # Translate first, then make the substitution.
                # We can have quotes in the special substitutions so need to 
                response = self.mTranslateClient.translate_text(parent=self.mParent,
                                                                contents=[currentSequence['original']],
                                                                 # Mime types: text/plain, text/html.
                                                                mime_type='text/plain',
                                                                source_language_code=self.mInputLanguage,
                                                                target_language_code=self.mOutputLanguage)
                sequenceTranslated = ""

                for currentTanslation in response.translations:
                    sequenceTranslated = currentTanslation.translated_text
                    break

                mediaLine["translatedLine"] = mediaLine["translatedLine"].replace(str(currentSequence["sequence"]),
                                                                                  sequenceTranslated.rstrip())

            else:
                # No translation required just a substitution.
                mediaLine["translatedLine"] = mediaLine["translatedLine"].replace(str(currentSequence["sequence"]),
                                                                                  currentSequence["original"].decode('utf8'))


    #
    # When sending text to Google Translation API we need to perform some clean-up on the 
    # string that is returned due to extra white spaces that get added.
    #
    def cleanupMediaWikiLine(self, mediaLine):

        # Final clean up for "= something =" change to "=something="
        # Clean up the spaces that are in between links and discrptions.
        patternsToCleanup = {"^\#\s+": "#",
                             "^\#\s*\*\s*": "#*",
                             "^\*\s+": "*",
                             "^\=\s+": "=",
                             "^\s*": "",
                             "\s+\=$": "=",
                             "\s*\|\s*": "|",
                             "\'\'\s*\'": "'''",
                             "\'\s*\'\'": "'''",
                             "&quot;": "'",
                         }

        # Clean up some patterns.
        for cleanupPattern, cleanupSub in patternsToCleanup.iteritems():

            currentPattern = re.compile(cleanupPattern, re.IGNORECASE)
            currentMatch = re.findall(currentPattern, mediaLine["translatedLine"])

            if currentMatch:
                for elementMatch in currentMatch:
                    mediaLine["translatedLine"] = re.sub(re.escape(elementMatch),
                                                         cleanupSub,
                                                         mediaLine["translatedLine"])


    #
    #  Friendly print of the internals of the WikiParser data scructure.
    #
    def printWikiParser(self, depth=0):

        print "###"
        print "# Input Filename:\t" + str(self.mInputFilename)
        print "# Output Filename:\t" + str(self.mOutputFilename)
        print "# Input Language:\t" + str(self.mInputLanguage)
        print "# Output Language:\t" + str(self.mOutputLanguage)

        # Report the details of the sequences on this line
        for currentElement in self.mMedia:
            # Only give details for the non-empty lines in the input file.
            if not currentElement["emptyLine"]:
                print "  Original Line:"
                print "  " + str(currentElement["originalLine"])
                print "  Sequence Line:"
                print "  " + str(currentElement["sequenceLine"])
                print "  Translated Line:"
                print "  " + currentElement["translatedLine"].encode('utf8')
                if len(currentElement) > 0:
                    print "Sequences:"

                # Details about each sequence.
                for currentSequence in currentElement["sequences"]:
                    print "    " + str(currentSequence["sequence"])
                    print "    " + str(currentSequence["original"])
                    print "    " + str(currentSequence["translate"])
                    print "    " + "---"
