"""Keywords validators."""

import validation


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
