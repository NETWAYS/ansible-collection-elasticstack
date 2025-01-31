# Documentation: netways.elasticstack module_utils

## `netways.elasticstack.certs` functions

### `bytes_to_hex()` function

Since binascii.hexlify doesn't support a second parameter, which would define a seperator (e.g. ":") for hex strings in older Python versions like 2.6 and 2.7, we implemeted a small function to get similar results.

**Parameter:** A __bytes__ string that represent a hexadecimal value (e.g. b'\\x82S \\x11\\xc7s\\xa7^*w\\xc1\\xdf\"\\xe4#\\xb4\\xc4P\\xba\\xcf')

**Return:** A hexadecimal __string__ seperated by colons (e.g. "82:53:20:11:C7:73:A7:5E:2A:77:C1:DF:22:E4:23:B4:C4:50:BA:CF") 

### `check_supported_extensions()` function

A function to check if the extension is supported. Returns true if extension name is found in `SUPPORTED_EXTENSIONS` dict.

**Parameter:** The extension name as __string__.

**Return:** Returns a __bool__.

### `check_supported_keys` function

A function to check if the extensions key is supported. Returns true if extensions key is found in `SUPPORTED_EXTENSIONS` dict.

**Parameter:** The key name as __string__.

**Return:** Returns a __bool__.

### `AnalyzeCertificate()` object

An object to load the certificate and to gather information about it.

**Parameter:** The path (required) to the certificate and the passphrase (optional), both as __string__.

**Return:** Returns the result dict to the Ansible module.
