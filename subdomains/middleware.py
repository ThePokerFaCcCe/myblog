import operator
import logging
import re

from django.http.request import HttpRequest

from subdomains.utils import get_domain


logger = logging.getLogger(__name__)
lower = operator.methodcaller('lower')


class SubdomainMiddleware(object):
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, req: HttpRequest):
        self.process_request(req)
        response = self.get_response(req)

        return response

    def process_request(self, request: HttpRequest):
        """
        Adds a ``subdomain`` attribute to the ``request`` parameter.
        """
        domain, host = map(lower, (get_domain(), request.get_host()))

        pattern = r'^(?:(?P<subdomain>.*?)\.)?%s(?::.*)?$' % re.escape(domain)
        matches = re.match(pattern, host)

        if matches:
            request.subdomain = matches.group('subdomain')
        else:
            request.subdomain = None
            logger.warning('The host %s does not belong to the domain %s, '
                           'unable to identify the subdomain for this request',
                           request.get_host(), domain)
