from models.batch_master import *
import pandas as pd
from datetime import datetime
from utils import logger_util


class AggregateController:

    """Base Controller for controlling Aggregate job
    """

    write_to_sql_query_string_dict = {'1': 'INSERT INTO %s (count_date, application_type, count) VALUES(:cntDate, :cntApplication, :countNum) ON DUPLICATE KEY UPDATE count = :countNum',
                                      '2': 'INSERT INTO %s (count_date, application_type, count) VALUES(:cntDate, :cntApplication, :countNum) ON DUPLICATE KEY UPDATE count = :countNum',
                                      '3': 'INSERT INTO %s (count_date, application_type, count) VALUES(:cntDate, :cntApplication, :countNum) ON DUPLICATE KEY UPDATE count = :countNum',
                                      '4': 'INSERT INTO %s (count_date, application_type, count) VALUES(:cntDate, :cntApplication, :countNum) ON DUPLICATE KEY UPDATE count = :countNum',
                                      '5': 'INSERT INTO %s (count_date, application_type, count) VALUES(:cntDate, :cntApplication, :countNum) ON DUPLICATE KEY UPDATE count = :countNum'}

    @classmethod
    def controller_factory(cls, local_data_file, aggregate_job: AggregateJob):
        """
        Factory function for creating AggregateController

        Parameters
        ----------
        local_data_file   : string
            local file paths of data file
        aggregate_job    : AggregateJob
            aggregate job

        Examples
        --------

        Returns
        -------
        new aggregate_controller : AggregateController
            new aggregate_controller instance
        """

        logger_util.logger_in()

        kpi_type = aggregate_job.kpi_type_id
        if kpi_type == 1:
            aggregate_controller = PVAggregateController(local_data_file, aggregate_job)
        elif kpi_type == 2:
            aggregate_controller = SessionAggregateController(local_data_file, aggregate_job)
        elif kpi_type == 3:
            aggregate_controller = DAUAggregateController(local_data_file, aggregate_job)
        elif kpi_type == 4:
            aggregate_controller = MAUAggregateController(local_data_file, aggregate_job)
        elif kpi_type == 5:
            aggregate_controller = DownloadAggregateController(local_data_file, aggregate_job)
        else:
            aggregate_controller = AggregateController(local_data_file, aggregate_job)

        logger_util.logger_out("aggregate_controller=%s" % aggregate_controller)

        return aggregate_controller

    def __init__(self, local_data_file, aggregate_job: AggregateJob):

        logger_util.logger_in_debug()

        self.data_file = local_data_file
        self.aggregate_job = aggregate_job
        self.input_data = None
        self.aggregate_output = None

        logger_util.logger_out_debug()

    def read_data(self):
        """
        Read data_file to pandas data_frame

        Parameters
        ----------

        Examples
        --------

        Returns
        -------
        """
        logger_util.logger_in_debug()
        self.input_data = pd.read_csv(self.data_file)
        logger_util.logger_out_debug()

    def execute(self):
        """
        execute aggregation : do nothing here

        Parameters
        ----------

        Examples
        --------

        Returns
        -------
        """
        logger_util.logger_in()
        logger_util.logger_info("This kind of aggregation is not supported")
        logger_util.logger_out()

    def get_write_to_sql_query_string(self, table_name):
        """
        create write query string

        Parameters
        ----------
        table_name      : str
            table name

        Examples
        --------

        Returns
        -------
        query_str       : str
            query string
        """
        kpi_type = self.aggregate_job.kpi_type_id
        query_str = AggregateController.write_to_sql_query_string_dict[str(kpi_type)]
        return query_str % table_name


class PVAggregateController(AggregateController):

    """PV AggregateController
    Attributes
    ----------
    """

    def __init__(self, local_data_file, aggregate_job: AggregateJob):
        super().__init__(local_data_file, aggregate_job)

    def execute(self):
        """
        execute aggregation

        Parameters
        ----------

        Examples
        --------

        Returns
        -------
        """
        logger_util.logger_in()

        self.read_data()
        self.do_aggregate()

        logger_util.logger_out()

    def do_aggregate(self):
        """
        do aggregate logic

        Parameters
        ----------

        Examples
        --------

        Returns
        -------
        """
        logger_util.logger_in_debug()

        self.aggregate_output = self.input_data

        logger_util.logger_out_debug()

    def write_data_to_table(self, sql_ses, table_name):
        """
        write aggregate result to sql db

        Parameters
        ----------
        sql_ses         : sql_alchemy session
            mysql session
        table_name      : str
            table name

        Examples
        --------

        Returns
        -------
        """
        logger_util.logger_in()

        logger_util.logger_debug(self.aggregate_output.head())
        query_string = self.get_write_to_sql_query_string(table_name)
        logger_util.logger_debug(query_string)

        for index, row in self.aggregate_output.iterrows():
            sql_ses.execute(query_string, {'cntDate': row['count_date'],
                                           'cntApplication': row['application_type'],
                                           'countNum': row['count']})

        logger_util.logger_out()


