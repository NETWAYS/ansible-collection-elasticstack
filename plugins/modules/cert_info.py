#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright (c) 2023, Daniel Patrick <daniel.patrick@netways.de>
# GNU General Public License v3.0+ (see LICENSES/GPL-3.0-or-later.txt or
# https://www.gnu.org/licenses/gpl-3.0.txt)
# SPDX-License-Identifier: GPL-3.0-or-later

from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

DOCUMENTATION = r'''
---
module: cert_info
short_description: Retrieve information from a PKCS12 certificate
description:
  - Reads a PKCS12 certificate file and returns details such as issuer, subject,
    validity dates, serial number, and supported X.509 extensions.
  - Requires the C(cryptography) Python library (>= 2.5) on the target host.
version_added: "1.0.0"
author:
  - Daniel Patrick (@dpatrick)
requirements:
  - cryptography >= 2.5
options:
  path:
    description: Absolute path to the PKCS12 certificate file on the target host.
    type: str
    required: true
  passphrase:
    description: Passphrase to decrypt the PKCS12 file. Omit if the file is not encrypted.
    type: str
    required: false
    default: null
'''

EXAMPLES = r'''
- name: Get certificate information
  netways.elasticstack.cert_info:
    path: /etc/elasticsearch/certs/elastic-certificates.p12
  register: cert

- name: Get certificate info with passphrase
  netways.elasticstack.cert_info:
    path: /etc/elasticsearch/certs/elastic-certificates.p12
    passphrase: "{{ cert_passphrase }}"
  register: cert

- name: Show certificate expiry date
  ansible.builtin.debug:
    msg: "Certificate expires: {{ cert.not_valid_after }}"
'''

RETURN = r'''
changed:
  description: Always false, this module does not modify anything.
  type: bool
  returned: always
issuer:
  description: Common name of the certificate issuer.
  type: str
  returned: success
subject:
  description: Common name of the certificate subject.
  type: str
  returned: success
not_valid_before:
  description: Start of the certificate validity period.
  type: str
  returned: success
not_valid_after:
  description: End of the certificate validity period.
  type: str
  returned: success
serial_number:
  description: Serial number of the certificate.
  type: str
  returned: success
version:
  description: X.509 version of the certificate.
  type: str
  returned: success
extensions:
  description: Dictionary of supported X.509 extensions and their values.
  type: dict
  returned: success
'''

from ansible.module_utils.basic import (
    AnsibleModule,
    to_native
)

from ansible_collections.netways.elasticstack.plugins.module_utils.certs import (
    AnalyzeCertificate
)


def run_module():
    module_args = dict(
        path=dict(type='str', no_log=True, required=True),
        passphrase=dict(type='str', no_log=True, required=False, default=None)
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

    try:
        cert_info = AnalyzeCertificate(module, result)
        result = cert_info.return_result()
    except ValueError as e:
        module.fail_json(msg='ValueError: %s' % to_native(e))
    except Exception as e:
        module.fail_json(msg='Exception: %s: %s' % (to_native(type(e)), to_native(e)))

    module.exit_json(**result)


def main():
    run_module()


if __name__ == '__main__':
    main()
