#!/usr/bin/python
# -*- coding: utf-8 -*-

import pytest
import unittest
import WikiParser

#
# Tests for the verification of parsing input files..
#
class TestWikiParser(unittest.TestCase):

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

        assert self.dut.getInputFilename() == expectedFilename

