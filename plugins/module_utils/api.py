# !/usr/bin/python3

# Copyright (c) 2024, Tobias Bauriedel <tobias.bauriedel@netways.de>
# GNU General Public License v3.0+ (see LICENSES/GPL-3.0-or-later.txt or
# https://www.gnu.org/licenses/gpl-3.0.txt)

import ssl

try:
    from elasticsearch import Elasticsearch
    HAS_ELASTICSEARCH = True
    ELASTICSEARCH_IMPORT_ERROR = None
except ImportError as import_error:
    HAS_ELASTICSEARCH = False
    ELASTICSEARCH_IMPORT_ERROR = import_error


class Api():

    def new_client_basic_auth(host, auth_user, auth_pass, ca_certs, verify_certs) -> Elasticsearch:
        ctx = ssl.create_default_context(cafile=ca_certs)
        ctx.check_hostname = False
        ctx.verify_mode = False
        return Elasticsearch(hosts=[host], basic_auth=(auth_user, auth_pass), ssl_context=ctx, verify_certs=verify_certs)
