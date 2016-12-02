"""Common entities and their validation."""

import validation
import slugify


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


class ImageValidator(validation.Validator):
    """Validate an image."""

    # TODO(horia141): keep in sync with frontend
    IMAGE_ASPECT_RATIO = 16/9
    IMAGE_MIN_WIDTH = 800
    IMAGE_MIN_HEIGHT = 450
    IMAGE_MAX_WIDTH = 1600
    IMAGE_MAX_HEIGHT = 900
    IMAGE_WIDTH = IMAGE_MAX_WIDTH
    IMAGE_HEIGHT = IMAGE_MAX_HEIGHT

    SCHEMA = {
        '$schema': 'http://json-schema.org/draft-04/schema#',
        'title': 'Image',
        'description': 'An image',
        'type': 'object',
        'properties': {
            'orderNo': {
                'description': 'The order in which the image appears for display',
                'type': 'integer',
                'minimum': 0
            },
            'uri': {
                'description': 'The URI where the image can be retrieved',
                'type': 'string',
            },
            'width': {
                'description': 'The width of the image',
                'type': 'integer',
                'minimum': IMAGE_MIN_WIDTH,
                'maximum': IMAGE_MAX_WIDTH
            },
            'height': {
                'description': 'The height of the image',
                'type': 'integer',
                'minimum': IMAGE_MIN_HEIGHT,
                'maximum': IMAGE_MAX_HEIGHT
            }
        },
        'required': ['orderNo', 'uri', 'width', 'height'],
        'additionalProperties': False
    }

    def _post_schema_validate(self, image_raw):
        image = dict(image_raw)
        image['uri'] = image['uri'].strip()

        if image['uri'] == '':
            raise validation.Error('Image set url is empty')

        return image


class ImageSetValidator(validation.Validator):
    """Validate an image set."""

    SCHEMA = {
        '$schema': 'http://json-schema.org/draft-04/schema#',
        'title': 'Image set',
        'description': 'A set of images',
        'type': 'array',
        'items': ImageValidator.SCHEMA,
        'additionalItems': False
    }

    def __init__(self, image_validator):
        self._image_validator = image_validator

    def _post_schema_validate(self, image_set_raw):
        image_set = []

        for i in range(len(image_set_raw)):
            image = self._image_validator.validate(image_set_raw[i])
                
            if image['orderNo'] != i:
                raise validation.Error('Image set not properly ordered')

            image_set.append(image)

        return image_set


class KeywordsValidator(validation.Validator):
    """Validator for a keywords set."""

    SCHEMA = {
        '$schema': 'http://json-schema.org/draft-04/schema#',
        'title': 'Keywords',
        'description': 'A set of keywords',
        'type': 'array',
        'items': {
            'type': 'string',
        },
        'additionalItems': False
    }

    MAX_KEYWORD_SIZE = 128
    MAX_KEYWORDS = 64

    def _post_schema_validate(self, keywords_raw):
        keywords_unsorted = [kw.strip() for kw in keywords_raw]

        if any(kw == '' for kw in keywords_unsorted):
            raise validation.Error('Keyword is empty')

        for kw in keywords_unsorted:
            if len(kw) >= self.MAX_KEYWORD_SIZE:
                raise validation.Error('Keyword "{}" is too long'.format(kw))

        keywords = sorted(set(keywords_unsorted))

        if len(keywords) >= MAX_KEYWORDS:
            raise validation.Error('Too many keywords')

        return keywords


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


class HostToSubdomainValidator(validation.Validator):
    """Validator for the host header which produces the subdomain part."""

    SCHEMA = {
        '$schema': 'http://json-schema.org/draft-04/schema#',
        'title': 'Host Header',
        'description': 'An host header value',
        'type': 'string'
    }

    MAX_DOMAIN_SIZE = 128

    def __init__(self, master_domain):
        self._subdomain_re = re.compile(r'^([^.]+)[.]{}$'.format(master_domain))
        pass

    def _post_schema_validate(self, host):
        match = self.SUBDOMAIN_RE.match(host)

        if match is None:
            raise validation.Error('Host "{}" is not a valid domain'.format(host))

        subdomain = match.group(1)

        if len(subdomain) >= self.MAX_DOMAIN_SIZE:
            raise validation.Error('Subdomain "{}" is too long'.format(subdomain))

        if not subdomain == slugify.slugify(subdomain):
            raise validation.Error('Subdomain "{}" is not valid'.format(subdomain))

        return subdomain
    
