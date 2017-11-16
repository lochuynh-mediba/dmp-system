from models.batch_master import *
from controllers import base_controller
from utils import logger_util
import os
import csv
import datetime


def save_google_analytics_to_file(aggregate_job: AggregateJob, aggregate_referrer: AggregateReferrer):
    """
    get report from GA and save to local file

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
    """

    logger_util.logger_in()

    data_referrer = AggregateReferrerDataReferrer(aggregate_referrer.data_referrer)

    analytics = base_controller.config_controller_object.get_google_api_analytics()

    # dimension filtering
    try:
        dimension_filter_clauses = data_referrer.dimensionFilterClauses
    except Exception:
        dimension_filter_clauses = []

    response = get_report(analytics, data_referrer.view_id, str(aggregate_job.start_date), str(aggregate_job.end_date),
                          data_referrer.metrics, data_referrer.dimensions, data_referrer.orderBys,
                          dimension_filter_clauses)

    # create file name
    file_name = data_referrer.base_filename
    file_name = file_name.replace('%%start_date%%', aggregate_job.start_date.strftime("%Y%m%d"))
    file_name = file_name.replace('%%end_date%%', aggregate_job.end_date.strftime("%Y%m%d"))
    local_file_path = base_controller.config_controller_object.get_aggregate_file_tmp_dir()
    # create dir if not exist
    os.makedirs(local_file_path, exist_ok=True)
    local_file = local_file_path + file_name

    csv_header = ["count_date", "application_type", "count"]

    report = response.get('reports', [])[0]
    rows = report.get('data', {}).get('rows', [])
    metric_value_array = []
    if aggregate_job.kpi_type_id == 4:  # MAU
        if len(rows) > 0:
            metric_value = rows[0].get('metrics', [])[0].get('values', [])[0]
            metric_value_array.append(metric_value)
        count_date_start = aggregate_job.end_date
    else:
        count_date_start = aggregate_job.start_date
        for row in rows:
            metric_value = row.get('metrics', [])[0].get('values', [])[0]
            metric_value_array.append(metric_value)

    with open(local_file, 'w') as csv_file:
        data_writer = csv.writer(csv_file, dialect='excel')
        data_writer.writerow(csv_header)
        for metric_value in metric_value_array:
            data_row = [str(count_date_start), aggregate_job.application_type, metric_value]
            data_writer.writerow(data_row)
            count_date_start += datetime.timedelta(days=1)

    logger_util.logger_out()

    return local_file


def get_report(analytics, view_id, start_date, end_date, metrics, dimensions, order, dimension_filter_clauses):
    """Queries the Analytics Reporting API V4.

    Args:
      analytics     : GoogleAnalytics
            An authorized Analytics Reporting API V4 service object.
      view_id       : str
            Google analytics view ID
      start_date    : DATE
      end_date      : DATE
      metrics       : arrays of str
      dimensions    : arrays of str
      order         : arrays of str
      dimension_filter_clauses      : array
            Dimension filter clause
    Returns:
      The Analytics Reporting API V4 response.
    """
    print(metrics)
    print(dimensions)
    return analytics.reports().batchGet(
        body={
            'reportRequests': [
                {
                    'viewId': view_id,
                    'dateRanges': [{'startDate': start_date, 'endDate': end_date}],
                    'metrics': metrics,
                    'dimensions': dimensions,
                    'orderBys': order,
                    'includeEmptyRows': 'true',
                    'dimensionFilterClauses': dimension_filter_clauses
                }]
        }
    ).execute()
