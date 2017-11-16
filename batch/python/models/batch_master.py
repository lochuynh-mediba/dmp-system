from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column
from sqlalchemy.dialects.mysql import *
from enum import Enum
import json

Base = declarative_base()


class JobStatus(Enum):

    """Job status
    """

    not_yet = 0
    success = 1
    processing = 2
    invalid = 9


class AggregateJob(Base):

    """Aggregate Job object definition
    """

    # table name
    __tablename__ = 'b_aggregate_job'

    # attributes
    job_id = Column(INTEGER(unsigned=True), primary_key=True)               # job ID
    service_id = Column(INTEGER(unsigned=True))                             # サービスID
    kpi_type_id = Column(INTEGER(unsigned=True))                            # 集計種別
    application_type = Column(INTEGER(unsigned=True))                       # アプリケション種別
    start_date = Column(DATE)                                               # 対象開始日
    end_date = Column(DATE)                                               # 対象終了日
    status = Column(TINYINT(unsigned=True))                                 # 実行ステータス

    def __str__(self, *args, **kwargs):
        return str(self.__dict__)


class AggregateReferrer(Base):

    """Aggregate Referrer definition
    """

    # table name
    __tablename__ = 'b_aggregate_referrer'

    # attributes
    id = Column(INTEGER(unsigned=True), primary_key=True)                   # ID
    service_id = Column(INTEGER(unsigned=True))                             # サービスID
    kpi_type_id = Column(INTEGER(unsigned=True))                            # 集計種別
    application_type = Column(INTEGER(unsigned=True))                       # アプリケション種別
    data_referrer_type = Column(TINYINT(unsigned=True))                     # 参照元種別
    data_referrer = Column(TEXT)                                            # 参照元情報

    def __str__(self, *args, **kwargs):
        return str(self.__dict__)


class DataReferrerType(Enum):

    """DataReferrer Type
    """

    s3 = 0
    ga = 1


class AggregateReferrerDataReferrer(object):

    def __init__(self, json_str):
        self.__dict__ = json.loads(json_str)