from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column
from sqlalchemy.dialects.mysql import *

Base = declarative_base()


class ServiceGroup(Base):

    """ServiceGroup object definition
    """

    # table name
    __tablename__ = 'm_service_group'

    # attributes
    service_group_id = Column(INTEGER(unsigned=True), primary_key=True)     # Group ID
    service_group_name = Column(VARCHAR(length=255))                        # Group name

    def __str__(self, *args, **kwargs):
        return str(self.__dict__)


class Service(Base):

    """Service object definition
    """

    # table name
    __tablename__ = 'm_service'

    # attributes
    service_id = Column(INTEGER(unsigned=True), primary_key=True)           # Service ID
    service_name = Column(VARCHAR(length=255))                              # Service name
    service_group_id = Column(INTEGER(unsigned=True))                       # Service Group ID
    enable_flag = Column(TINYINT(display_width=3))                            # Enable Flag

    def __str__(self, *args, **kwargs):
        return str(self.__dict__)


class KpiType(Base):

    """KpiType object definition
    """

    # table name
    __tablename__ = 'm_kpi_type'

    # attributes
    kpi_type_id = Column(INTEGER(unsigned=True), primary_key=True)          # KPI type ID
    kpi_type_name = Column(VARCHAR(length=255))                             # KPI type name
    description = Column(TEXT)                                              # KPI type description

    def __str__(self, *args, **kwargs):
        return str(self.__dict__)


class ResultTableMapping(Base):

    """TD_query_job object definition
    """

    # table name
    __tablename__ = 'm_result_table_mapping'

    # attributes
    id = Column(INTEGER(unsigned=True), primary_key=True)               # ID
    service_id = Column(INTEGER(unsigned=True))                         # サービスID
    kpi_type_id = Column(INTEGER(unsigned=True))                        # 集計種別
    result_table_name = Column(TEXT)                                    # 集計間隔有効開始時点

    def __str__(self, *args, **kwargs):
        return str(self.__dict__)

