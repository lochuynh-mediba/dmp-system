import configparser
from oauth2client.service_account import ServiceAccountCredentials
import httplib2
from apiclient.discovery import build
import mongoengine
from utils import logger_util


class LocalConfigurationController:

    """Hold the configuration for local
            """

    def __init__(self):
        self.td_export_dir = None
        self.aggregate_file_tmp_dir = None

    def config(self, config_parser):

        """
        Config local

        Parameters
        ----------
        config_parser  : ConfigParser
            config parser object

        Examples
        --------

        Returns
        -------
        """
        logger_util.logger_in()

        self.td_export_dir = config_parser.get('local', 'td_export_dir')
        self.aggregate_file_tmp_dir = config_parser.get('local', 'aggregate_file_tmp_dir')

        logger_util.logger_out()


class MongoDbConfigurationController:

    """Hold the configuration for MongoDb
            """

    def __init__(self):
        self.database = None
        self.username = None
        self.password = None
        self.host = None
        self.port = None

    def config(self, config_parser):

        """
        Config local

        Parameters
        ----------
        config_parser  : ConfigParser
            config parser object

        Examples
        --------

        Returns
        -------
        """
        logger_util.logger_in()

        self.database = config_parser.get('mongodb', 'database')
        try:
            self.username = config_parser.get('mongodb', 'username')
            self.password = config_parser.get('mongodb', 'password')
            self.host = config_parser.get('mongodb', 'host')
            self.port = config_parser.get('mongodb', 'port')
        except configparser.NoOptionError:
            pass

        logger_util.logger_out()

    def connect(self):
        if (self.username is not None) and (self.host is not None):
            mongoengine.connect(db=self.database,
                                username=self.username, password=self.password,
                                host=self.host, port=self.port)
        elif self.username is not None:
            mongoengine.connect(db=self.database,
                                username=self.username, password=self.password)
        elif self.host is not None:
            mongoengine.connect(db=self.database,
                                host=self.host, port=self.port)
        else:
            mongoengine.connect(db=self.database)


class GoogleAPIConfigurationController:

    """Hold the configuration for google_api
            """

    SCOPES = ['https://www.googleapis.com/auth/analytics.readonly']

    def __init__(self):
        self.secret_key_path = None
        self.analytics = None

    def config(self, config_parser):
        """
        Config google_api

        Parameters
        ----------
        config_parser  : ConfigParser
            config parser object

        Examples
        --------

        Returns
        -------
        """
        logger_util.logger_in()

        self.secret_key_path = config_parser.get('google_api', 'secret_key_path')
        credentials = ServiceAccountCredentials.from_json_keyfile_name(self.secret_key_path, scopes=self.SCOPES)
        credentials.authorize(httplib2.Http())
        # Build the service object.
        self.analytics = build('analytics', 'v4', credentials=credentials)

        logger_util.logger_out()

    def get_analytic(self):
        return self.analytics


class ConfigurationController:

    """Hold all server configuration
    """

    def __init__(self, ):
        # local config
        self.local_config = LocalConfigurationController()
        # mongodb config
        self.mongodb_config = MongoDbConfigurationController()
        # google_api config
        self.google_api_config = GoogleAPIConfigurationController()

    def start_config(self, config_file):
        """
        Config MySql

        Parameters
        ----------
        config_file  : string
            config with *.ini file

        Examples
        --------

        Returns
        -------
        success : bool
            True if config successfully
            False if failed to config
        """

        logger_util.logger_in()

        config_parser = configparser.ConfigParser()

        # read config file
        try:
            config_parser.read(config_file)
            self.local_config.config(config_parser)
            self.mongodb_config.config(config_parser)
            self.google_api_config.config(config_parser)
        except configparser.ParsingError as error:
            # error handle
            logger_util.logger_error(error)
            logger_util.logger_traceback()
            logger_util.logger_out("success=False")
            return False

        logger_util.logger_out("success=True")

        return True

    def get_local_td_export_dir(self):
        """
        Get local export directory

        Parameters
        ----------

        Examples
        --------

        Returns
        -------
        td_export_dir  : string
            td query result export local directory
        """
        return self.local_config.td_export_dir

    def get_aggregate_file_tmp_dir(self):
        """
        Get local temporary file path to count

        Parameters
        ----------

        Examples
        --------

        Returns
        -------
        local_count_file_tmp_dir  : string
            local directory for processing file
        """
        return self.local_config.aggregate_file_tmp_dir

    def connect_mongodb(self):
        """
        Connect to Mongodb

        Parameters
        ----------

        Examples
        --------

        Returns
        -------
        """
        self.mongodb_config.connect()

    def get_google_api_analytics(self):
        """
        Get local temporary file path to count

        Parameters
        ----------

        Examples
        --------

        Returns
        -------
        google_api_analytics  : google analytics
            analytics object for GA
        """
        return self.google_api_config.get_analytic()
