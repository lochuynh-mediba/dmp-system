from models.batch_master import *
from models.common_master import *
from sqlalchemy import *
from sqlalchemy.orm import *
from utils import logger_util
import datetime


class AggregateJobMySqlUtil:

    @classmethod
    def get_aggregate_jobs_list(cls, sql_ses, query_date, kpi_type=None, aggregate_job_list=None,
                                status=JobStatus.not_yet):
        """
        Get aggregate job list filtering with aggregate_type and status

        Parameters
        ----------
        sql_ses                     : sql_alchemy session
                mysql session
        kpi_type  : int
                aggregate type
        aggregate_job_list          : list
                aggregate jobs list
        query_date                  : DATE
                query date (end_date of job should less than query date)
        status                      : JobStatus
                aggregate job status

        Examples
        --------

        Returns
        -------
        cursors : AggregateJob list
                query result
        """
        # get enable services
        enable_services = sql_ses.query(Service).filter(Service.enable_flag == 1).options(load_only("service_id"))

        # filter with enable services
        cursors = sql_ses.query(AggregateJob).filter(AggregateJob.service_id.in_(enable_services))

        # filter with kpi_type
        if kpi_type is not None:
            cursors = cursors.filter(AggregateJob.kpi_type_id == kpi_type)

        # filter with aggregate_job_list
        if aggregate_job_list is not None:
            cursors = cursors.filter(AggregateJob.job_id.in_(aggregate_job_list))

        # filter with status
        cursors = cursors.filter(AggregateJob.status == status.value)

        # download_query_date (1 days before query_date)
        download_query_date = query_date - datetime.timedelta(days=1)

        # filter with kpi_type_id & end_date
        # 他のKPI種別の場合は、昨日までジョブを集計 => AggregateJob.end_date < query_date
        # ダウンロード数のKピ種別の場合は、一昨日までジョブを集計 => AggregateJob.end_date < download_query_date
        cursors = cursors.filter(or_(and_(AggregateJob.kpi_type_id != 5, AggregateJob.end_date < query_date),
                                     and_(AggregateJob.kpi_type_id == 5, AggregateJob.end_date < download_query_date)))

        return cursors.all()

    @classmethod
    def update_aggregate_job_with_status(cls, sql_ses, aggregate_job, status):
        """
        update aggregate job status
        Note : using when aggregate_job is detached to session
                otherwise, just change status value and commit

        Parameters
        ----------
        sql_ses         : sql_alchemy session
                mysql session
        aggregate_job      : AggregateJob
                aggregate job instance
        status          : TDExportJobStatus
                aggregate job status

        Examples
        --------

        Returns
        -------
        """
        aggregate_job.status = status.value
        sql_ses.merge(aggregate_job)

    @classmethod
    def insert_aggregate_job(cls, sql_ses, aggregate_job: AggregateJob, aggregate_next_start_date,
                             aggregate_next_end_date):

        logger_util.logger_in()

        new_aggregate_job = AggregateJob(service_id=aggregate_job.service_id,
                                         kpi_type_id=aggregate_job.kpi_type_id,
                                         application_type=aggregate_job.application_type,
                                         start_date=aggregate_next_start_date,
                                         end_date=aggregate_next_end_date,
                                         status=JobStatus.not_yet.value)
        sql_ses.add(new_aggregate_job)

        logger_util.logger_out()

    @classmethod
    def get_aggregate_referrer(cls, sql_ses, service_id, kpi_type, application_type):
        """
        Get aggregate referrer

        Parameters
        ----------
        sql_ses             : sql_alchemy session
                mysql session
        service_id          : int
                service id
        kpi_type      : int
                kpi type
        application_type  : int
                application type

        Examples
        --------

        Returns
        -------
        cursors : AggregateReferrer object
                query result
        """
        cursors = sql_ses.query(AggregateReferrer)\
            .filter(and_(AggregateReferrer.service_id == service_id,
                         AggregateReferrer.kpi_type_id == kpi_type,
                         AggregateReferrer.application_type == application_type))\
            .order_by(AggregateReferrer.id)
        return cursors.first()

    @classmethod
    def get_result_table_mapping(cls, sql_ses, service_id, kpi_type):
        """
        Get aggregate result mapping table

        Parameters
        ----------
        sql_ses             : sql_alchemy session
                mysql session
        service_id          : int
                service id
        kpi_type      : int
                kpi_type type

        Examples
        --------

        Returns
        -------
        cursors : ResultTableMapping object
                query result
        """
        cursors = sql_ses.query(ResultTableMapping)\
            .filter(and_(ResultTableMapping.service_id == service_id,
                         ResultTableMapping.kpi_type_id == kpi_type))
        return cursors.first()
