import datetime


def get_next_aggregate_date(kpi_type, prev_start_date, prev_end_date):
    """
    generate next start_date and end_date for next aggregate_job

    Parameters
    ----------
    kpi_type            : int
            kpi type
    prev_start_date     : date
            previous start_date
    prev_end_date       : date
            previous end_date

    Examples
    --------

    Returns
    next_start_date     : date
            next start_date
    next_end_date       : date
            next end_date
    -------
    """

    next_end_date = prev_end_date + datetime.timedelta(days=1)
    next_start_date = prev_start_date

    # calculate for next aggregate_date
    if kpi_type == 4:  # MAU
        if next_end_date.month > next_start_date.month:
            next_start_date = next_end_date
    else:
        next_start_date = next_end_date

    return next_start_date, next_end_date
