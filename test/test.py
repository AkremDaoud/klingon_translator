#!/usr/bin/env python

"""
Test script allowing to test the language parser

Prerequisites:
 - Python 3.6.4
"""

import sys
import os
import logging

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

from language_def import LOG_CMN, LOG_FILE_PATH, LOGGER_NAME, CONFIG_FILE_LANG_DEF_XML, LanguageDef
import string
import random


class LanguageTest():
    """ Language tests"""
    def __init__(self, num_iterations, alphabet_klingon):
        self.num_iterations = num_iterations
        self.alphabet_klingon = alphabet_klingon

    def generate_random_string_from_list(self, allowed_letters, string_size, add_unknown_letter=False):
        """ Generate random string using the input allowed list. 
            An unknown letter could be added at the end of the string"""
        ret_str = ''
        length_unknow = len(allowed_letters[0]) + 1
        if add_unknown_letter == False:
            size = string_size
        else:
            size = string_size - length_unknow
        for i in range(size):
            ret_str += allowed_letters[random.randint(0,len(allowed_letters)-1)]
        # Add the unknow letter
        if add_unknown_letter == True:
            i = 0
            while i < length_unknow:
                character = random.choice(string.ascii_letters + string.digits + string.punctuation)
                if character.lower() not in allowed_letters and character.upper() not in allowed_letters:
                    ret_str += character
                    i += 1
        return ret_str

    def generate_random_string_except_list(self, forbidden_letters, string_size):
        """ Generate random string execpting the letters in the input forbidden list"""
        ret_str = ''
        i = 0
        while i < string_size:
            character = random.choice(string.ascii_letters + string.digits + string.punctuation)
            if character.lower() not in forbidden_letters and character.upper() not in forbidden_letters:
                ret_str += character
                i += 1
        
        return ret_str

    def process_success_tests(self):
        """ Process successful tests : these tests are supposed to be accepted"""
        LOG_CMN.info("** Start successfull tests : all texts should be accepted")
        execution_result = 0
        for i in range(self.num_iterations):
            str_msg = "--- Test OK %d -----" % (i + 1)
            LOG_CMN.info(str_msg)
            string_size = random.randint(1, 100)
            input_text = self.generate_random_string_from_list(self.alphabet_klingon, string_size)
            exec_ret, hex_text= kinglon_lang.parse_text(input_text)
            if exec_ret == 0:
                str_msg = " - English text = [%s]" % input_text
                LOG_CMN.info(str_msg)
                str_msg = " - Hex result = [%s]" % hex_text
                LOG_CMN.info(str_msg)
            else:
                str_msg = "Unable to parse the text = [%s]" % input_text
                LOG_CMN.error(str_msg)
                execution_result = 1
                break

        return execution_result

    def process_failed_tests(self, is_random_except_one_char=False):
        """ Process failed tests : all texts should be rejected """
        LOG_CMN.info("** Start failed tests : all texts should be rejected")
        if is_random_except_one_char == False:
            trace_txt = '--- Test (KO 1)'
            LOG_CMN.info("** The whole text inculeds unknow letters.")
        else:
            trace_txt = '--- Test (KO 2)'
            LOG_CMN.info("** The text only contains one unknow letter.")

        execution_result = 0

        for i in range(self.num_iterations):
            str_msg = "%s %d -----" % (trace_txt, (i + 1))
            LOG_CMN.info(str_msg)
            string_size = random.randint(1, 100)
            if is_random_except_one_char == False:
                input_text = self.generate_random_string_except_list(self.alphabet_klingon, string_size)
            else:
                input_text = self.generate_random_string_from_list(self.alphabet_klingon, string_size, True)
            exec_ret, hex_text= kinglon_lang.parse_text(input_text)
            if exec_ret == 1:
                str_msg = " - Erroneous text [%s] was detected" % input_text
                LOG_CMN.info(str_msg)
            else:
                str_msg = "Erroneous text [%s] was not detected" % input_text
                LOG_CMN.error(str_msg)
                execution_result = 1
                break

        return execution_result


if __name__ == '__main__':
    # Set logger type
    FORMATTER = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s')

    # File handler logger
    if not os.path.exists(LOG_FILE_PATH):
        os.makedirs(LOG_FILE_PATH)
    log_file_path = os.path.normpath('%s/%s' % (LOG_FILE_PATH, LOGGER_NAME))
    HDLR_LOGGER = logging.FileHandler(log_file_path)
    HDLR_LOGGER.setFormatter(FORMATTER)
    LOG_CMN.addHandler(HDLR_LOGGER)
    LOG_CMN.setLevel(logging.DEBUG)
    execution_result = 0

    try:
        # load language 
        kinglon_lang = LanguageDef()
        kinglon_lang.set_path_def_lang_file('../src/%s' %CONFIG_FILE_LANG_DEF_XML)
        #loafd language definition
        execution_result = kinglon_lang.load_languages_defitions()
        if execution_result == 0:
            alphabet_klingon = sorted(kinglon_lang.letters, key=len, reverse=True)
            # Parse the input message 
            num_iterations = random.randint(100, 10000)
            str_msg = "Number of processed iteration: [%d]" % num_iterations
            LOG_CMN.info(str_msg)
            tests_manager = LanguageTest(num_iterations, alphabet_klingon)
            execution_result = tests_manager.process_success_tests()
            if execution_result == 0:
                execution_result = tests_manager.process_failed_tests()
                if execution_result == 0:
                    execution_result = tests_manager.process_failed_tests(True)
    except ValueError as error:
        LOG_CMN.critical(str(error))
        execution_result = 1
    except Exception as exception:
        LOG_CMN.critical(repr(exception))
        execution_result = 2
    except SystemExit as exit_val:
        if(exit_val.code != 0):
            str_msg = "Unexpected system exit: [%d]" % exit_val.code
            LOG_CMN.critical(str_msg)
        # remove the log file if empty
        HDLR_LOGGER.close()
        LOG_CMN.removeHandler(HDLR_LOGGER)
        if os.path.exists(log_file_path) and os.path.getsize(log_file_path) == 0:
            os.remove(log_file_path)
        sys.exit(exit_val.code)
    except BaseException:
        LOG_CMN.critical("Exception happened")
        execution_result = 2

    if execution_result == 0:
        LOG_CMN.info("Test execution succeeded")
    else:
        LOG_CMN.error("Test execution failed")

    sys.exit(execution_result)
