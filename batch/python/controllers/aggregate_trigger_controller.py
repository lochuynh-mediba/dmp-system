from controllers import base_controller
from controllers.aggregate_controller import *
from utils import mysql_util
from utils import common_util
import datetime
from utils import logger_util
from utils import google_api_util
from utils import file_util
from utils import gamegift_api_util
from utils import appflyer_report_api_util
from models.mongo_common_master import *
from models.mongo_aggregate_master import *


def execute_aggregate_job(aggregate_job, repeat_next):
    """
    Executing aggregate job

    Parameters
    ----------
    aggregate_job           : AggregateJob
            aggregate job
    repeat_next         : bool
            true if automatically add new aggregate_job to db

    Examples
    --------

    Returns
    -------
    """
    logger_util.logger_in()

    try:
        # get other related info to this aggregate job
        with base_controller.config_controller_object.mysql_session() as sql_ses:
            # get aggregate job referrer
            aggregate_referrer = mysql_util.AggregateJobMySqlUtil.get_aggregate_referrer(sql_ses,
                                                                                         aggregate_job.service_id,
                                                                                         aggregate_job.kpi_type_id,
                                                                                         aggregate_job.application_type)

            # get result_mapping_table to export aggregate result
            result_table_mapping = mysql_util.AggregateJobMySqlUtil.get_result_table_mapping(sql_ses,
                                                                                             aggregate_job.service_id,
                                                                                             aggregate_job.kpi_type_id)
            result_table_name = result_table_mapping.result_table_name

            # start and end date for next job
            aggregate_next_start_date, aggregate_next_end_date = common_util.get_next_aggregate_date(
                aggregate_job.kpi_type_id,
                aggregate_job.start_date,
                aggregate_job.end_date)
            sql_ses.expunge_all()
    except Exception as error:
        logger_util.logger_error("DB query error=%s" % error)
        update_detached_aggregate_job_status(aggregate_job, JobStatus.not_yet)
        logger_util.logger_out()
        return

    if aggregate_referrer.data_referrer_type == 1:      # GA API
        # Save GA data to local file
        try:
            local_file = google_api_util.save_google_analytics_to_file(aggregate_job, aggregate_referrer)
        except Exception as error:
            logger_util.logger_error("Google API save file error =%s" % error)
            logger_util.logger_traceback()
            update_detached_aggregate_job_status(aggregate_job, JobStatus.not_yet)
            logger_util.logger_out()
            return
    elif aggregate_referrer.data_referrer_type == 2:    # Gamegift API
        try:
            local_file = gamegift_api_util.save_gamegift_data_to_file(aggregate_job, aggregate_referrer)
        except Exception as error:
            logger_util.logger_error("Gamegift API save file error =%s" % error)
            logger_util.logger_traceback()
            update_detached_aggregate_job_status(aggregate_job, JobStatus.not_yet)
            logger_util.logger_out()
            return
    elif aggregate_referrer.data_referrer_type == 3:    # AppFlyer API
        try:
            local_file = appflyer_report_api_util.save_daily_report_to_file(aggregate_job, aggregate_referrer)
        except Exception as error:
            logger_util.logger_error("AppFlyer API save file error =%s" % error)
            logger_util.logger_traceback()
            update_detached_aggregate_job_status(aggregate_job, JobStatus.not_yet)
            logger_util.logger_out()
            return

    if local_file is None:
        logger_util.logger_error("Cannot get data from data source")
        update_detached_aggregate_job_status(aggregate_job, JobStatus.not_yet)
        logger_util.logger_out()
        return

    aggregate_controller = AggregateController.controller_factory(local_file, aggregate_job)
    try:
        # execute aggregate job
        aggregate_controller.execute()
    except Exception as error:
        logger_util.logger_error("Fail to aggregate %s" % error)
        update_detached_aggregate_job_status(aggregate_job, JobStatus.not_yet)
    else:
        logger_util.logger_info("Successfully aggregate")
        try:
            with base_controller.config_controller_object.mysql_session() as sql_ses:
                # export aggregated result to db
                aggregate_controller.write_data_to_table(sql_ses, result_table_name)
                # update aggregate_job status
                mysql_util.AggregateJobMySqlUtil.update_aggregate_job_with_status(sql_ses, aggregate_job,
                                                                                  JobStatus.success)
                # insert new aggregate_job if needed
                if repeat_next:
                    mysql_util.AggregateJobMySqlUtil.insert_aggregate_job(sql_ses, aggregate_job,
                                                                          aggregate_next_start_date,
                                                                          aggregate_next_end_date)
        except Exception as error:
            logger_util.logger_error("Fail to update db %s" % error)
            update_detached_aggregate_job_status(aggregate_job, JobStatus.not_yet)

    try:
        file_util.remove_file(local_file)
    except Exception as error:
        logger_util.logger_warning("Fail to remove local temp file %s" % error)

    logger_util.logger_out()


