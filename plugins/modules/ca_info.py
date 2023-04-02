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
    analyze_cert
)


def run_module():
    module_args = dict(
        ca_dir=dict(type='str', no_log=True, required=False, default='/opt/es-ca'),
        ca_cert=dict(type='str', no_log=True, required=False, default='elastic-stack-ca.p12'),
        password=dict(type='str', no_log=True, required=False, default=None)
    )

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

    # the AnsibleModule object
    module = AnsibleModule(
        argument_spec=module_args,
        supports_check_mode=True
    )

    # check mode
    if module.check_mode:
        module.exit_json(**result)

    __path = module.params['ca_dir'] + '/' + module.params['ca_cert']

    try:
        result = analyze_cert(module, result, __path, module.params['password'])
    except ValueError as e:
        module.fail_json(msg='ValueError: %s' % to_native(e))
    except Exception as e:
        module.fail_json(msg='Exception: %s' % to_native(e))

    module.exit_json(**result)


def main():
    run_module()


if __name__ == '__main__':
    main()
