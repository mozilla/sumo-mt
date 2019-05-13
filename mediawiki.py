#!/usr/bin/python
# -*- coding: utf-8 -*-


"""
  mediawiki - Translate the language of a mediawiki file.

Usage:
  mediawiki.py --input <inputfilename>
  mediawiki.py --input <inputfilename> --outdir <outputDirname>
  mediawiki.py --input <inputfilename> --lang <outputlanguages>
  mediawiki.py --input <inputfilename> --lang <outputlanguages> --outdir <outputDirname>
  mediawiki.py --indir <inputDirname>
  mediawiki.py --indir <inputDirname> --outdir <outputDirname>
  mediawiki.py --indir <inputDirname> --lang <outputlanguages> --outdir <outputDirname>
  mediawiki.py -h | --help

Options:
  --input       Input mediawiki file.
  --indir       Input directory that has one or more input mediawiki files in it.
  --outdir      Output directory where the output files are written to.
  --lang        The name of the output language to translate into.
  -h --help     Show this help menu.
"""


# Parse input arguments into this script.
import docopt

# Access operating system libraries to check if file or directory exist.
import os

# Custom Mediawiki file package.
import WikiParser

# Non-zero error codes.
ERROR_FILE_DOES_NOT_EXIST = 1
ERROR_LANGUAGE_NOT_SUPPORTED = 2
ERROR_DIRECTORY_DOES_NOT_EXIST = 3

# Languages that we support.
SUPPORTED_LANGUAGES = {"af": "Afrikaans",
                       "sq": "Albanian",
                       "am": "Amharic",
                       "ar": "Arabic",
                       "hy": "Armenian",
                       "az": "Azerbaijani",
                       "eu": "Basque",
                       "be": "Belarusian",
                       "bn": "Bengali",
                       "bs": "Bosnian",
                       "bg": "Bulgarian",
                       "ca": "Catalan",
                       "ceb": "Cebuano(ISO-639-2)",
                       "zh-CN": "Chinese(Simplified)(BCP-47)",
                       "zh-TW": "Chinese(Traditional)(BCP-47)",
                       "co": "Corsican",
                       "hr": "Croatian",
                       "cs": "Czech",
                       "da": "Danish",
                       "nl": "Dutch",
                       "en": "English",
                       "eo": "Esperanto",
                       "et": "Estonian",
                       "fi": "Finnish",
                       "fr": "French",
                       "fy": "Frisian",
                       "gl": "Galician",
                       "ka": "Georgian",
                       "de": "German",
                       "el": "Greek",
                       "gu": "Gujarati",
                       "ht": "Haitian Creole",
                       "ha": "Hausa",
                       "haw": "Hawaiian(ISO-639-2)",
                       "hi": "Hindi",
                       "hmn": "Hmong(ISO-639-2)",
                       "hu": "Hungarian",
                       "is": "Icelandic",
                       "ig": "Igbo",
                       "id": "Indonesian",
                       "ga": "Irish",
                       "it": "Italian",
                       "ja": "Japanese",
                       "jw": "Javanese",
                       "kn": "Kannada",
                       "kk": "Kazakh",
                       "km": "Khmer",
                       "ko": "Korean",
                       "ku": "Kurdish",
                       "ky": "Kyrgyz",
                       "lo": "Lao",
                       "la": "Latin",
                       "lv": "Latvian",
                       "lt": "Lithuanian",
                       "lb": "Luxembourgish",
                       "mk": "Macedonian",
                       "mg": "Malagasy",
                       "ms": "Malay",
                       "ml": "Malayalam",
                       "mt": "Maltese",
                       "mi": "Maori",
                       "mr": "Marathi",
                       "mn": "Mongolian",
                       "my": "Myanmar(Burmese)",
                       "ne": "Nepali",
                       "no": "Norwegian",
                       "ny": "Nyanja(Chichewa)",
                       "ps": "Pashto",
                       "fa": "Persian",
                       "pl": "Polish",
                       "pt": "Portuguese(Portugal, Brazil)",
                       "pa": "Punjabi",
                       "ro": "Romanian",
                       "ru": "Russian",
                       "sm": "Samoan",
                       "gd": "Scots Gaelic",
                       "sr": "Serbian",
                       "st": "Sesotho",
                       "sn": "Shona",
                       "sd": "Sindhi",
                       "si": "Sinhala(Sinhalese)",
                       "sk": "Slovak",
                       "sl": "Slovenian",
                       "so": "Somali",
                       "es": "Spanish",
                       "su": "Sundanese",
                       "sw": "Swahili",
                       "sv": "Swedish",
                       "tl": "Tagalog (Filipino)",
                       "tg": "Tajik",
                       "ta": "Tamil",
                       "te": "Telugu",
                       "th": "Thai",
                       "tr": "Turkish",
                       "uk": "Ukrainian",
                       "ur": "Urdu",
                       "uz": "Uzbek",
                       "vi": "Vietnamese",
                       "cy": "Welsh",
                       "xh": "Xhosa",
                       "yi": "Yiddish",
                       "yo": "Yoruba",
                       "zu": "Zulu"
                   }

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


