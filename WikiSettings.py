#!/usr/bin/python
# -*- coding: utf-8 -*-


# Setup environment using project settings.
import configparser

# Parsing of JSON file(s).
import json

# Access operating system libraries to check if file or directory exist.
import os

# Custom common data.
import WikiData

#
# Set up the environment for Media Wiki by extracting information from the settings file.
#
def extractSettings(settingsFilename='settings'):

    # Settings sub-section within the settings file.
    SETTINGS_SECTION = 'settings'
    SETTINGS_GOOGLE_APPLICATION_CREDENTIALS = 'GOOGLE_APPLICATION_CREDENTIALS'
    SETTINGS_LOCATION = 'location'
    SETTINGS_DEFAULT_INPUT_LANGUAGE = 'DEFAULT_INPUT_LANGUAGE'
    SETTINGS_DEFAULT_OUTPUT_LANGUAGE = 'DEFAULT_OUTPUT_LANGUAGE'
    SETTINGS_EXPECTED = [SETTINGS_GOOGLE_APPLICATION_CREDENTIALS,
                         SETTINGS_LOCATION,
                         SETTINGS_DEFAULT_INPUT_LANGUAGE,
                         SETTINGS_DEFAULT_OUTPUT_LANGUAGE]

    # Local parser to process the project settings.
    parser = configparser.ConfigParser()

    if not os.path.exists(settingsFilename):
        raise ValueError("Error: Settings file (" + settingsFilename + ") does not exist.")

    if not os.path.isfile(settingsFilename):
        raise ValueError("Error: Settings file (" + settingsFilename + ") is not a file.")

    if os.path.getsize(settingsFilename) <= 0:
        raise ValueError("Error: Settings file (" + settingsFilename + ") is empty.")

    # Read and parese the input settings file.
    dataset = parser.read(settingsFilename)

    # Get the part of the settings file that is under the settings section.
    if SETTINGS_SECTION in parser.keys():
        section = parser[SETTINGS_SECTION]
    else:
        errStr = "Error: Missing [" + SETTINGS_SECTION + "]"
        errStr += " section from settings file (" + settingsFilename + ")"
        raise ValueError(errStr)

    # Verify the settings we expect to see in the input settings file.
    for expectedSetting in SETTINGS_EXPECTED:
        if section.get(expectedSetting, None) is None:
            errStr = "Error: Setting (" + expectedSetting
            errStr += ") missing from settings file (" + settingsFilename + ")\n"
            raise ValueError(errStr)

    # Set up the Google API Application credentials
    os.environ[SETTINGS_GOOGLE_APPLICATION_CREDENTIALS] = section.get(SETTINGS_GOOGLE_APPLICATION_CREDENTIALS, None)
    inputLang = section.get(SETTINGS_DEFAULT_INPUT_LANGUAGE, None)
    outputLang = section.get(SETTINGS_DEFAULT_OUTPUT_LANGUAGE, None)
    location = section.get(SETTINGS_LOCATION, None)

    # Verify that the credentials file exists.
    if not os.path.exists(os.environ[SETTINGS_GOOGLE_APPLICATION_CREDENTIALS]):
        errMsg = "Error: Missing input settings Google App credentials file ("
        errMsg += os.environ[SETTINGS_GOOGLE_APPLICATION_CREDENTIALS] + ")"
        raise ValueError(errMsg)

    # Get the Google Cloud Project ID from the private key credentials file.
    with open(os.environ[SETTINGS_GOOGLE_APPLICATION_CREDENTIALS], 'r') as googleCredentialsFile:

        # Parse the credential's JSON file into dictionary.
        googleCredentialsJson = json.load(googleCredentialsFile)

    # Google Application Project ID.
    projectId = googleCredentialsJson.get('project_id', None)

    # Verify the expected settings are not empty.
    if not location:
        errStr = "Error: Setting (" +  SETTINGS_LOCATION
        errStr += ") no value set from settings file (" + settingsFilename + ")\n"
        raise ValueError(errStr)

    if not projectId:
        errStr = "Error: Project ID missing in credentials file ("
        errStr += os.environ[SETTINGS_GOOGLE_APPLICATION_CREDENTIALS] + ")"
        raise ValueError(errStr)

    # Verify the default languages in the settings.
    if not (inputLang in WikiData.SUPPORTED_LANGUAGES.keys()):
        errStr = "Error: Setting (" +  SETTINGS_DEFAULT_INPUT_LANGUAGE
        errStr += " = " + inputLang + ")"
        errStr += " not supported from settings file (" + settingsFilename + ")\n"
        errStr += "Supported are: " + str(supportedLanguagesString())
        raise ValueError(errStr)

    if not (outputLang in WikiData.SUPPORTED_LANGUAGES.keys()):
        errStr = "Error: Setting (" +  SETTINGS_DEFAULT_OUTPUT_LANGUAGE
        errStr += " = " + outputLang + ")"
        errStr += " not supported from settings file (" + settingsFilename + ")\n"
        errStr += "Supported are: " + str(supportedLanguagesString())
        raise ValueError(errStr)

    return inputLang, outputLang, location, projectId
