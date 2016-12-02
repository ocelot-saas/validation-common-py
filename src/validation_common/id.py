"""Id validation."""

import validation


class IdValidator(validation.Validator):
    """Validate an id."""

    SCHEMA = {
        '$schema': 'http://json-schema.org/draft-04/schema#',
        'title': 'Id',
        'description': 'An unique id for the entiry',
        'type': 'integer',
        'minimum': 1
    }

    def validate(self, id_raw):
        if not isinstance(id_raw, (int, str)):
            raise validation.Error('Id "{id_raw}" is neither an int nor a string'.format(id_raw=str(id_raw)))
                                   
        try:
            id = int(id_raw)
        except ValueError as e:
            raise validation.Error('Id "{id_raw}" cannot be converted to int'.format(id_raw=id_raw)) from e
            
        if id <= 0:
            raise validation.Error('Id "{id_raw}" is negative'.format(id_raw=id_raw))

        return id
