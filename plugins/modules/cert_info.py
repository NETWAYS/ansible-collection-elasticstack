#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright (c) 2023, Daniel Patrick <daniel.patrick@netways.de>
# GNU General Public License v3.0+ (see LICENSES/GPL-3.0-or-later.txt or
# https://www.gnu.org/licenses/gpl-3.0.txt)
# SPDX-License-Identifier: GPL-3.0-or-later

from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

from ansible.module_utils.basic import (
    AnsibleModule,
    to_native
)

from ansible_collections.netways.elasticstack.plugins.module_utils.certs import (
    AnalyzeCertificate
)

argument_spec = dict(
    # module function variables
    path=dict(type='str', no_log=True, required=True),
    passphrase=dict(type='str', no_log=True, required=False, default=None)
)


def setup_module_object():
    module = AnsibleModule(
        argument_spec=argument_spec,
        supports_check_mode=True
    )
    return module


def run_module(module):
    # seed the result dict
    result = dict(
        changed=False,
        extensions=dict(),
        issuer='',
        not_valid_after='',
        not_valid_before='',
        serial_number='',
        subject='',
        version=''
    )

    # check mode
    if module.check_mode:
        module.exit_json(**result)

    try:
        cert_info = AnalyzeCertificate(module, result)
        result = cert_info.return_result()
    except ValueError as e:
        module.fail_json(msg='ValueError: %s' % to_native(e))
    except Exception as e:
        module.fail_json(msg='Exception: %s: %s' % (to_native(type(e)), to_native(e)))

    return result


def main():
    module = setup_module_object()
    return_dict = run_module(module)
    module.exit_json(**return_dict)


if __name__ == '__main__':
    main()
