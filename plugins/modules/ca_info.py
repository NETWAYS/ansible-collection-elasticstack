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
    missing_required_lib,
    to_text,
    to_native,
    to_bytes
)

try:
    from cryptography.hazmat.primitives.serialization import pkcs12
    from cryptography.x509.oid import NameOID
    HAS_CRYPTOGRAPHY_PKCS12 = True
except ImportError:
    HAS_CRYPTOGRAPHY_PKCS12 = False

import binascii
import re
import sys


def analyze_ca_cert(result, __path, __password=None):
    # read the pkcs12 file
    with open(__path, 'rb') as f:
        pkcs12_data = f.read()

    # load pkcs12 with password in bytes
    __privatekey, certificate, additional_certificates = pkcs12.load_key_and_certificates(
        pkcs12_data,
        to_bytes(__password)
        )

    # map object values to result dict
    issuer = to_text(certificate.issuer.get_attributes_for_oid(
        NameOID.COMMON_NAME)[0].value
        )
    subject = to_text(certificate.subject.get_attributes_for_oid(
        NameOID.COMMON_NAME)[0].value
        )
    result['issuer'] = to_text(issuer)
    result['not_valid_after'] = to_text(certificate.not_valid_after)
    result['not_valid_before'] = to_text(certificate.not_valid_before)
    result['serial_number'] = to_text(certificate.serial_number)
    result['subject'] = to_text(subject)
    result['version'] = to_text(certificate.version)

    # read and map every extension in certificate.extensions
    for extension in certificate.extensions:
        # map oid object
        oid = to_text(extension.oid)
        oid = re.split('\\(|\\)|=| ', oid)
        extension_name = to_text(oid[4])
        oid = to_text(oid[2])

        # map critical object
        critical = to_text(extension.critical)

        # map extension values object
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

        # create new dictionaries for extensions name and its key values
        result['extensions'][extension_name] = dict()
        result['extensions'][extension_name]['values'] = dict()

        # map key values to key and value
        for key_value in key_values:
            key = key_value[0]

            # list of possible words in key which contain hex values
            # in bytes
            hex_values = ['identifier', 'digest']

            # check if key contans a value of hex_values
            check = False
            for hex_value in hex_values:
                if hex_value in key.lower():
                    check = True

            # convert to hex str and then format
            if check:
                if sys.version_info < (3, 0):
                    # Python 2 detected
                    value = key_value[1].replace('\\\\', '\\')[1:-1]
                    bytes_str = value.decode('string_escape')
                    hex_str = binascii.hexlify(bytes_str)
                else:
                    # Python 3 detected

                    # remove b' at beginning and ' at end to make string
                    # from "fake" bytes string
                    value = key_value[1][2:-1]
                    bytes_str = to_bytes(value).decode("unicode_escape")
                    bytes_str = to_bytes(bytes_str, 'iso-8859-1')
                    hex_str = binascii.hexlify(bytes_str).decode()

                # format hex string
                formatted_str = ':'.join(
                    hex_str[i:i + 2] for i in range(0, len(hex_str), 2)
                    )

                value = formatted_str
            else:
                value = key_value[1]

            # set check back to false
            check = False

            # map key and value
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

    # check if cryptography library is missing
    if not HAS_CRYPTOGRAPHY_PKCS12:
        module.fail_json(msg=missing_required_lib('cryptography >= 2.5'))

    __path = module.params['ca_dir'] + '/elastic-stack-ca.p12'

    try:
        result = analyze_ca_cert(result, __path, module.params['password'])
    except ValueError as e:
        module.fail_json(msg='ValueError: %s' % to_native(e))
    except Exception as e:
        module.fail_json(msg='Exception: %s' % to_native(e))

    module.exit_json(**result)


def main():
    run_module()


if __name__ == '__main__':
    main()
