from models.batch_master import *
from controllers import base_controller
from utils import logger_util
from utils import http_request_util
import os
import csv
import datetime
from requests.auth import HTTPDigestAuth


def save_gamegift_data_to_file(aggregate_job: AggregateJob, aggregate_referrer: AggregateReferrer):
    """
    get data from gamegift api and write to file

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
    api_url = data_referrer.url

    # if need api auth
    api_auth = None
    need_authentication = data_referrer.need_authentication
    if need_authentication == 1:
        username = data_referrer.username
        password = data_referrer.password
        api_auth = HTTPDigestAuth(username, password)

    metric_value_array = []

    # get api parameters
    if aggregate_job.kpi_type_id == 4:  # MAU
        count_date_start = aggregate_job.end_date
        api_params = {'targetDate': count_date_start.strftime("%Y-%m-%d"), 'deviceType': aggregate_job.application_type}

    else:
        count_date_start = aggregate_job.start_date
        api_params = {'startDate': count_date_start.strftime("%Y-%m-%d"),
                      'endData': aggregate_job.end_date.strftime("%Y-%m-%d"),
                      'deviceType': aggregate_job.application_type}

    # call api
    json_response = http_request_util.http_get_request_json(api_url, api_params, api_auth)

    if json_response is None:
        raise Exception("No Json Response Exception")

    logger_util.logger_debug('json_response=%s' % json_response)

    # api response process
    # error check
    error_flag = json_response.get('errorFlag', 1)
    if error_flag == 1:
        error_message = json_response.get('errorMessage', 'Empty Error Message')
        raise Exception(error_message)

    # read and save data to array
    if aggregate_job.kpi_type_id == 4:  # MAU (1 row only)
        count = int(json_response.get('count', '0'))
        metric_value_array.append(count)
    else:   # Other KPI (array of data)
        kpi_data_rows = json_response.get('kpiData', [])
        for row in kpi_data_rows:
            count = int(row.get('count', '0'))
            metric_value_array.append(count)

    local_file = None

    if len(metric_value_array) > 0:

        # create file name
        file_name = data_referrer.base_filename
        file_name = file_name.replace('%%start_date%%', aggregate_job.start_date.strftime("%Y%m%d"))
        file_name = file_name.replace('%%end_date%%', aggregate_job.end_date.strftime("%Y%m%d"))
        local_file_path = base_controller.config_controller_object.get_aggregate_file_tmp_dir()
        # create dir if not exist
        os.makedirs(local_file_path, exist_ok=True)
        local_file = local_file_path + file_name

        csv_header = ["count_date", "application_type", "count"]

        # write data to file
        with open(local_file, 'w') as csv_file:
            data_writer = csv.writer(csv_file, dialect='excel')
            data_writer.writerow(csv_header)
            for metric_value in metric_value_array:
                data_row = [str(count_date_start), aggregate_job.application_type, metric_value]
                data_writer.writerow(data_row)
                count_date_start += datetime.timedelta(days=1)

    return local_file
