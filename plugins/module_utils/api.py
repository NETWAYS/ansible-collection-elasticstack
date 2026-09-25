# !/usr/bin/python3

# Copyright (c) 2024, Tobias Bauriedel <tobias.bauriedel@netways.de>
# GNU General Public License v3.0+ (see LICENSE or
# https://www.gnu.org/licenses/gpl-3.0.txt)

import traceback

from ansible.module_utils.basic import missing_required_lib

# The modules need the 8.x client. Version 7 accepts basic_auth without sending
# the credentials, and the response objects that the module_utils read through
# .raw only exist from 8.0 on.
ELASTICSEARCH_MIN_VERSION = (8, 0, 0)

try:
    from elasticsearch import Elasticsearch, __version__ as ELASTICSEARCH_VERSION
except ImportError:
    HAS_ELASTICSEARCH = False
    HAS_SUPPORTED_ELASTICSEARCH = False
    ELASTICSEARCH_IMPORT_ERROR = traceback.format_exc()
    ELASTICSEARCH_VERSION = None
else:
    HAS_ELASTICSEARCH = True
    HAS_SUPPORTED_ELASTICSEARCH = ELASTICSEARCH_VERSION >= ELASTICSEARCH_MIN_VERSION
    ELASTICSEARCH_IMPORT_ERROR = None


def unsupported_elasticsearch_message():
    """Message for a client that is too old, for the modules to fail with."""
    if ELASTICSEARCH_VERSION is None:
        return missing_required_lib('elasticsearch')

    return (
        "The elasticsearch Python library on the target host is version %s, "
        "this module needs %s or later. Version 7 accepts the basic_auth argument "
        "without sending the credentials, so every request reaches Elasticsearch "
        "unauthenticated and is answered with HTTP 401. The distribution package "
        "python3-elasticsearch is still version 7 on EL 9 and Ubuntu 22.04. Install "
        "the library with pip instead, for example by setting elasticstack_force_pip "
        "to true."
        % (
            ".".join(str(part) for part in ELASTICSEARCH_VERSION),
            ".".join(str(part) for part in ELASTICSEARCH_MIN_VERSION),
        )
    )


class Api():

    @staticmethod
    def new_client_basic_auth(host, auth_user, auth_pass, ca_certs, verify_certs):
        if not HAS_ELASTICSEARCH:
            raise ImportError(missing_required_lib('elasticsearch'))

        # TLS options are only accepted for an https host, NodeConfig raises
        # ValueError as soon as one of them is set on a plain http host.
        kwargs = {}
        if host.startswith('https://'):
            kwargs['verify_certs'] = verify_certs
            if verify_certs and ca_certs:
                kwargs['ca_certs'] = ca_certs

        return Elasticsearch(
            hosts=[host],
            basic_auth=(auth_user, auth_pass),
            **kwargs
        )