class SessionAggregateController(AggregateController):

    """Session AggregateController
    Attributes
    ----------
    """

    def __init__(self, local_data_file, aggregate_job: AggregateJob):
        super().__init__(local_data_file, aggregate_job)

    def execute(self):
        """
        execute aggregation

        Parameters
        ----------

        Examples
        --------

        Returns
        -------
        """
        logger_util.logger_in()

        self.read_data()
        self.do_aggregate()

        logger_util.logger_out()

    def do_aggregate(self):
        """
        do aggregate logic

        Parameters
        ----------

        Examples
        --------

        Returns
        -------
        """
        logger_util.logger_in_debug()

        self.aggregate_output = self.input_data

        logger_util.logger_out_debug()

    def write_data_to_table(self, sql_ses, table_name):
        """
        write aggregate result to sql db

        Parameters
        ----------
        sql_ses         : sql_alchemy session
            mysql session
        table_name      : str
            table name

        Examples
        --------

        Returns
        -------
        """
        logger_util.logger_in()

        logger_util.logger_debug(self.aggregate_output.head())
        query_string = self.get_write_to_sql_query_string(table_name)
        logger_util.logger_debug(query_string)

        for index, row in self.aggregate_output.iterrows():
            sql_ses.execute(query_string, {'cntDate': row['count_date'],
                                           'cntApplication': row['application_type'],
                                           'countNum': row['count']})

        logger_util.logger_out()


class DAUAggregateController(AggregateController):

    """DAU AggregateController
    Attributes
    ----------
    """

    def __init__(self, local_data_file, aggregate_job: AggregateJob):
        super().__init__(local_data_file, aggregate_job)

    def execute(self):
        """
        execute aggregation

        Parameters
        ----------

        Examples
        --------

        Returns
        -------
        """
        logger_util.logger_in()

        self.read_data()
        self.do_aggregate()

        logger_util.logger_out()

    def do_aggregate(self):
        """
        do aggregate logic

        Parameters
        ----------

        Examples
        --------

        Returns
        -------
        """
        logger_util.logger_in_debug()

        self.aggregate_output = self.input_data

        logger_util.logger_out_debug()

    def write_data_to_table(self, sql_ses, table_name):
        """
        write aggregate result to sql db

        Parameters
        ----------
        sql_ses         : sql_alchemy session
            mysql session
        table_name      : str
            table name

        Examples
        --------

        Returns
        -------
        """
        logger_util.logger_in()

        logger_util.logger_debug(self.aggregate_output.head())
        query_string = self.get_write_to_sql_query_string(table_name)
        logger_util.logger_debug(query_string)

        for index, row in self.aggregate_output.iterrows():
            sql_ses.execute(query_string, {'cntDate': row['count_date'],
                                           'cntApplication': row['application_type'],
                                           'countNum': row['count']})

        logger_util.logger_out()


class MAUAggregateController(AggregateController):

    """MAU AggregateController
    Attributes
    ----------
    """

    def __init__(self, local_data_file, aggregate_job: AggregateJob):
        super().__init__(local_data_file, aggregate_job)

    def execute(self):
        """
        execute aggregation

        Parameters
        ----------

        Examples
        --------

        Returns
        -------
        """
        logger_util.logger_in()

        self.read_data()
        self.do_aggregate()

        logger_util.logger_out()

    def do_aggregate(self):
        """
        do aggregate logic

        Parameters
        ----------

        Examples
        --------

        Returns
        -------
        """
        logger_util.logger_in_debug()

        self.aggregate_output = self.input_data

        logger_util.logger_out_debug()

    def write_data_to_table(self, sql_ses, table_name):
        """
        write aggregate result to sql db

        Parameters
        ----------
        sql_ses         : sql_alchemy session
            mysql session
        table_name      : str
            table name

        Examples
        --------

        Returns
        -------
        """
        logger_util.logger_in()

        logger_util.logger_debug(self.aggregate_output.head())
        query_string = self.get_write_to_sql_query_string(table_name)
        logger_util.logger_debug(query_string)

        for index, row in self.aggregate_output.iterrows():
            sql_ses.execute(query_string, {'cntDate': row['count_date'],
                                           'cntApplication': row['application_type'],
                                           'countNum': row['count']})

        logger_util.logger_out()


class DownloadAggregateController(AggregateController):

    """Download AggregateController
    Attributes
    ----------
    """

    def __init__(self, local_data_file, aggregate_job: AggregateJob):
        super().__init__(local_data_file, aggregate_job)

    def execute(self):
        """
        execute aggregation

        Parameters
        ----------

        Examples
        --------

        Returns
        -------
        """
        logger_util.logger_in()

        self.read_data()
        self.do_aggregate()

        logger_util.logger_out()

    def do_aggregate(self):
        """
        do aggregate logic

        Parameters
        ----------

        Examples
        --------

        Returns
        -------
        """
        logger_util.logger_in_debug()

        self.aggregate_output = self.input_data

        logger_util.logger_out_debug()

    def write_data_to_table(self, sql_ses, table_name):
        """
        write aggregate result to sql db

        Parameters
        ----------
        sql_ses         : sql_alchemy session
            mysql session
        table_name      : str
            table name

        Examples
        --------

        Returns
        -------
        """
        logger_util.logger_in()

        logger_util.logger_debug(self.aggregate_output.head())
        query_string = self.get_write_to_sql_query_string(table_name)
        logger_util.logger_debug(query_string)

        for index, row in self.aggregate_output.iterrows():
            sql_ses.execute(query_string, {'cntDate': row['count_date'],
                                           'cntApplication': row['application_type'],
                                           'countNum': row['count']})

        logger_util.logger_out()
