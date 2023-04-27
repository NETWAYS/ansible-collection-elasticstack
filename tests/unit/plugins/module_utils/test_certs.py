import unittest
import sys
sys.path.append('/home/runner/.ansible/collections/')
from ansible_collections.netways.elasticstack.plugins.module_utils.certs import (
    check_supported_extensions,
    check_supported_keys,
    bytes_to_hex
)
from binascii import unhexlify


class TestCerts(unittest.TestCase):
    # 82532011c773a75e2a77c1df22e423b4c450bacf
    # b'\x82S \x11\xc7s\xa7^*w\xc1\xdf"\xe4#\xb4\xc4P\xba\xcf'
    def test_bytes_to_hex_byte_string(self):
        bytes_string = unhexlify('82532011c773a75e2a77c1df22e423b4c450bacf')
        # or
        #bytes_string = b'\x82S \x11\xc7s\xa7^*w\xc1\xdf"\xe4#\xb4\xc4P\xba\xcf'
        result = bytes_to_hex(bytes_str=bytes_string)
        #print("Bytes converted: " + str(result))
        self.assertEqual(result, '82:53:20:11:C7:73:A7:5E:2A:77:C1:DF:22:E4:23:B4:C4:50:BA:CF')

    def test_check_supported_extensions_with_supported_extension(self):
        result = check_supported_extensions(extension_name='authorityKeyIdentifier')
        #print("Extension is supported: " + str(result))
        self.assertEqual(result, True)

    def test_check_supported_extensions_with_unknown_extension(self):
        result = check_supported_extensions(extension_name='UnknownExtension')
        #print("Extension is supported: " + str(result))
        self.assertEqual(result, False)

    def test_check_supported_keys_with_known_key(self):
        result = check_supported_keys(key='_key_identifier', extension_name='authorityKeyIdentifier')
        #print("Key is supported: " + str(result))
        self.assertEqual(result, True)

    def test_check_supported_keys_with_unknown_key(self):
        result = check_supported_keys(key='_unknown', extension_name='authorityKeyIdentifier')
        #print("Key is supported: " + str(result))
        self.assertEqual(result, False)


if __name__ == '__main__':
    unittest.main()
