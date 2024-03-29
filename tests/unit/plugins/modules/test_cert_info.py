import json
import sys
import unittest
from unittest.mock import patch
from ansible.module_utils import basic
from ansible.module_utils.common.text.converters import to_bytes
sys.path.append('/home/runner/.ansible/collections/')
from ansible_collections.netways.elasticstack.plugins.modules import cert_info

certificate = {
    "changed": False,
    "extensions": {
        "authorityKeyIdentifier": {
            "_critical": "False",
            "_dotted_string": "2.5.29.35",
            "_values": {
                "_authority_cert_issuer": "None",
                "_authority_cert_serial_number": "None",
                "_key_identifier": "82:53:20:11:C7:73:A7:5E:2A:77:C1:DF:22:E4:23:B4:C4:50:BA:CF"
            }
        },
        "basicConstraints": {
            "_critical": "True",
            "_dotted_string": "2.5.29.19",
            "_values": {
                "_ca": "True",
                "_path_length": "None"
            }
        },
        "subjectKeyIdentifier": {
            "_critical": "False",
            "_dotted_string": "2.5.29.14",
            "_values": {
                "_digest": "82:53:20:11:C7:73:A7:5E:2A:77:C1:DF:22:E4:23:B4:C4:50:BA:CF"
            }
        }
    },
    "failed": False,
    "issuer": "Elastic Certificate Tool Autogenerated CA",
    "not_valid_after": "2026-03-28 01:58:02",
    "not_valid_before": "2023-03-29 01:58:02",
    "serial_number": "719770426243590812378787092632593850366518596520",
    "subject": "Elastic Certificate Tool Autogenerated CA",
    "version": "Version.v3"
    }


def set_module_args(args):
    """prepare arguments so that they will be picked up during module creation"""
    args = json.dumps({'ANSIBLE_MODULE_ARGS': args})
    basic._ANSIBLE_ARGS = to_bytes(args)


class AnsibleExitJson(Exception):
    """Exception class to be raised by module.exit_json and caught by the test case"""
    pass

class AnsibleFailJson(Exception):
    """Exception class to be raised by module.fail_json and caught by the test case"""
    pass


def exit_json(*args, **kwargs):
    """function to patch over exit_json; package return data into an exception"""
    if 'changed' not in kwargs:
        kwargs['changed'] = False

    if 'failed' not in kwargs:
        kwargs['failed'] = False

    checks_passed = True

    # check every item in certificate if it matches with the result
    # and if that fails, don't catch the Exception, so the test will fail
    for item in certificate:
        if certificate[item] != kwargs[item]:
            checks_passed = False
    
    if checks_passed:
        raise AnsibleExitJson(kwargs)


def fail_json(*args, **kwargs):
    """function to patch over fail_json; package return data into an exception"""
    kwargs['failed'] = True
    raise AnsibleFailJson(kwargs)


class TestCertInfo(unittest.TestCase):
    def setUp(self):
        self.mock_module_helper = patch.multiple(basic.AnsibleModule,
                                                 exit_json=exit_json,
                                                 fail_json=fail_json
                                                 )
        self.mock_module_helper.start()
        self.addCleanup(self.mock_module_helper.stop)

    def test_module_fail_when_required_args_missing(self):
        with self.assertRaises(AnsibleFailJson):
            set_module_args({})
            cert_info.main()

    def test_module_fail_when_wrong_path(self):
        with self.assertRaises(AnsibleFailJson):
            set_module_args({
                'path': 'wrong-path',
                'passphrase': 'PleaseChangeMe'
            })
            cert_info.main()

    def test_module_fail_when_wrong_password(self):
        with self.assertRaises(AnsibleFailJson):
            set_module_args({
                'path': 'molecule/plugins/files/es-ca/elastic-stack-ca.p12',
                'passphrase': 'wrong-password'
            })
            cert_info.main()

    def test_module_fail_when_password_missing_but_required(self):
        with self.assertRaises(AnsibleFailJson):
            set_module_args({
                'path': 'molecule/plugins/files/es-ca/elastic-stack-ca.p12'
            })
            cert_info.main()

    def test_module_exit_when_path_and_password_correct(self):
        with self.assertRaises(AnsibleExitJson):
            set_module_args({
                'path': 'molecule/plugins/files/es-ca/elastic-stack-ca.p12',
                'passphrase': 'PleaseChangeMe'
            })
            cert_info.main()


if __name__ == '__main__':
    unittest.main()
