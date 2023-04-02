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
    from cryptography.hazmat.backends import default_backend
    from cryptography.hazmat.primitives.serialization import pkcs12
    from cryptography.x509.oid import NameOID
    HAS_CRYPTOGRAPHY_PKCS12 = True
except ImportError:
    HAS_CRYPTOGRAPHY_PKCS12 = False

import binascii

SUPPORTED_EXTENSIONS = {
    'basicConstraints': [
        '_ca',
        '_path_length'
        ],
    'subjectKeyIdentifier': [
        '_digest'
        ],
    'authorityKeyIdentifier': [
        '_authority_cert_issuer',
        '_authority_cert_serial_number',
        '_key_identifier'
        ]
    }


def check_supported_vars(var_name, extension_name):
    check_supported_vars = False
    for variable in SUPPORTED_EXTENSIONS[extension_name]:
        if variable == var_name:
            check_supported_vars = True
    return check_supported_vars


def analyze_ca_cert(result, __path, __password=None):
    warnings = []
    loaded = False

    # read the pkcs12 file
    with open(__path, 'rb') as f:
        pkcs12_data = f.read()

    # try to load with 2 parameters
    # for cryptography >= 3.1.x
    try:
        privatekey, certificate, additional_certificates = pkcs12.load_key_and_certificates(
            pkcs12_data,
            to_bytes(__password),
            )
        loaded = True
    except Exception:
        pass

    # try to load with 3 parameters for
    # cryptography >= 2.5.x and <= 3.0.x
    if not loaded:
        backend = default_backend()
        privatekey, certificate, additional_certificates = pkcs12.load_key_and_certificates(
            pkcs12_data,
            to_bytes(__password),
            backend
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
        # skip variable in case some information can't be accessed
        skip = False

        # check if variable is supported is supported else skip
        check_extension = False

        # skip if something unexpected happens
        try:
            # map oid name to variables
            _name = to_text(extension.oid._name)
        except Exception:
            warnings.append(
                "Name of extension couldn't be accessed. Skipping unknown extension."
                )
            skip = True

        # check supported extension
        if not skip:
            for supported_name in SUPPORTED_EXTENSIONS:
                if supported_name in _name:
                    check_extension = True

        # skip if extension is not supported
        if not check_extension:
            skip = True

        if not skip:
            try:
                # create dict if extension has been found
                result['extensions'][to_text(_name)] = dict()

                # skip if dotte_string is not available
                try:
                    result['extensions'][_name]['_dotted_string'] = extension.oid.dotted_string
                except:
                    warnings.append('Couldn\'t find dotted_string. Skipping extension.')
                    skip = True

                # get critical value
                critical = to_text(extension.critical)
                result['extensions'][_name]['_critical'] = to_text(critical)

            except Exception as e:
                # if something went wrong skip this extension and its key values and
                # also create a warning
                warnings.append(
                    "Extension %s has been skipped due to unparsable name or values." % _name
                    )
                skip = True

        if not skip:
            # create new dictionaries for extensions and key values
            result['extensions'][_name]['_values'] = dict()

            # map with for loop key value in extension to results:
            for key, value in vars(extension.value).items():
                # check if key is supported in specified extension
                if check_supported_vars(key, _name):
                    if isinstance(value, bytes):
                        hex_str = binascii.hexlify(value).decode()
                        value = ':'.join(
                            hex_str[i:i + 2] for i in range(0, len(hex_str), 2)
                            ).upper()
                    result['extensions'][_name]['_values'][to_text(key)] = to_text(value)

        # set skip back to false
        skip = False
        check_extension = False

    return result, warnings


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

    # check if cryptography library is missing
    if not HAS_CRYPTOGRAPHY_PKCS12:
        module.fail_json(msg=missing_required_lib('cryptography >= 2.5'))

    __path = module.params['ca_dir'] + '/' + module.params['ca_cert']

    try:
        result, warnings = analyze_ca_cert(result, __path, module.params['password'])
    except ValueError as e:
        module.fail_json(msg='ValueError: %s' % to_native(e))
    except Exception as e:
        module.fail_json(msg='Exception: %s' % to_native(e))

    for warning in warnings:
        module.warn(warning)

    module.exit_json(**result)


def main():
    run_module()


if __name__ == '__main__':
    main()
