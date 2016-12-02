"""Domain validators."""

import validation
import slugify


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
    
