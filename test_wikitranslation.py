#!/usr/bin/python
# -*- coding: utf-8 -*-

# Test frame work.
import pytest
import unittest

# Perform pattern matching through regular expressions.
import re

# Custom common data.
import WikiData

# Custom Mediawiki file package.
import WikiParser

# Custom settings.
import WikiSettings

#
# Tests for the Google translation of various text sequences.
#
class TestWikiTranslation(unittest.TestCase):

    #
    # Create the Device Under Test (DUT).
    #
    def setup_method(self, method):

        # Set-up the line that you would like to test.
        self.inputLine = {"originalLine": "",
                          "translatedLine": "",
                          "lineNumber": 99,
                          "sequenceLine": "",
                          "sequences": [],
                          "usedSequenceNumbers": [],
                          "emptyLine": False}

        # Deal with the settings file.
        self.inputLangDefault, self.outputLangDefault, self.location, self.projectId = WikiSettings.extractSettings()

        # Expected outputs.
        self.expectedRawFilename = "orig_input"
        self.expectedFilename = self.expectedRawFilename + ".txt"

        # Build the Device Under Test.
        self.dut = WikiParser.WikiParser(inputFilename = self.expectedFilename,
                                         outputLanguage = self.outputLangDefault,
                                         inputLanguage = self.inputLangDefault,
                                         location = self.location,
                                         projectId = self.projectId)

    #
    # Perform any necessary clean-up.
    #
    def teardown_method(self, method):
        pass

    ##############
    # Test-Cases #
    ##############

    ##### Now lets test the translation of some simple lines ###

    def test_translate_Firefox_version(self):

        # Expected outputs.
        expectedTranslatedLine = "Version de firefox"

        # Modify test input line.
        self.inputLine["originalLine"] = "Firefox version"
        self.inputLine["sequenceLine"] = "Firefox version"

        # Run the Device Under Test.
        self.dut.translateMediaWikiLine(self.inputLine)

        assert expectedTranslatedLine.decode('utf8') == self.inputLine["translatedLine"]

    def test_translate_link_description(self):

        # Expected outputs.
        expectedTranslatedLine = "[[Find what version of Firefox you are using | Versión de Firefox]]"

        # Modify test input line.
        self.inputLine["originalLine"] = "[[Find what version of Firefox you are using|Firefox version]]"
        self.inputLine["sequenceLine"] = "[[ 123.456 |Firefox version]]"
        self.inputLine["sequences"] = [{"sequence": 123.456,
                                        "original": "Find what version of Firefox you are using",
                                        "translate": False}]
        self.inputLine["usedSequenceNumbers"] = [123.456]

        # Run the Device Under Test.
        self.dut.translateMediaWikiLine(self.inputLine)

        assert expectedTranslatedLine.decode('utf8') == self.inputLine["translatedLine"]
