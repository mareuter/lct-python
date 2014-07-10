#!/usr/bin/env python
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
    _FILE_LOG_FORMAT = '%(asctime)s - %(levelname)s - %(name)s - %(message)s'
    
    # Parse the command line optional arguments
    parser = argparse.ArgumentParser(usage='%(prog)s [option]... ')
    
    program_settings = parser.add_argument_group('program_settings')
    
    program_settings.add_argument('-t', '--localtime', 
                                  help='Give a local time. Format: YYYY/MM/DD HH:MM:SS')
    
    logging_group = parser.add_argument_group('logging')
    # Logging options
    logging_group.add_argument('-l', '--log-file', help='Set the log file path.')
    logging_group.add_argument('-v', '--verbose', action='count', default=0,
                      help='Set the log verbosity level.')

    # parse and process arguments
    args = parser.parse_args()
    
    # Setup top level logger using command line options
    logger = logging.getLogger('lct')
    file_formatter = logging.Formatter(_FILE_LOG_FORMAT)
    if args.log_file is not None:
        import os
        log_filename = os.path.expandvars(os.path.expanduser(args.log_file))
        try:
            file_handler = logging.FileHandler(log_filename)
        except IOError:
            # Write access denied, try the home area.
            direc = os.path.dirname(log_filename)
            log_filename = log_filename.replace(direc, os.path.expanduser("~"))
            print "Write access denied. Writing to", os.path.expanduser("~"), "instead!"
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
    

    import sys
    import qdarkstyle
    
    from PyQt4 import QtGui
    app = QtGui.QApplication(sys.argv)
    app.setStyleSheet(qdarkstyle.load_stylesheet(pyside=False))
    app.setOrganizationName("Type II Software")
    app.setApplicationName("Lunar Club Tools")
    
    import lct.main_window as lm
    form = lm.LunarClubTools(datetimestr=args.localtime)
    form.show()
    
    app.exec_()