def supportedLanguagesString():


    # Create friendly human readable string to read.
    friendlySupportedLanguages = ""

    # Sort the list of supported languages by their human readable value not their key.
    # As some languages have a weird key like Spanish='es' or German='de'
    for supportedLangKey, supportedLangVal in sorted(SUPPORTED_LANGUAGES.iteritems(), key=lambda x: x[1]):
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

    # Add a slash to the end of the output dir if it has been provided.
    if inputArgs['--outdir']:
        inputArgs['<outputDirname>'] = addSlashToDir(inputArgs['<outputDirname>'])

    # Check for the required input argument.
    if inputArgs['--input']:
        try:
            # Parse the mediawiki file and store into a local data structure
            # Verify the language that the user has provided.
            if inputArgs['--lang']:

                multiLang = inputArgs["<outputlanguages>"].rsplit(',')

                # User has asked for an output language just need to verify it is allowed.
                for currentLang in multiLang:

                    if not (currentLang in SUPPORTED_LANGUAGES.keys()):
                        print "Error: Language (" + inputArgs["<outputlanguages>"] + ") not supported."
                        print "Supported are: " + str(supportedLanguagesString())
                        return ERROR_LANGUAGE_NOT_SUPPORTED

                    mediawikiParser = WikiParser.WikiParser(inputFilename = inputArgs['<inputfilename>'],
                                                            outputLanguage = currentLang,
                                                            outputDirname= inputArgs.get("<outputDirname>", None))
                    mediawikiParser.readProcessTranslateWrite()
            else:
                mediawikiParser = WikiParser.WikiParser(inputFilename = inputArgs['<inputfilename>'],
                                                        outputDirname= inputArgs.get("<outputDirname>", None))
                mediawikiParser.readProcessTranslateWrite()

        except ValueError as exception:
            # what was the details of the error.
            print exception
            return ERROR_FILE_DOES_NOT_EXIST


    if inputArgs['--indir']:
        if not os.path.exists(inputArgs['<inputDirname>']):
            print "Error: Input directory (" + str(inputArgs['<inputDirname>']) + ") does not exist."
            return ERROR_DIRECTORY_DOES_NOT_EXIST

        if not os.path.isdir(inputArgs['<inputDirname>']):
            print "Error: Input directory (" + str(inputArgs['<inputDirname>']) + ") is not a directory."
            return ERROR_DIRECTORY_DOES_NOT_EXIST

        # Get a list of files in the dir.
        inputDir = addSlashToDir(inputArgs['<inputDirname>'])

        # Find the list of all the files in the input directory so that we can parse them one at a time.
        listOfInputFiles =  os.listdir(inputDir)

        # Run the parser over each of the files in the sub-directory.
        for currentFile in listOfInputFiles:

            # Parse the mediawiki file and store into a local data structure
            # Verify the language that the user has provided.
            if inputArgs['--lang']:

                multiLang = inputArgs["<outputlanguages>"].rsplit(',')

                # User has asked for an output language just need to verify it is allowed.
                for currentLang in multiLang:

                    if not (currentLang in SUPPORTED_LANGUAGES.keys()):
                        print "Error: Language (" + inputArgs["<outputlanguages>"] + ") not supported."

                        print "Supported are: " + str(supportedLanguagesString())
                        return ERROR_LANGUAGE_NOT_SUPPORTED

                    mediawikiParser = WikiParser.WikiParser(inputFilename = inputDir + currentFile,
                                                            outputLanguage = currentLang,
                                                            outputDirname= inputArgs.get("<outputDirname>", None))
                    mediawikiParser.readProcessTranslateWrite()
            else:
                mediawikiParser = WikiParser.WikiParser(inputFilename = inputDir + currentFile,
                                                        outputDirname= inputArgs.get("<outputDirname>", None))
                mediawikiParser.readProcessTranslateWrite()

    # DEBUG: Report the data structure of special sequences.
    # mediawikiParser.printWikiParser()

    # End of main.
    return

#
# Main driver for Cross-Check.
#
if __name__ == '__main__':
    main()
