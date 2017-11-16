import argparse
from utils import argparse_util
from controllers import aggregate_trigger_controller
from utils import logger_util
from controllers import base_controller


if __name__ == "__main__":

    # logger config
    logger_util.setup_logger()

    logger_util.logger_in("Start Batch")

    # parse arguments from command line
    parser = argparse.ArgumentParser()

    parser.add_argument('-m', '--mode',
                        help='processing mode - 0:all_jobs 1:kpi_type 2:job_id_list',
                        required=True,
                        type=argparse_util.valid_unsinged_int)

    parser.add_argument('-ty', '--type',
                        help='kpi type - require > 0',
                        required=False,
                        type=argparse_util.valid_unsinged_int)

    parser.add_argument('-ids', '--job_ids',
                        help='aggregate job_ids list',
                        required=False,
                        nargs='+', type=int)

    parser.add_argument('-re', '--repeat_next',
                        help='next job adding or not - 0:false 1:true',
                        required=False,
                        type=argparse_util.valid_unsinged_int)

    parser.add_argument('-envi', '--environment',
                        help='environment - local:local dev:dev prd:prd',
                        required=True,
                        type=str)

    args = parser.parse_args()

    # get arguments
    processing_mode = args.mode
    kpi_type = None
    aggregate_job_ids = None
    repeat_next = False
    environment = args.environment

    logger_util.logger_info("environment:%s" % environment)

    if environment == "local":
        config_file = "local_config.ini"
    elif environment == "dev":
        config_file = "dev_config.ini"
    elif environment == "prd":
        config_file = "prd_config.ini"
    else:
        logger_util.logger_error("arguments have no valid environment")
        logger_util.logger_out("End Batch")
        exit()

    # config system
    config_success = base_controller.config_server(config_file)
    if not config_success:
        # config error
        logger_util.logger_out("End Batch")
        exit()

    if processing_mode == 1:
        kpi_type = args.type
        if kpi_type is None:
            logger_util.logger_error("arguments is not enough : lacking of kpi_type in mode 1")
            logger_util.logger_out("End Batch")
            exit()
    elif processing_mode == 2:
        aggregate_job_ids = args.job_ids
        if aggregate_job_ids is None:
            logger_util.logger_error("arguments is not enough : lacking of job_ids in mode 2")
            logger_util.logger_out("End Batch")
            exit()

    if args.repeat_next:
        repeat_next = bool(args.repeat_next)

    aggregate_trigger_controller.execute(processing_mode, kpi_type, aggregate_job_ids, repeat_next)

    logger_util.logger_out("End Batch")
