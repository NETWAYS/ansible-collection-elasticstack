# !/usr/bin/python3

# Copyright (c) 2024, Tobias Bauriedel <tobias.bauriedel@netways.de>
# GNU General Public License v3.0+ (see LICENSES/GPL-3.0-or-later.txt or
# https://www.gnu.org/licenses/gpl-3.0.txt)

import traceback
import ssl

from ansible.module_utils.basic import missing_required_lib

try:
    from elasticsearch import Elasticsearch
except ImportError:
    HAS_ELASTICSEARCH = False
    ELASTICSEARCH_IMPORT_ERROR = traceback.format_exc()
else:
    HAS_ELASTICSEARCH = True
    ELASTICSEARCH_IMPORT_ERROR = None


class Api():

    @staticmethod
    def new_client_basic_auth(host, auth_user, auth_pass, ca_certs, verify_certs):
        if not HAS_ELASTICSEARCH:
            raise ImportError(missing_required_lib('elasticsearch'))

        ctx = ssl.create_default_context(cafile=ca_certs)
        ctx.check_hostname = False
        ctx.verify_mode = False

        return Elasticsearch(
            hosts=[host],
            basic_auth=(auth_user, auth_pass),
            ssl_context=ctx,
            verify_certs=verify_certs
        )
