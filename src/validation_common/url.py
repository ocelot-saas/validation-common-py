"""URL validators."""

import urllib.parse as urlparse

import validation


class URLValidator(validation.Validator):
    """URL validator."""

    SCHEMA = {
        '$schema': 'http://json-schema.org/draft-04/schema#',
        'title': 'URL',
        'description': 'An URL',
        'type': 'string',        
    }

    ALLOWED_SCHEMES = frozenset(['http', 'https'])

    def _post_schema_validate(self, url_raw):
        # TODO(horia141): improvements to quoting/encodint etc.
        try:
            url_obj = urlparse.urlparse(url_raw)

            if url_obj.scheme not in self.ALLOWED_SCHEMS:
                raise validation.Error('Invalid scheme "{scheme}"'.format(scheme=url_obj.scheme))

            return url_obj.geturl()
        except Exception as e:
            raise validation.Error('Could not parse URL') from e
