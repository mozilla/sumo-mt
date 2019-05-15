#!/usr/bin/python
# -*- coding: utf-8 -*-

import pytest
import unittest
import WikiParser
import re

#
# Tests for the verification of parsing input files.
#
class TestWikiParser(unittest.TestCase):

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
        pass

    #
    # Perform any necessary clean-up.
    #
    def teardown_method(self, method):
        pass

    ##############
    # Test-Cases #
    ##############

    def test_invalid_inputfile_none(self):
        self.assertRaises(ValueError, WikiParser.WikiParser, None)

    def test_invalid_inputfile_empty(self):
        self.assertRaises(ValueError, WikiParser.WikiParser, "")

    def test_invalid_inputfile_emptyfile(self):
        self.assertRaises(ValueError, WikiParser.WikiParser, "empty_input.txt")

    def test_valid_inputfile_txt(self):

        # Expected outputs.
        expectedRawFilename = "orig_input"
        expectedFilename = expectedRawFilename + ".txt"

        # Build the Device Under Test.
        self.dut = WikiParser.WikiParser(expectedFilename)

        assert self.dut.mInputFilename == expectedFilename

    ##### Now lets test the parsing of some simple lines ###

    def test_template_for_not_fx67(self):

        # Expected outputs.
        expectedRawFilename = "orig_input"
        expectedFilename = expectedRawFilename + ".txt"
        expectedSequence = "\d+\-\d+"

        # Modify test input line.
        self.inputLine["originalLine"] = "{for not fx67}"

        # Build the Device Under Test.
        self.dut = WikiParser.WikiParser(expectedFilename)

        self.dut.processMediaWikiLine(self.inputLine)

        currentPattern = re.compile(expectedSequence, re.IGNORECASE)
        currentMatch = re.findall(currentPattern, self.inputLine["sequenceLine"])

        assert len(currentMatch) == 1

    def test_template_open_extensions(self):

        # Expected outputs.
        expectedRawFilename = "orig_input"
        expectedFilename = expectedRawFilename + ".txt"
        expectedSequence = "\d+\-\d+"

        # Modify test input line.
        self.inputLine["originalLine"] = "#[[Template:openextensions]]"

        # Build the Device Under Test.
        self.dut = WikiParser.WikiParser(expectedFilename)

        self.dut.processMediaWikiLine(self.inputLine)

        currentPattern = re.compile(expectedSequence, re.IGNORECASE)
        currentMatch = re.findall(currentPattern, self.inputLine["sequenceLine"])

        assert len(currentMatch) == 1

    def test_hash_star_string(self):

        # Expected outputs.
        expectedRawFilename = "orig_input"
        expectedFilename = expectedRawFilename + ".txt"
        expectedSequence = "\#\*[\s\w]+\."

        self.inputLine["originalLine"] = "#*This will open a panel where you can manage extension settings."

        # Build the Device Under Test.
        self.dut = WikiParser.WikiParser(expectedFilename)

        self.dut.processMediaWikiLine(self.inputLine)

        currentPattern = re.compile(expectedSequence, re.IGNORECASE)
        currentMatch = re.findall(currentPattern, self.inputLine["sequenceLine"])

        assert len(currentMatch) == 1

    def test_double_quotes(self):

        # Expected outputs.
        expectedRawFilename = "orig_input"
        expectedFilename = expectedRawFilename + ".txt"
        expectedSequence = "[\s\w]+\,[\s\w]+\.[\s\w]+\d+\-\d+\s*\,[\s\w]+"

        self.inputLine["originalLine"] = "Underneath the description of the extension, you will see extension settings. Next to ''Run in Private Windows'', select"

        # Build the Device Under Test.
        self.dut = WikiParser.WikiParser(expectedFilename)

        self.dut.processMediaWikiLine(self.inputLine)

        currentPattern = re.compile(expectedSequence, re.IGNORECASE)
        currentMatch = re.findall(currentPattern, self.inputLine["sequenceLine"])

        assert len(currentMatch) == 1

    def test_template_table_of_contents(self):

        # Expected outputs.
        expectedRawFilename = "orig_input"
        expectedFilename = expectedRawFilename + ".txt"
        expectedSequence = "\d+\-\d+"

        self.inputLine["originalLine"] = "__TOC__"

        # Build the Device Under Test.
        self.dut = WikiParser.WikiParser(expectedFilename)

        self.dut.processMediaWikiLine(self.inputLine)

        currentPattern = re.compile(expectedSequence, re.IGNORECASE)
        currentMatch = re.findall(currentPattern, self.inputLine["sequenceLine"])

        assert len(currentMatch) == 1

    def test_template_button(self):

        # Expected outputs.
        expectedRawFilename = "orig_input"
        expectedFilename = expectedRawFilename + ".txt"
        expectedSequence = "[\s\w]+\{\s*\d+\-\d+\s*\}[\s\w]+\."

        self.inputLine["originalLine"] = "to add a check mark and then click on the {button Okay, Got It} bar."

        # Build the Device Under Test.
        self.dut = WikiParser.WikiParser(expectedFilename)

        self.dut.processMediaWikiLine(self.inputLine)

        currentPattern = re.compile(expectedSequence, re.IGNORECASE)
        currentMatch = re.findall(currentPattern, self.inputLine["sequenceLine"])

        assert len(currentMatch) == 1

    def test_equals_string_equals(self):

        # Expected outputs.
        expectedRawFilename = "orig_input"
        expectedFilename = expectedRawFilename + ".txt"
        expectedSequence = "\d+\-\d+"

        self.inputLine["originalLine"] = "=Extensions in private windows="

        # Build the Device Under Test.
        self.dut = WikiParser.WikiParser(expectedFilename)

        self.dut.processMediaWikiLine(self.inputLine)

        currentPattern = re.compile(expectedSequence, re.IGNORECASE)
        currentMatch = re.findall(currentPattern, self.inputLine["sequenceLine"])

        assert len(currentMatch) == 1

    def test_template_slash_for(self):

        # Expected outputs.
        expectedRawFilename = "orig_input"
        expectedFilename = expectedRawFilename + ".txt"
        expectedSequence = "\d+\-\d+"

        self.inputLine["originalLine"] = "{/for}"

        # Build the Device Under Test.
        self.dut = WikiParser.WikiParser(expectedFilename)

        self.dut.processMediaWikiLine(self.inputLine)

        currentPattern = re.compile(expectedSequence, re.IGNORECASE)
        currentMatch = re.findall(currentPattern, self.inputLine["sequenceLine"])

        assert len(currentMatch) == 1

    def test_template_note(self):

        # Expected outputs.
        expectedRawFilename = "orig_input"
        expectedFilename = expectedRawFilename + ".txt"
        expectedSequence = "\d+\-\d+"

        self.inputLine["originalLine"] = "{note}"

        # Build the Device Under Test.
        self.dut = WikiParser.WikiParser(expectedFilename)

        self.dut.processMediaWikiLine(self.inputLine)

        currentPattern = re.compile(expectedSequence, re.IGNORECASE)
        currentMatch = re.findall(currentPattern, self.inputLine["sequenceLine"])

        assert len(currentMatch) == 1

    def test_template_slash_note(self):

        # Expected outputs.
        expectedRawFilename = "orig_input"
        expectedFilename = expectedRawFilename + ".txt"
        expectedSequence = "\d+\-\d+"

        self.inputLine["originalLine"] = "{/note}"

        # Build the Device Under Test.
        self.dut = WikiParser.WikiParser(expectedFilename)

        self.dut.processMediaWikiLine(self.inputLine)

        currentPattern = re.compile(expectedSequence, re.IGNORECASE)
        currentMatch = re.findall(currentPattern, self.inputLine["sequenceLine"])

        assert len(currentMatch) == 1

    def test_template_triple_quotes(self):

        # Expected outputs.
        expectedRawFilename = "orig_input"
        expectedFilename = expectedRawFilename + ".txt"
        expectedSequence = "\d+\-\d+"

        self.inputLine["originalLine"] = "'''Note:'''"

        # Build the Device Under Test.
        self.dut = WikiParser.WikiParser(expectedFilename)

        self.dut.processMediaWikiLine(self.inputLine)

        currentPattern = re.compile(expectedSequence, re.IGNORECASE)
        currentMatch = re.findall(currentPattern, self.inputLine["sequenceLine"])

        assert len(currentMatch) == 1

    def test_link_with_desription(self):

        # Expected outputs.
        expectedRawFilename = "orig_input"
        expectedFilename = expectedRawFilename + ".txt"
        expectedSequence = "\[\[\s+\d+\-\d+\s+\|Firefox\s+version\]\]"

        self.inputLine["originalLine"] = "[[Find what version of Firefox you are using|Firefox version]]"

        # Build the Device Under Test.
        self.dut = WikiParser.WikiParser(expectedFilename)

        self.dut.processMediaWikiLine(self.inputLine)

        currentPattern = re.compile(expectedSequence, re.IGNORECASE)
        currentMatch = re.findall(currentPattern, self.inputLine["sequenceLine"])

        assert len(currentMatch) == 1

    def test_image_with_tag(self):

        # Expected outputs.
        expectedRawFilename = "orig_input"
        expectedFilename = expectedRawFilename + ".txt"
        expectedSequence = "\d+\-\d+"

        self.inputLine["originalLine"] = ";[[Image:Fx67ExtensionInstall-AllowPrivate]]"

        # Build the Device Under Test.
        self.dut = WikiParser.WikiParser(expectedFilename)

        self.dut.processMediaWikiLine(self.inputLine)

        currentPattern = re.compile(expectedSequence, re.IGNORECASE)
        currentMatch = re.findall(currentPattern, self.inputLine["sequenceLine"])

        assert len(currentMatch) == 1


    def test_brackets_http(self):

        # Expected outputs.
        expectedRawFilename = "orig_input"
        expectedFilename = expectedRawFilename + ".txt"
        expectedSequence = "Mozilla\'s\s*CA\s*Certificate\s*Program\s*publishes\s*a\s*list\s*of\s*\d+\-\d+\s*which\s*contains\s*details\s*that\s*might\s*be\s*useful\s*to\s*the\s*website\s*owners\."

        self.inputLine["originalLine"] = "Mozilla's CA Certificate Program publishes a list of [https://wiki.mozilla.org/CA/Upcoming_Distrust_Actions upcoming policy actions affecting certificate authorities] which contains details that might be useful to the website owners."

        # Build the Device Under Test.
        self.dut = WikiParser.WikiParser(expectedFilename)

        self.dut.processMediaWikiLine(self.inputLine)

        currentPattern = re.compile(expectedSequence, re.IGNORECASE)
        currentMatch = re.findall(currentPattern, self.inputLine["sequenceLine"])

        assert len(currentMatch) == 1

    def test_key_directive(self):

        # Expected outputs.
        expectedRawFilename = "orig_input"
        expectedFilename = expectedRawFilename + ".txt"
        expectedSequence = "\#\s*Press\s*\d+\-\d+\s*\d+\-\d+\s*\+\s*\d+\-\d+\s*\d+\-\d+\s*\."

        self.inputLine["originalLine"] = "# Press {for mac}{key command}+{/for}{key Delete}."

        # Build the Device Under Test.
        self.dut = WikiParser.WikiParser(expectedFilename)

        self.dut.processMediaWikiLine(self.inputLine)

        currentPattern = re.compile(expectedSequence, re.IGNORECASE)
        currentMatch = re.findall(currentPattern, self.inputLine["sequenceLine"])

        assert len(currentMatch) == 1

    def test_filepath_directive(self):

        # Expected outputs.
        expectedRawFilename = "orig_input"
        expectedFilename = expectedRawFilename + ".txt"
        expectedSequence = "\#\s*Press\s*\d+\-\d+\s*\d+\-\d+\s*\+\s*\d+\-\d+\s*\."

        self.inputLine["originalLine"] = "# Press {for mac}{filepath mypath}+{/for}."

        # Build the Device Under Test.
        self.dut = WikiParser.WikiParser(expectedFilename)

        self.dut.processMediaWikiLine(self.inputLine)

        currentPattern = re.compile(expectedSequence, re.IGNORECASE)
        currentMatch = re.findall(currentPattern, self.inputLine["sequenceLine"])

        assert len(currentMatch) == 1

    def test_http_inside_a_comment(self):

        # Expected outputs.
        expectedRawFilename = "orig_input"
        expectedFilename = expectedRawFilename + ".txt"
        expectedSequence = "\s*\d+\-\d+[\s\w]+\,[\s\w]+https\:\/\/support\.mozilla\.org\/en\-US\/kb\/get\-started\-firefox\-overview\-main\-features\/discuss\/7308\s*\d+\-\d+\s*"

        self.inputLine["originalLine"] = "<!-- The next two surveys are ONLY for the US, see https://support.mozilla.org/en-US/kb/get-started-firefox-overview-main-features/discuss/7308-->"

        # Build the Device Under Test.
        self.dut = WikiParser.WikiParser(expectedFilename)

        self.dut.processMediaWikiLine(self.inputLine)

        currentPattern = re.compile(expectedSequence, re.IGNORECASE)
        currentMatch = re.findall(currentPattern, self.inputLine["sequenceLine"])

        assert len(currentMatch) == 1

    def test_http_inside_a_square_bracket(self):

        # Expected outputs.
        expectedRawFilename = "orig_input"
        expectedFilename = expectedRawFilename + ".txt"
        expectedSequence = "[\s\w]+\d+\-\d+[\s\w]+\."

        self.inputLine["originalLine"] = "to your [https://getpocket.com/ Pocket] list so you can read them whenever and wherever you want."

        # Build the Device Under Test.
        self.dut = WikiParser.WikiParser(expectedFilename)

        self.dut.processMediaWikiLine(self.inputLine)

        currentPattern = re.compile(expectedSequence, re.IGNORECASE)
        currentMatch = re.findall(currentPattern, self.inputLine["sequenceLine"])

        assert len(currentMatch) == 1

    def test_http_inside_curved_backets_with_double_quotes(self):

        # Expected outputs.
        expectedRawFilename = "orig_input"
        expectedFilename = expectedRawFilename + ".txt"
        expectedSequence = "\(\s*\d+\-\d+[\s\w]+\[\[\s*\d+\-\d+\s*\|\s*\d+\-\d+[\s\w]+\,[\s\w]+\]\]\.\)"

        self.inputLine["originalLine"] = "('''Tip:''' A secure connection will have [[How do I tell if my connection to a website is secure?#w_green-padlock|\"HTTPS\" in the address bar, along with a green lock icon]].)"

        # Build the Device Under Test.
        self.dut = WikiParser.WikiParser(expectedFilename)

        self.dut.processMediaWikiLine(self.inputLine)

        currentPattern = re.compile(expectedSequence, re.IGNORECASE)
        currentMatch = re.findall(currentPattern, self.inputLine["sequenceLine"])

        assert len(currentMatch) == 1

    def test_http_inside_double_of_single_quotes(self):

        # Expected outputs.
        expectedRawFilename = "orig_input"
        expectedFilename = expectedRawFilename + ".txt"
        expectedSequence = "[\s\w]+\,[\s\w]+\d+\-\d+[\s\w]+\."

        self.inputLine["originalLine"] = "If a login page for your favorite site is insecure, you can try and see if a secure version of the page exists by typing ''https://'' before the URL in the address bar."

        # Build the Device Under Test.
        self.dut = WikiParser.WikiParser(expectedFilename)

        self.dut.processMediaWikiLine(self.inputLine)

        currentPattern = re.compile(expectedSequence, re.IGNORECASE)
        currentMatch = re.findall(currentPattern, self.inputLine["sequenceLine"])

        assert len(currentMatch) == 1
