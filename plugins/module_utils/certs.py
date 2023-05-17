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


class AnalyzeCertificate():
    def __init__(self, module, result):
        self.module = module
        self.result = result
        self.__passphrase = self.module.params['passphrase']
        self.__path = self.module.params['path']
        self.__cert = None
        self.__private_key = None
        self.__additional_certs = None
        self.load_certificate()
        self.load_info()

    def load_certificate(self):
        # track if module can load pkcs12
        loaded = False
        # check if cryptography library is missing
        if not HAS_CRYPTOGRAPHY_PKCS12:
            self.module.fail_json(
                msg=missing_required_lib('cryptography >= 2.5')
                )
        # read the pkcs12 file
        try:
            with open(self.__path, 'rb') as f:
                pkcs12_data = f.read()
        except IOError as e:
            self.module.fail_json(
                msg='IOError: %s' % (to_native(e))
                )
        # try to load with 2 parameters
        # for cryptography >= 3.1.x
        try:
            __pkcs12_tuple = pkcs12.load_key_and_certificates(
                pkcs12_data,
                to_bytes(self.__passphrase),
                )
            loaded = True
        except Exception:
            self.module.log(
                msg="Couldn't load certificate without backend. Trying with backend."
                )
        # try to load with 3 parameters for
        # cryptography >= 2.5.x and <= 3.0.x
        if not loaded:
            # create backend object
            backend = default_backend()
            # call load_key_and_certificates with 3 paramters
            __pkcs12_tuple = pkcs12.load_key_and_certificates(
                pkcs12_data,
                to_bytes(self.__passphrase),
                backend
                )
            self.module.log(
                msg="Loaded certificate with backend."
                )
        # map loaded certificate to object
        self.__private_key = __pkcs12_tuple[0]
        self.__cert = __pkcs12_tuple[1]
        self.__additional_certs = __pkcs12_tuple[2]

    def load_info(self):
        self.general_info()
        self.extensions_info()

    def general_info(self):
        # map object values to result dict
        issuer = to_text(self.__cert.issuer.get_attributes_for_oid(
            NameOID.COMMON_NAME)[0].value
            )
        subject = to_text(self.__cert.subject.get_attributes_for_oid(
            NameOID.COMMON_NAME)[0].value
            )
        self.result['issuer'] = to_text(issuer)
        self.result['subject'] = to_text(subject)
        self.result['not_valid_after'] = to_text(self.__cert.not_valid_after)
        self.result['not_valid_before'] = to_text(self.__cert.not_valid_before)
        self.result['serial_number'] = to_text(self.__cert.serial_number)
        self.result['version'] = to_text(self.__cert.version)

    def extensions_info(self):
        try:
            # read and map every extension in certificate.extensions
            for extension in self.__cert.extensions:
                # check if extension is supported bool
                supported_extension = False
                # map oid/extension name to variables
                name = to_text(extension.oid._name)
                # check if extension is in supported extensions by name
                supported_extension = check_supported_extensions(name)
                if supported_extension:
                    # create dict
                    self.result['extensions'][name] = dict()
                    # get dotted string
                    dotted_string = extension.oid.dotted_string
                    self.result['extensions'][name]['_dotted_string'] = to_text(dotted_string)
                    # get critical value
                    critical = to_text(extension.critical)
                    self.result['extensions'][name]['_critical'] = to_text(critical)
                self.extensions_values_info(name, extension)
        except Exception as e:
            # if something went wrong skip this extension and its key values and
            # also create a warning
            warning = "Error type: %s. Error message: %s" % (type(e), e)
            self.module.warn(to_native(warning))

    def extensions_values_info(self, name, extension):
        try:
            # create new dictionary for extension and keys/values
            self.result['extensions'][name]['_values'] = dict()
            # map with for loop key value in extension to results:
            for key, value in vars(extension.value).items():
                # check if key is supported in specified extension
                if check_supported_keys(key, name):
                    # check if bytes and if true convert to hex
                    if isinstance(value, bytes):
                        value = bytes_to_hex(value)
                    self.result['extensions'][name]['_values'][to_text(key)] = to_text(value)
        except Exception as e:
            warning = "Error type: %s. Error message: %s" % (type(e), e)
            self.module.warn(to_native(warning))

    def return_result(self):
        return self.result
