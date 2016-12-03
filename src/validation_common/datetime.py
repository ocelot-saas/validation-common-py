"""Datetime validators."""

import validation


class DateTimeTsValidator(validation.Validator):
    """Date and time as a timestamp in UTC validator."""

    SCHEMA = {
        '$schema': 'http://json-schema.org/draft-04/schema#',
        'title': 'Users resouces response',        
        'description': 'A datetime timestamp, in UTC',
        'type': 'integer',
        'minimum': 0
    }

    def _post_schema_validate(self, datetime_ts_raw):
        return datetime_ts_raw
