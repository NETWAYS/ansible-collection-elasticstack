import json
import sys
import unittest
from unittest.mock import patch
from ansible.module_utils import basic
from ansible.module_utils.common.text.converters import to_bytes
sys.path.append('/home/daniel/.ansible/collections')
from ansible_collections.netways.elasticstack.plugins.modules import cert_info

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
    raise AnsibleExitJson(kwargs)


def fail_json(*args, **kwargs):
    """function to patch over fail_json; package return data into an exception"""
    kwargs['failed'] = True
    raise AnsibleFailJson(kwargs)


#def get_bin_path(self, arg, required=False):
#    """Mock AnsibleModule.get_bin_path"""
#    if arg.endswith('my_command'):
#        return '/usr/bin/my_command'
#    else:
#        if required:
#            fail_json(msg='%r not found !' % arg)


class TestCertInfo(unittest.TestCase):

    def setUp(self):
        self.mock_module_helper = patch.multiple(basic.AnsibleModule,
                                                 exit_json=exit_json,
                                                 fail_json=fail_json#,
                                                 #get_bin_path=get_bin_path
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
                'path': 'molecule/plugins/es-ca/elastic-stack-ca.p12',
                'passphrase': 'wrong-password'
            })
            cert_info.main()

    def test_module_fail_when_password_missing_but_required(self):
        with self.assertRaises(AnsibleFailJson):
            set_module_args({
                'path': 'molecule/plugins/es-ca/elastic-stack-ca.p12'
            })
            cert_info.main()

    def test_module_exit_when_path_and_password_correct(self):
        with self.assertRaises(AnsibleExitJson):
            set_module_args({
                'path': 'molecule/plugins/es-ca/elastic-stack-ca.p12',
                'passphrase': 'PleaseChangeMe'
            })
            cert_info.main()

#    def test_module_result(self):
#        with self.assertRaises(AnsibleExitJson):
#            set_module_args({
#                'path': 'molecule/plugins/es-ca/elastic-stack-ca.p12',
#                'passphrase': 'PleaseChangeMe'
#            })
#            cert_info.main()

if __name__ == '__main__':
    unittest.main()