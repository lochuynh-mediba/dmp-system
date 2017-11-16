from mongoengine import *
from enum import Enum


class ServiceGroup(Document):

    """Service Group object definition
    """

    service_group_id = StringField(primary_key=True, required=True)
    service_group_name = StringField(required=True)
    enable_flag = BooleanField(required=True)
    services = ListField(ReferenceField("Service"))


class Service(Document):

    """Service Group object definition
    """

    service_id = StringField(primary_key=True, required=True)
    service_name = StringField(required=True)
    enable_flag = BooleanField(required=True)
    service_group = ReferenceField(ServiceGroup)


class KpiType(Document):

    """Kpi types object definition
    """

    kpi_type_id = StringField(primary_key=True, required=True)
    kpi_type_name = StringField(equired=True)
    description = StringField(equired=True)


class DataSource(Enum):

    """DataSource Type
    """

    td = "td"
    ga = "ga"
    appsflyer = "appsflyer"


class ApplicationType(Enum):

    """ApplicationType Type
    """

    web = "web"
    mobile = "mobile"
    mobile_ios = "mobile_ios"
    mobile_android = "mobile_android"

