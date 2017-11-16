#!/bin/bash
# aggregate result to sql

function InfoLogger() {
  logger -is -t script -p local2.info '[INFO] '$1
}

function WarningLogger() {
  logger -is -t script -p local2.warning '[WARN] '$1
}

function ErrorLogger() {
  logger -is -t script -p local2.err '[ERROR] '$1
}

InfoLogger "aggregate_trigger Script Start"

# 二重起動チェック
CMDLINE=$(cat /proc/$$/cmdline | xargs --null) # プロセス番号のコマンド（引数込み）取得
if [[ $$ -ne $(pgrep -oxf "${CMDLINE}") ]]; then
    WarningLogger "Another same script is running"
    InfoLogger "sally_td_s3_export Script End\n"
    exit 1
fi

InfoLogger "Script Running"

BASEDIR=$(dirname "$0")
PARENTDIR="$(dirname "$BASEDIR")"

# Arguments check
while [[ $# -gt 1 ]]
do
key="$1"

case $key in
    -m|--mode)
    MODE="$2"
    shift # past argument
    ;;
    -ty|--kpitype)
    KPITYPE="$2"
    shift # past argument
    ;;
    -id|--jobid)
    JOBID="$2"
    shift # past argument
    ;;
    -re|--repeat)
    REPEAT="$2"
    shift # past argument
    ;;
    -envi|--environment)
    ENVIROMENT="$2"
    shift # past argument
    ;;
    --default)
    DEFAULT=YES
    ;;
    *)
            # unknown option
    ;;
esac
shift # past argument or value
done


# run python script
if [ $MODE -eq 0 ]
then
	InfoLogger "arguments : mode=$MODE , repeat=$REPEAT, environment=$ENVIROMENT"
	/usr/local/pyenv/shims/python3 "$PARENTDIR/python/aggregate_trigger.py" -m $MODE -re $REPEAT -envi $ENVIROMENT
elif [ $MODE -eq 1 ]
then
	InfoLogger "arguments : mode=$MODE , type=$KPITYPE , repeat=$REPEAT, environment=$ENVIROMENT"
	/usr/local/pyenv/shims/python3 "$PARENTDIR/python/aggregate_trigger.py" -m $MODE -ty $KPITYPE -re $REPEAT -envi $ENVIROMENT
elif [ $MODE -eq 2 ]
then
	InfoLogger "arguments : mode=$MODE , jobid=$JOBID , repeat=$REPEAT, environment=$ENVIROMENT"
	/usr/local/pyenv/shims/python3 "$PARENTDIR/python/aggregate_trigger.py" -m $MODE -ids $JOBID -re $REPEAT -envi $ENVIROMENT
else
	ErrorLogger "Mode value is wrong (mode in [0:2])"
fi

InfoLogger "aggregate_trigger Script End\n"