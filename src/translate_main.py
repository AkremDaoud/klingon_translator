#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Main Translation scipt

Pre-requisites:
 - Python 3.6.4
"""

import sys
import os
import logging
from optparse import OptionParser, OptionGroup, Option
import stapi
from language_def import LOG_CMN, LOG_FILE_PATH, LOGGER_NAME, CONFIG_FILE_LANG_DEF_XML, LanguageDef

__version__ = '1.0'
__updated__ = '2018-09-25'
program_description = """ Klingon language translator """


class MultipleOption(Option):
    ACTIONS = Option.ACTIONS + ("extend",)
    STORE_ACTIONS = Option.STORE_ACTIONS + ("extend",)
    TYPED_ACTIONS = Option.TYPED_ACTIONS + ("extend",)
    ALWAYS_TYPED_ACTIONS = Option.ALWAYS_TYPED_ACTIONS + ("extend",)

    def take_action(self, action, dest, opt, value, values, parser):
        if action == "extend":
            values.ensure_value(dest, []).append(value)
        else:
            Option.take_action(self, action, dest, opt, value, values, parser)

#
# main entry point
#
if __name__ == '__main__':
    PROGRAM_NAME = os.path.basename(sys.argv[0])
    PROGRAM_VERSION = "v" + __version__
    PROGRAM_BUILD_DATE = "%s" % __updated__

    PROGRAM_VERSION_STRING = '%%prog %s (%s)' % (
        PROGRAM_VERSION, PROGRAM_BUILD_DATE)
    HELP_MESSAGE = """
    %prog [Text to translate]
    """
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
    LOG_CMN.setLevel(logging.INFO)

    execution_result = 0
    argv = sys.argv[1:]
    try:
        parser = OptionParser(option_class=MultipleOption,
                              usage=HELP_MESSAGE,
                              version=PROGRAM_VERSION_STRING,
                              description=program_description)

        parser.add_option(
            "-p",
            "--path_lang_definition",
            dest="path_lang_definition",
            default=CONFIG_FILE_LANG_DEF_XML,
            help="Set path of the tables definition file. Default = ./%s ." %
            CONFIG_FILE_LANG_DEF_XML)

        group_parser = OptionGroup(parser, "Logger")

        group_parser.add_option(
            "-v",
            "--verbose",
            dest='verbose',
            action='store_const',
            const=logging.INFO,
            help="Be more verbose in letting you know what is going on."
            " Enables informational messages.")
        group_parser.add_option(
            "-V",
            "--very-verbose",
            dest='verbose',
            action='store_const',
            const=logging.DEBUG,
            help="Be very verbose in letting you know what is going on."
            " Enables debugging messages.")
        group_parser.add_option(
            "-q",
            "--quiet",
            dest='verbose',
            action='store_const',
            const=logging.ERROR,
            help="Be less verbose. Ignores warnings, only prints errors.")
        group_parser.add_option(
            "-Q",
            "--very-quiet",
            dest='verbose',
            action='store_const',
            const=logging.CRITICAL,
            help="Be much less verbose. Ignores warnings and errors."
            " Only print CRITICAL messages.")
        parser.add_option_group(group_parser)
        # process options
        (opts, others) = parser.parse_args(argv)
        if len (others) == 0 :
            # Nothing to do
            LOG_CMN.warning("No input text was specified. Nothing to do !")
        else:
            input_text = " ".join([str(e) for e in others])
            if opts.verbose:
                LOG_CMN.setLevel(opts.verbose)

            # load language 
            kinglon_lang = LanguageDef()
            if opts.path_lang_definition:
                kinglon_lang.set_path_def_lang_file(opts.path_lang_definition)
            #loafd language definition
            execution_result = kinglon_lang.load_languages_defitions()
            if execution_result == 0:
                # Parse the input message 
                execution_result, hex_text= kinglon_lang.parse_text(input_text)
                if execution_result == 0:
                    rest_client = stapi.RestClient()
                    # only for test
                    input_text = "ASMA0000012319"
                    species = rest_client.species.get(input_text)
                    #print all data
                    print (hex_text)
                    print (species.name)
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
        LOG_CMN.info("Execution succeeded")
    else:
        LOG_CMN.error("Execution failed")

    sys.exit(execution_result)
