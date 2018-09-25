#!/usr/bin/env python

"""
Main Translation scipt

Pre-requisites:
 - Python 3.6.4
"""

import sys
import os
import logging

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

from language_def import LOG_CMN, LOG_FILE_PATH, LOGGER_NAME, CONFIG_FILE_LANG_DEF_XML, LanguageDef
import string
import random


def generate_random_string_from_list(allowed_letters, string_size):
    """ Generate random string using the input allowed list"""
    ret_str = ''
    for i in range(string_size):
        ret_str += allowed_letters[random.randint(0,len(allowed_letters)-1)]
    
    return ret_str


def generate_random_string_except_list(forbidden_letters, string_size):
    """ Generate random string execpting the letters in the input forbidden list"""
    ret_str = ''
    i = 0
    while i < string_size:
        character = random.choice(string.ascii_letters + string.digits + string.punctuation)
        if character.lower() not in forbidden_letters and character.upper() not in forbidden_letters:
            ret_str += character
            i += 1
    
    return ret_str


if __name__ == '__main__':
    try:
        LOG_CMN.setLevel(logging.DEBUG)

        # load language 
        kinglon_lang = LanguageDef()
        kinglon_lang.set_path_def_lang_file('../src/%s' %CONFIG_FILE_LANG_DEF_XML)
        #loafd language definition
        execution_result = kinglon_lang.load_languages_defitions()
        if execution_result == 0:
            alphabet_klingon = kinglon_lang.letters.keys()
            # Parse the input message 
            num_iterations = random.randint(100, 1000)
            str_msg = "Number of processed iteration: [%d]" % num_iterations
            LOG_CMN.info(str_msg)
            LOG_CMN.info("** Start successfull Tests : all texts should be accepted")
            for i in range(num_iterations):
                str_msg = "--- Test %d -----" % (i + 1)
                LOG_CMN.info(str_msg)
                string_size = random.randint(1, 100)
                input_text = generate_random_string_from_list(alphabet_klingon, string_size)
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
            if execution_result == 0:
                LOG_CMN.info("** Start failed Tests : all texts should be rejected")
                for i in range(num_iterations):
                    str_msg = "--- Test %d -----" % (i + 1)
                    LOG_CMN.info(str_msg)
                    string_size = random.randint(1, 100)
                    input_text = generate_random_string_except_list(alphabet_klingon, string_size)
                    exec_ret, hex_text= kinglon_lang.parse_text(input_text)
                    if exec_ret == 1:
                        str_msg = " - Erroneous text [%s] was detected" % input_text
                        LOG_CMN.info(str_msg)
                    else:
                        str_msg = "Erroneous text [%s] was not detected" % input_text
                        LOG_CMN.error(str_msg)
                        execution_result = 1
                        break
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
