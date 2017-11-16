from controllers import config_controller
import os
import sys
from utils import logger_util

# config controller instance
config_controller_object = config_controller.ConfigurationController()


def config_server(config_file='local_config.ini'):

    """
    Config server

    Parameters
    ----------
    config_file  : string
            config file location

    Examples
    --------

    Returns
    -------
    success : boolean
            config result status
    """

    logger_util.logger_in()

    config_file_dir = os.path.join(os.path.dirname(sys.argv[0]), "configurations/")
    config_file_path = config_file_dir + config_file

    # do config
    success = config_controller_object.start_config(config_file_path)

    logger_util.logger_out("success=%r" % success)

    return success
