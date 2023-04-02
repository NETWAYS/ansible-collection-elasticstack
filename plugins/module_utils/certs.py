# -*- coding: utf-8 -*-

# Copyright (c) 2023, Daniel Patrick <daniel.patrick@netways.de>
# GNU General Public License v3.0+ (see LICENSES/GPL-3.0-or-later.txt or
# https://www.gnu.org/licenses/gpl-3.0.txt)
# SPDX-License-Identifier: GPL-3.0-or-later

from __future__ import absolute_import, division, print_function
__metaclass__ = type

from ansible.module_utils.basic import (
    missing_required_lib,
    to_text,
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


# function returns and converts bytes to a hex string separated with ":"
# and is a Python 2.6 and 2.7 compatibility patch. hexlify() does not
# support a second parameter (a seperator e.g. ":") in this versions
def bytes_to_hex(bytes_str):
    # convert from bytes to ascii
    ascii_hex_str = binascii.hexlify(bytes_str).decode()
    # seperate by ":" every two characters and upper()
    value = ':'.join(
        ascii_hex_str[i:i + 2] for i in range(0, len(ascii_hex_str), 2)
        ).upper()
    return value


# function returns True (bool) if extension_name is in SUPPORTED_EXTENSIONS
def check_supported_extensions(extension_name):
    check_extension = False
    for supported_name in SUPPORTED_EXTENSIONS:
        if supported_name in extension_name:
            check_extension = True
    return check_extension


# function returns True (bool) if key is under supported keys in SUPPORTED_EXTENSIONS
def check_supported_keys(key, extension_name):
    check_key = False
    for supported_key in SUPPORTED_EXTENSIONS[extension_name]:
        if supported_key == key:
            check_key = True
    return check_key


# analyze pkcs12 cert created by Elastic stack cert util
def analyze_cert(module, result, __path, __password=None):
    loaded = False

    # check if cryptography library is missing
    if not HAS_CRYPTOGRAPHY_PKCS12:
        module.fail_json(msg=missing_required_lib('cryptography >= 2.5'))

    # read the pkcs12 file
    with open(__path, 'rb') as f:
        pkcs12_data = f.read()

    # try to load with 2 parameters
    # for cryptography >= 3.1.x
    try:
        __privatekey, __certificate, __additional_certificates = pkcs12.load_key_and_certificates(
            pkcs12_data,
            to_bytes(__password),
            )
        loaded = True
    except Exception:
        pass

    # try to load with 3 parameters for
    # cryptography >= 2.5.x and <= 3.0.x
    if not loaded:
        # create backend object
        backend = default_backend()
        # call load_key_and_certificates with 3 paramters
        __privatekey, __certificate, __additional_certificates = pkcs12.load_key_and_certificates(
            pkcs12_data,
            to_bytes(__password),
            backend
            )

    # map object values to result dict
    issuer = to_text(__certificate.issuer.get_attributes_for_oid(
        NameOID.COMMON_NAME)[0].value
        )
    subject = to_text(__certificate.subject.get_attributes_for_oid(
        NameOID.COMMON_NAME)[0].value
        )
    result['issuer'] = to_text(issuer)
    result['not_valid_after'] = to_text(__certificate.not_valid_after)
    result['not_valid_before'] = to_text(__certificate.not_valid_before)
    result['serial_number'] = to_text(__certificate.serial_number)
    result['subject'] = to_text(subject)
    result['version'] = to_text(__certificate.version)

    # read and map every extension in certificate.extensions
    for extension in __certificate.extensions:
        # skip variable in case some information can't be accessed
        skip = False

        # check if extension is supported bool
        supported_extension = False

        # skip if something unexpected happens
        try:
            # map oid/extension name to variables
            _name = to_text(extension.oid._name)
        except Exception:
            module.warn(
                "Name of extension couldn't be accessed. Skipping unknown extension."
                )
            skip = True

        # check if extension is in supported extensions by name
        if not skip:
            supported_extension = check_supported_extensions(_name)

        # skip if extension is not supported
        if not supported_extension:
            skip = True

        if not skip:
            try:
                # create dict if extension has been found
                result['extensions'][to_text(_name)] = dict()

                # skip if dotted_string is not available
                try:
                    result['extensions'][_name]['_dotted_string'] = extension.oid.dotted_string
                except:
                    module.warn('Couldn\'t find dotted_string. Skipping value.')
                    skip = True

                # get critical value
                critical = to_text(extension.critical)
                result['extensions'][_name]['_critical'] = to_text(critical)

            except Exception as e:
                # if something went wrong skip this extension and its key values and
                # also create a warning
                module.warn(
                    "Extension %s has been skipped due to unparsable name or values." % _name
                    )
                skip = True

        if not skip:
            # create new dictionary for extension and keys/values
            result['extensions'][_name]['_values'] = dict()

            # map with for loop key value in extension to results:
            for key, value in vars(extension.value).items():
                # check if key is supported in specified extension
                if check_supported_keys(key, _name):
                    # check if bytes and if true convert to hex
                    if isinstance(value, bytes):
                        value = bytes_to_hex(value)
                    result['extensions'][_name]['_values'][to_text(key)] = to_text(value)

    return result
