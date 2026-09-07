# Documentation: netways.elasticstack module_utils

## Overview
- [`certs` module_util](#netwayselasticstackcerts-function)

## `netways.elasticstack.certs` function

### `bytes_to_hex()` function

Since binascii.hexlify doesn't support a second parameter, which would define a seperator (e.g. ":") for hex strings in older Python versions like 2.6 and 2.7, we implemeted a small function to get similar results.

**Parameter:** A __bytes__ object that represent a hexadecimal value (e.g. b'\\x82S \\x11\\xc7s\\xa7^*w\\xc1\\xdf\"\\xe4#\\xb4\\xc4P\\xba\\xcf')

**Return:** A hexadecimal __string__ seperated by colons (e.g. "82:53:20:11:C7:73:A7:5E:2A:77:C1:DF:22:E4:23:B4:C4:50:BA:CF") 

### `check_supported_extensions()` function

A function to check if the extension is supported. Returns true if extension name is found in `SUPPORTED_EXTENSIONS` dict.

**Parameter:** The extension name as __string__.

**Return:** Returns a __bool__.

### `check_supported_keys` function

A function to check if the extensions key is supported. Returns true if the key is listed under
the given extension in the `SUPPORTED_EXTENSIONS` dict. Unlike `check_supported_extensions()`
this compares exactly, not by substring.

**Parameter:** Two, in this order: the key name as __string__, and the extension name as
__string__. The extension name has to be a key of `SUPPORTED_EXTENSIONS`, otherwise the lookup
raises a `KeyError`.

**Return:** Returns a __bool__.

### `AnalyzeCertificate()` object

An object to load the certificate and to gather information about it. Constructing it already
does the work: it reads the file and fills the result dict, so there is no separate call to
start the analysis.

**Parameter:** Two, in this order: the `AnsibleModule` __object__ and the result __dict__ to
fill. The certificate path and the passphrase are not passed in, the object reads them from
`module.params`. It also uses the module to log, to warn and to fail.

**Return:** The constructor returns nothing, it writes into the result dict it was given.
`return_result()` hands that dict back to the module, which passes it to `exit_json()`.
