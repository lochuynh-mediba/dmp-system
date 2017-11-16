from models.batch_master import *
from controllers import base_controller
from utils import logger_util
from utils import http_request_util
import os
from io import StringIO
import pandas as pd


def save_daily_report_to_file(aggregate_job: AggregateJob, aggregate_referrer: AggregateReferrer):
    """
    get data via appflyer api and write to file

    Parameters
    ----------
    aggregate_job               : AggregateJob
            aggregate job instance
    aggregate_referrer          : AggregateReferrer
            aggregate job referrer instance

    Examples
    --------

    Returns
    -------
    local_file                  : String
            data saved local file full path
            return None if there is no data
    """
    logger_util.logger_in()

    local_file = None

    if aggregate_job.kpi_type_id == 5: # Download report
        local_file = save_daily_download_report_to_file(aggregate_job, aggregate_referrer)

    logger_util.logger_out()

    return local_file


def save_daily_download_report_to_file(aggregate_job: AggregateJob, aggregate_referrer: AggregateReferrer):
    """
    get download data via appflyer api and write to file

    Parameters
    ----------
    aggregate_job               : AggregateJob
            aggregate job instance
    aggregate_referrer          : AggregateReferrer
            aggregate job referrer instance

    Examples
    --------

    Returns
    -------
    local_file                  : String
            data saved local file full path
            return None if there is no data
    """

    logger_util.logger_in()

    # get data referrer
    data_referrer = AggregateReferrerDataReferrer(aggregate_referrer.data_referrer)

    # api request url
    try:
        api_url = data_referrer.url
        api_token = data_referrer.api_token
        timezone = data_referrer.timezone
    except Exception as error:
        logger_util.logger_error("Lacking of arguments")
        logger_util.logger_out()
        raise error

    api_params = {'api_token': api_token, 'from': aggregate_job.start_date.strftime("%Y-%m-%d"),
                  'to': aggregate_job.end_date.strftime("%Y-%m-%d"), 'timezone': timezone}

    # call api
    response_content = http_request_util.http_get_request_content_string(api_url, params=api_params)

    # check if api over the quota
    if response_content == "Limit reached for daily_report":
        raise Exception("Limit reached for daily_report")

    # read data and save to pandas data frame
    data_tmp = StringIO(response_content)
    report_data_frame = pd.read_csv(data_tmp, sep=",")

    # aggregate sum to get final download number
    download_data_frame = report_data_frame.groupby(["Date"], as_index=False).agg({"Installs": "sum"})

    # add application type to data
    download_data_frame["application_type"] = aggregate_job.application_type

    # change data columns name
    download_data_frame.columns = ["count_date", "count", "application_type"]
    download_data_frame = download_data_frame[["count_date", "application_type", "count"]]

    # setup local file to write report values
    file_name = data_referrer.base_filename
    file_name = file_name.replace('%%start_date%%', aggregate_job.start_date.strftime("%Y%m%d"))
    file_name = file_name.replace('%%end_date%%', aggregate_job.end_date.strftime("%Y%m%d"))
    local_file_path = base_controller.config_controller_object.get_aggregate_file_tmp_dir()
    # create dir if not exist
    os.makedirs(local_file_path, exist_ok=True)
    local_file = local_file_path + file_name

    download_data_frame.to_csv(local_file, index=False)

    logger_util.logger_out()

    return local_file
