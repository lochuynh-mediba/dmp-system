import argparse
import datetime


def valid_start_time(start_time):
    """
    start_time validation for argparser

    """
    try:
        return datetime.datetime.strptime(start_time, "%Y-%m-%d %H")
    except ValueError:
        msg = "Not a valid date: '{0}'.".format(start_time)
        raise argparse.ArgumentTypeError(msg)


def valid_start_min(start_min):
    """
    start_min validation for argparser

    """
    try:
        int_start_min = int(start_min)
        if (int_start_min >= 0) & (int_start_min < 60):
            return int_start_min
        else:
            msg = "minute value is invalid"
            raise argparse.ArgumentTypeError(msg)
    except ValueError:
        msg = "minute must be int type"
        raise argparse.ArgumentTypeError(msg)


def valid_unsinged_int(value):
    """
    unsigned int value validation for argparser

    """
    try:
        int_value = int(value)
        if int_value >= 0:
            return int_value
        else:
            msg = "value must be equal or larger than 0"
            raise argparse.ArgumentTypeError(msg)
    except ValueError:
        msg = "value must be int type"
        raise argparse.ArgumentTypeError(msg)