def update_detached_aggregate_job_status(aggregate_job, status):
    """
    update aggregate job status
    Note : using when aggregate_job is detached to session
            otherwise, just change status value and commit

    Parameters
    ----------
    aggregate_job      : AggregateJob
            aggregate job instance
    status          : TDExportJobStatus
            aggregate job status

    Examples
    --------

    Returns
    -------
    """
    logger_util.logger_in()

    with base_controller.config_controller_object.mysql_session() as sql_ses:
        mysql_util.AggregateJobMySqlUtil.update_aggregate_job_with_status(sql_ses, aggregate_job, status)

    logger_util.logger_out()


def execute(processing_mode, kpi_type, aggregate_job_ids, repeat_next):
    """
    Executing aggregate_trigger

    Parameters
    ----------
    processing_mode     : int
            processing_mode
    kpi_type            : int
            aggregate_type of jobs to be aggregated
    aggregate_job_ids   : list
            aggregate_id list of jobs to be aggregated
    repeat_next         : bool
            true if automatically add new aggregate_job to db

    Examples
    --------

    Returns
    -------
    """

    logger_util.logger_in()

    # current_date = datetime.datetime.now().date()
    #
    # # query all count job list
    # with base_controller.config_controller_object.mysql_session() as sql_ses:
    #     if processing_mode == 0:
    #         aggregate_job_list = mysql_util.AggregateJobMySqlUtil.get_aggregate_jobs_list(sql_ses, current_date)
    #     elif processing_mode == 1:
    #         aggregate_job_list = mysql_util.AggregateJobMySqlUtil.get_aggregate_jobs_list(sql_ses, current_date,
    #                                                                                       kpi_type=kpi_type)
    #     elif processing_mode == 2:
    #         aggregate_job_list = mysql_util.AggregateJobMySqlUtil.get_aggregate_jobs_list(sql_ses, current_date,
    #                                                                                       kpi_type=None,
    #                                                                                       aggregate_job_list=aggregate_job_ids)
    #
    #     logger_util.logger_debug("aggregate_job_list count=%d" % len(aggregate_job_list))
    #
    #     # update status to "processing"
    #     for aggregate_job in aggregate_job_list:
    #         aggregate_job.status = JobStatus.processing.value
    #
    #     sql_ses.commit()
    #
    #     # detach all objects from session
    #     sql_ses.expunge_all()
    #
    # # execute each count job
    # for aggregate_job in aggregate_job_list:
    #     execute_aggregate_job(aggregate_job, repeat_next)

    base_controller.config_controller_object.connect_mongodb()

    aggregate_referrers = AggregateReferrer.objects()
    for aggregate_referrer in aggregate_referrers:
        print(aggregate_referrer.to_json(ensure_ascii=False))

    # service_groups = mongo_common_master.ServiceGroup.objects()
    # for service_group in service_groups:
    #     print(service_group.to_json(ensure_ascii=False))
    #     for service in service_group.services:
    #         print(service.to_json(ensure_ascii=False))
    #
    #     print("------------------------------------------------------")
    #
    #     services = mongo_common_master.Service.objects(service_group=service_group)
    #     for service in services:
    #         print(service.to_json(ensure_ascii=False))
    #
    #     print("------------------------------------------------------")

    # services = mongo_common_master.Service.objects()
    # for service in services:
    #     print(service.to_json(ensure_ascii=False))
    #     print(service.service_group_id.to_json(ensure_ascii=False))
    logger_util.logger_out()
