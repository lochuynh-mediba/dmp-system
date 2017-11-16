import os
import sys
import json
import logging.config
import traceback
import inspect

logger = None

logger_name_td_query_trigger = "td_query_trigger"
logger_name_td_s3_export = "td_s3_export"
logger_name_aggregate_trigger = "aggregate_trigger"


def setup_logger(logger_name=None, config_file='log_config.json', default_level=logging.INFO):
    """
    Config logger

    Parameters
    ----------
    logger_name     : str
            logger module name
    config_file     : str
            logger config file
    default_level   : log level
            logger default level

    Examples
    --------

    Returns
    -------

    """

    # get config file full paths
    config_file_dir = os.path.join(os.path.dirname(sys.argv[0]), "configurations/")
    config_file_path = config_file_dir + config_file

    # read config data from config file
    with open(config_file_path, 'rt') as file_reader:
        try:
            config = json.load(file_reader)
            # setup config to logging
            logging.config.dictConfig(config)
        except ValueError as error:
            print(error)
            logging.basicConfig(level=default_level)

    # get module based logger
    global logger
    if logger_name is not None:
        logger = logging.getLogger(logger_name)
        for handler in logger.handlers:
            if isinstance(handler, logging.handlers.TimedRotatingFileHandler):
                handler.suffix = "%Y-%m-%d"
    else:
        logger = logging.getLogger()

    # silence google api traceback error
    logging.getLogger('googleapiclient.discovery_cache').setLevel(logging.ERROR)


def logger_in(message=None):
    global logger
    func = inspect.currentframe().f_back
    func_params = func.f_code
    args, _, _, values = inspect.getargvalues(func)

    params_message = ""
    for arg in args:
        if arg == "self":
            continue
        value = values[arg]
        params_message += "%s=%s, " % (arg, value)

    # Dump the message + the name of this function to the log.
    logger.info("[IN] %s in %s line %i : params {%s}, message {%s}" % (
        func_params.co_name,
        func_params.co_filename,
        func_params.co_firstlineno,
        params_message,
        message
    ))


def logger_out(message=None):
    global logger
    func = inspect.currentframe().f_back.f_code
    logger.info("[OUT] %s in %s line %i : message {%s}" % (
        func.co_name,
        func.co_filename,
        func.co_firstlineno,
        message
    ))


def logger_in_debug(message=None):
    global logger
    func = inspect.currentframe().f_back
    func_params = func.f_code
    args, _, _, values = inspect.getargvalues(func)

    params_message = ""
    for arg in args:
        if arg == "self":
            continue
        value = values[arg]
        params_message += "%s=%s, " % (arg, value)

    # Dump the message + the name of this function to the log.
    logger.debug("[IN] %s in %s line %i : params {%s}, message {%s}" % (
        func_params.co_name,
        func_params.co_filename,
        func_params.co_firstlineno,
        params_message,
        message
    ))


def logger_out_debug(message=None):
    global logger
    func = inspect.currentframe().f_back.f_code
    logger.debug("[OUT] %s in %s line %i : message {%s}" % (
        func.co_name,
        func.co_filename,
        func.co_firstlineno,
        message
    ))


def logger_debug(message):
    global logger
    logger.debug(message)


def logger_info(message):
    global logger
    logger.info(message)


def logger_warning(message):
    global logger
    logger.warning(message)


def logger_error(message):
    global logger
    logger.error(message)


def logger_critical(message):
    global logger
    logger.critical(message)


def logger_traceback():
    exc_type, exc_value, exc_traceback = sys.exc_info()
    traceback_message = repr(traceback.format_exception(exc_type, exc_value,exc_traceback))
    global logger
    logger.error(traceback_message)
