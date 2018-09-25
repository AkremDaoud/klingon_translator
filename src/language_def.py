#!/usr/bin/env python

"""
Language definition

Pre-requisites:
 - Python 3.6.4
"""

import sys
import os
import logging
import datetime
from time import sleep
import xml.etree.ElementTree

CONFIG_FILE_LANG_DEF_XML = 'language_definitions.xml'
LOGGER_NAME = ("klingon_translator_%s.log" %
               datetime.datetime.now().strftime('%Y%m%d%H%M%S'))
LOG_FILE_PATH = os.path.normpath('./traces')
#
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
LOG_CMN = logging.getLogger(LOGGER_NAME)

class LanguageDef():
    """ Language defintion"""
    def __init__(self, path_lang_def_file = None):
        if path_lang_def_file is None:
            self.path_lang_def_file = None
        else:
            self.set_path_def_lang_file(path_lang_def_file)
        self.letters = {}

    def set_path_def_lang_file(self, in_path):
        """ Sets the path of the language definition file"""
        path_file = os.path.normpath(in_path)
        if(os.path.exists(path_file) == False):
            raise ValueError("Language definition file [%s] was not found !" % path_file)
        self.path_lang_def_file = path_file

    def load_languages_defitions(self):
        """ Load the language definition file content """
        ret = 0
        try:
            xml_file = xml.etree.ElementTree.parse(self.path_lang_def_file).getroot()
            for current_module in xml_file.findall('letter'):
                ascii_value = current_module.attrib['value']
                hex_value = current_module.attrib['hex_code']
                self.letters[ascii_value] = hex_value
        except xml.etree.ElementTree.ParseError as err:
            log_msg = "Unable to read the language definition file [%s]" % self.path_lang_def_file
            LOG_CMN.error(log_msg)
            log_msg = "Error description = %s" % str(err)
            LOG_CMN.error(log_msg)
            self.letters = {}
            ret = 1

        return ret

    def parse_text(self, input_text):
        """ Parse the input text message and return its hexadicimal value """
        ret = 1
        hex_text = ''
        if input_text is None or len(input_text) == 0 :
            LOG_CMN.error("Empty input text !")
            return ret, hex_text

        try:
            sorted_key = sorted(self.letters, key=len, reverse=True)
            ret = 0
            len_in_text = len (input_text)
            index = 0
            while index < len_in_text and ret == 0:
                found = False
                for key in sorted_key:
                    if len(key) + index <= len_in_text and input_text[index:(index + len(key))] == key:
                        index = index + len(key)
                        # add a space in case this is not the first code to be set
                        if len(hex_text) > 0:
                            hex_text += ' '
                        hex_text = hex_text + self.letters[key]
                        found = True
                        break
                # in case the letter was not found, try with lower key 
                if found == True:
                    continue
                for key in sorted_key:
                    if len(key) + index <= len_in_text and (input_text[index:(index + len(key))]).lower() == key.lower():
                        index = index + len(key)
                        # add a space in case this is not the first code to be set
                        if len(hex_text) > 0:
                            hex_text += ' '
                        hex_text = hex_text + self.letters[key]
                        found = True
                        break
                if found == True:
                    continue
                # Key not found : exit with error
                log_msg = "Unknow letter [%s] !!" % input_text[index]
                LOG_CMN.error(log_msg)
                log_msg = "Unable to translate the input text : [%s] !!" % input_text
                LOG_CMN.error(log_msg)
                ret = 1
                hex_text = ''

        except xml.etree.ElementTree.ParseError as err:
            log_msg = "Unable to parse input text [%s]" % input_text
            LOG_CMN.error(log_msg)
            log_msg = "Error description = %s" % str(err)
            LOG_CMN.error(log_msg)
            ret = 1
            hex_text = ''

        return ret, hex_text
