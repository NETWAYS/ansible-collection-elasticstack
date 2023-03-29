# -*- coding: utf-8 -*-
# Copyright (c) 2023, Daniel Patrick <daniel.patrick@netways.de>
# GNU General Public License v3.0+ (see LICENSES/GPL-3.0-or-later.txt or
# https://www.gnu.org/licenses/gpl-3.0.txt)
# SPDX-License-Identifier: GPL-3.0-or-later

from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

from ansible.module_utils.basic import AnsibleModule, to_text, to_native

import datetime
import locale


def run_module():
    # define available arguments/parameters a user can pass to the module
    # set password and ca_dir to no_log for security
    module_args = dict(
        ca_dir=dict(type='str', no_log=True, required=True),
        password=dict(type='str', no_log=True, required=False, default=False),
        format=dict(type='str', required=False, default='%b %d %H:%M:%S %Y %Z'),
        language_code=dict(type='str', required=False, default=None),
        encoding=dict(type='str', required=False, default=None)
    )

    # parameters required together
    module = AnsibleModule(
        argument_spec=module_args,
        supports_check_mode=True,
        required_together=[['language_code', 'encoding']]
    )

    # seed the result dict
    result = dict(
        changed=False,
        enddate=''
    )

    # the AnsibleModule object
    module = AnsibleModule(
        argument_spec=module_args,
        supports_check_mode=True
    )

    # if the user is working with this module in only check mode we do not
    # want to make any changes to the environment, just return the current
    # state with no modifications
    if module.check_mode:
        module.exit_json(**result)

    # build openssl command to read certificate
    openssl_cmd = "openssl pkcs12"
    openssl_cmd += " -in '%s/elastic-stack-ca.p12'" % module.params['ca_dir']
    openssl_cmd += " -passin pass:'%s'" % (module.params['password'])
    openssl_cmd += " -clcerts"
    openssl_cmd += " -nokeys"

    # run command with the basic utils from AnsibleModules
    # run_command() has three returns which are
    # rc, stdout, and stderr
    rc, stdout, stderr = module.run_command(openssl_cmd)

    # check if command failed
    if rc != 0:
        result['stderr'] = to_text(stderr)
        module.fail_json(msg='Error: openssl: ', **result)

    cert_content = stdout

    # new command build to get the notAfter date
    # passed in last stdout to stdin
    openssl_cmd = "openssl x509 -noout -enddate"
    rc, stdout, stderr = module.run_command(openssl_cmd, data=cert_content)

    # check if command failed
    if rc != 0:
        result['stderr'] = to_text(stderr)
        module.fail_json(msg='Error: openssl: ', **result)

    # formatting to remove 'notAfter=' with awk from last result
    # passed in last stdout to stdin
    openssl_cmd = "awk -F'=' '{print $2}'"
    rc, stdout, stderr = module.run_command(openssl_cmd, data=stdout)

    # New commands to get more information about the CA can be
    # continued with the commented example code.

    # new command build to get notBefore date
    # openssl_cmd = "openssl x509 -noout -startdate"
    # rc, stdout, stderr = module.run_command(openssl_cmd, data=cert_content)

    # check if command failed
    if rc != 0:
        result['stderr'] = to_text(stderr)
        module.fail_json(msg='Error: awk: ', **result)

    # set locale, if given
    try:
        if module.params['language_code'] or module.params['encoding']:
            sequence = (module.params['language_code'], module.params['encoding'])
            locale.setlocale(locale.LC_ALL, sequence)
    except Exception as e:
        module.fail_json(msg='Exception: %s' % to_native(e))

    # get datetime object and convert it to string for return
    try:
        # use stdout from last command and the paramter
        # format from the module
        datetime_object = datetime.datetime.strptime(
            to_text(stdout.strip()),
            module.params['format']
            )
        result['enddate'] = to_native(datetime_object)
        module.exit_json(**result)
    except ValueError as e:
        module.fail_json(msg='ValueError: %s' % to_native(e))
    except Exception as e:
        module.fail_json(msg='Exception: %s' % to_native(e))


def main():
    run_module()


if __name__ == '__main__':
    main()
