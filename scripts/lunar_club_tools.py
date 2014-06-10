# -*- coding: utf-8 -*-
#------------------------------------------------------------------------------
# Copyright (c) 2012-2014, Michael Reuter
# Distributed under the MIT License. See LICENSE.txt for more information.
#------------------------------------------------------------------------------

if __name__ == '__main__':
    import argparse
    import logging
    
    _VERBOSITY_LOGLEVEL_DICT = {0: logging.ERROR, 1: logging.WARNING,
                                2: logging.INFO, 3: logging.DEBUG}
    _FILE_LOG_FORMAT = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    
    # Parse the command line optional arguments
    parser = argparse.ArgumentParser(usage='%(prog)s [option]... ')
    
    logging_group = parser.add_argument_group('logging')
    # Logging options
    logging_group.add_argument('-d', '--debug', action='store_false', 
                               help='Debug the program via logging.')
    logging_group.add_argument('-l', '--log-file', help='log file path')
    logging_group.add_argument('-v', '--verbose', action='count', default=0,
                      help='log verbosity level')

    # parse and process arguments
    args = parser.parse_args()
    
    # Setup top level logger using command line options
    logger = logging.getLogger('lct')
    file_formatter = logging.Formatter(_FILE_LOG_FORMAT)
    #temporary_stderr_handler = logging.StreamHandler()
    #temporary_stderr_handler.setFormatter(file_formatter)
    #logger.addHandler(temporary_stderr_handler)
    if args.log_file is not None:
        import os
        log_filename = os.path.expandvars(os.path.expanduser(args.log_file))
        file_handler = logging.FileHandler(log_filename)
        file_handler.setFormatter(file_formatter)
        logger.addHandler(file_handler)
    else:
        stream_handler = logging.StreamHandler()
        stream_handler.setFormatter(file_formatter)
        logger.addHandler(stream_handler)
    if args.verbose in _VERBOSITY_LOGLEVEL_DICT:
        logger.setLevel(_VERBOSITY_LOGLEVEL_DICT[args.verbose])
    else:
        logger.setLevel(logging.ERROR)
        logger.error('Invalid verbosity level: {}'.format(args.verbose))
    # remove stderr handler, by default use logger.Logger object
    #logger.removeHandler(temporary_stderr_handler)
    
    import lct.main_window as lm
    lm.main()
