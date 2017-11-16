from models.mongo_common_master import *
import datetime


class AggregateReferrer(Document):

    """Aggregate Referrer object definition
    """

    service = ReferenceField(Service)
    kpi_types = ListField(ReferenceField(KpiType))

    # active duration
    active_start_day = DateTimeField(required=False)
    active_end_day = DateTimeField(required=False)

    # application type
    application_type = StringField(required=True)
    sub_application_type = StringField(required=False)

    # data source
    data_source = StringField(required=True)

    # for google analytics
    ga_view_id = StringField()
    ga_reference = DictField()


class AggregateJob(Document):

    """Aggregate Job object definition
    """

    service = ReferenceField(Service)
    kpi_types = ListField(ReferenceField(KpiType))
    duration_type = StringField(required=True)

    # auto update or insert
    auto_update_pre_hours = IntField(required=True)
    auto_update_max_step = IntField(required=True)

    # aggregate time
    start_time = DateTimeField(required=True)
    end_time = DateTimeField(required=True)

    # status
    job_status = IntField(required=True)

    # job create & update management
    create_at = DateTimeField()
    updated_at = DateTimeField(default=datetime.datetime.now)

    def save(self, *args, **kwargs):
        if not self.create_at:
            self.create_at = datetime.datetime.now()
        self.updated_at = datetime.datetime.now()
        return super(AggregateJob, self).save(*args, **kwargs)


class HourlyKpi(Document):

    """Hourly Kpi object definition
    """
    service = ReferenceField(Service)
    datetime_index = DateTimeField()
    aggregate_data = DictField()


class DailyKpi(Document):

    """Daily Kpi object definition
    """
    service = ReferenceField(Service)
    datetime_index = DateTimeField()
    aggregate_data = DictField()


class AggregateDurationType(Enum):

    """Aggregate Duration Type
    """

    hourly = "hourly"
    daily = "daily"


class AggregateJobStatis(Enum):

    """Aggregate Duration Type
    """

    not_yet = 0
    processing = 1
    success = 2
    unavailable = 9

