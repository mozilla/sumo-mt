#!/usr/bin/python
# -*- coding: utf-8 -*-

import pytest
import unittest
import WikiParser
import re

#
# Tests for the Google translation of various text sequences.
#
class TestWikiTranslation(unittest.TestCase):

    #
    # Create the Device Under Test (DUT).
    #
    def setup_method(self, method):
        pass

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
        expectedRawFilename = "orig_input"
        expectedFilename = expectedRawFilename + ".txt"
        expectedTranslatedLine = "Version de firefox"

        inputLine = {"originalLine": "Firefox version",
                     "translatedLine": "",
                     "lineNumber": 99,
                     "sequenceLine": "Firefox version",
                     "sequences": [],
                     "usedSequenceNumbers": [],
                     "emptyLine": False}

        # Build the Device Under Test.
        self.dut = WikiParser.WikiParser(expectedFilename)

        self.dut.translateMediaWikiLine(inputLine)

        assert expectedTranslatedLine.decode('utf8') == inputLine["translatedLine"]

    def test_translate_link_description(self):

        # Expected outputs.
        expectedRawFilename = "orig_input"
        expectedFilename = expectedRawFilename + ".txt"
        expectedTranslatedLine = "[[Find what version of Firefox you are using | Versión de Firefox]]"

        inputLine = {"originalLine": "[[Find what version of Firefox you are using|Firefox version]]",
                     "translatedLine": "",
                     "lineNumber": 99,
                     "sequenceLine": "[[ 123.456 |Firefox version]]",
                     "sequences": [{"sequence": 123.456,
                                    "original": "Find what version of Firefox you are using",
                                    "translate": False}],
                     "usedSequenceNumbers": [123.456],
                     "emptyLine": False}

        # Build the Device Under Test.
        self.dut = WikiParser.WikiParser(expectedFilename)

        self.dut.translateMediaWikiLine(inputLine)

        assert expectedTranslatedLine.decode('utf8') == inputLine["translatedLine"]
