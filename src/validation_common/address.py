"""Address validators."""

import validation


class AddressValidator(validation.Validator):
    """Validator for an address."""

    SCHEMA = {
        '$schema': 'http://json-schema.org/draft-04/schema#',
        'title': 'Address',
        'description': 'An address',
        'type': 'string'
    }

    MAX_ADDRESS_SIZE = 128

    def _post_schema_validate(self, address_raw):
        address = address_raw.strip()

        if len(address) >= self.MAX_ADDRESS_SIZE:
            raise Error('Address is too long')

        return address


