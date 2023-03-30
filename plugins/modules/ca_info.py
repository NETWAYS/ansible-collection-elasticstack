# -*- coding: utf-8 -*-
# Copyright (c) 2023, Daniel Patrick <daniel.patrick@netways.de>
# GNU General Public License v3.0+ (see LICENSES/GPL-3.0-or-later.txt or
# https://www.gnu.org/licenses/gpl-3.0.txt)
# SPDX-License-Identifier: GPL-3.0-or-later

from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

from ansible.module_utils.basic import AnsibleModule, to_text, to_native, to_bytes
from cryptography.hazmat.primitives.serialization import pkcs12
from cryptography.x509.oid import NameOID

import re


def analyze_ca_cert(result, path, __password=None):
    # read the PKCS12 file
    with open(path, 'rb') as f:
        pkcs12_data = f.read()

    # import the PKCS12 data using cryptography
    privatekey, certificate, additional_certificates = pkcs12.load_key_and_certificates(
        pkcs12_data,
        to_bytes(__password)
        )

    # map objects to results
    result['version'] = to_text(certificate.version)
    result['serial_number'] = to_text(certificate.serial_number)
    result['not_valid_before'] = to_text(certificate.not_valid_before)
    result['not_valid_after'] = to_text(certificate.not_valid_after)
    issuer = to_text(certificate.issuer.get_attributes_for_oid(
        NameOID.COMMON_NAME)[0].value
        )
    subject = to_text(certificate.subject.get_attributes_for_oid(
        NameOID.COMMON_NAME)[0].value
        )
    result['issuer'] = issuer
    result['subject'] = to_text(subject)

    for extension in certificate.extensions:
        # map oid object
        oid = to_text(extension.oid)
        oid = re.split('\\(|\\)|=| ', oid)
        extension_name = to_text(oid[4])
        oid = to_text(oid[2])

        # map critical object
        critical = to_text(extension.critical)

        # map value object
        key_values = to_text(extension.value)
        key_values = re.split('\\(|\\)', key_values)

        # pop last and first item
        key_values.pop(0)
        key_values.pop(-1)

        # one item left with values, separated with ","
        # split and strip
        key_values = re.split(',', to_text(key_values[0]))
        key_values = [value.strip() for value in key_values]

        # split all items by "="
        key_values = [value.split('=') for value in key_values]

        # create new dictionary for extensions name and its key values
        result['extensions'][extension_name] = dict()
        result['extensions'][extension_name]['values'] = dict()

        # map key values to key and value
        for key_value in key_values:
            key = key_value[0]
            value = key_value[1]
            result['extensions'][extension_name]['values'][to_text(key)] = to_text(value)

        # map to results
        result['extensions'][extension_name]['oid'] = to_text(oid)
        result['extensions'][extension_name]['critical'] = to_text(critical)

    return result


def run_module():
    # define available arguments/parameters a user can pass to the module
    # set password and ca_dir to no_log for security
    module_args = dict(
        ca_dir=dict(type='str', no_log=True, required=True),
        password=dict(type='str', no_log=True, required=False, default=False)
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

    path = module.params['ca_dir'] + '/elastic-stack-ca.p12'

    try:
        result = analyze_ca_cert(result, path, module.params['password'])
    except ValueError as e:
        module.fail_json(msg='ValueError: %s' % to_native(e))
    except Exception as e:
        module.fail_json(msg='Exception: %s' % to_native(e))

    try:
        module.exit_json(**result)
    except ValueError as e:
        module.fail_json(msg='ValueError: %s' % to_native(e))
    except Exception as e:
        module.fail_json(msg='Exception: %s' % to_native(e))


def main():
    run_module()


if __name__ == '__main__':
    main()
