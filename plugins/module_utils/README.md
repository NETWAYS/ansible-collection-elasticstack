# Documentation: netways.elasticstack module_utils

Shared code used by the modules in `plugins/modules/`. `ansible-doc` does not read this
directory, which is why it is documented here by hand instead of in a `DOCUMENTATION` block.

## Overview
- [`certs`](#certs), reading PKCS12 certificates. Used by `cert_info`.
- [`api`](#api), the Elasticsearch client. Used by `elasticsearch_role` and `elasticsearch_user`.
- [`elasticsearch_role`](#elasticsearch_role), the role logic behind the `elasticsearch_role` module.
- [`elasticsearch_user`](#elasticsearch_user), the user logic behind the `elasticsearch_user` module.

## `certs`<a id="certs"></a>

Requires the `cryptography` library (>= 2.5). The module that uses it fails with
`missing_required_lib()` when it is absent.

`SUPPORTED_EXTENSIONS` is a dict at the top of the file. It maps an X.509 extension name to the
list of its attribute names that may be reported. Nothing outside it ever reaches the result, so
extending the module means extending that dict.

### `bytes_to_hex()` function

Since binascii.hexlify doesn't support a second parameter, which would define a separator (e.g. ":") for hex strings in older Python versions like 2.6 and 2.7, we implemented a small function to get similar results.

**Parameter:** A __bytes__ object that represent a hexadecimal value (e.g. b'\\x82S \\x11\\xc7s\\xa7^*w\\xc1\\xdf\"\\xe4#\\xb4\\xc4P\\xba\\xcf')

**Return:** A hexadecimal __string__ separated by colons (e.g. "82:53:20:11:C7:73:A7:5E:2A:77:C1:DF:22:E4:23:B4:C4:50:BA:CF") 

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

A broken or unreadable extension does not fail the module. It is skipped with `module.warn()`,
so a task can succeed with fewer extensions in the result than the certificate contains.

## `api`<a id="api"></a>

Builds the Elasticsearch client for the two Elasticsearch modules. Requires the `elasticsearch`
Python library, currently a version below 9.

### `HAS_ELASTICSEARCH` and `ELASTICSEARCH_IMPORT_ERROR`

Set while the file is imported. `HAS_ELASTICSEARCH` is a __bool__,
`ELASTICSEARCH_IMPORT_ERROR` holds the formatted traceback as a __string__ or `None`. A module
checks the flag and reports the traceback, so a missing library produces a readable message
instead of an import error.

### `Api.new_client_basic_auth()` static method

Returns a connected `Elasticsearch` client authenticated with username and password.

**Parameter:** Five keyword arguments: `host` (URL including protocol and port), `auth_user`,
`auth_pass`, `ca_certs` (path to a CA file, or `None`) and `verify_certs`.

**Return:** An `Elasticsearch` __object__. Raises `ImportError` when the library is missing.

The SSL context it builds sets `check_hostname` and `verify_mode` to false before `verify_certs`
is handed to the client, so the hostname in the certificate is not checked.

## `elasticsearch_role`<a id="elasticsearch_role"></a>

### `Role()` object

The whole logic of the `elasticsearch_role` module. Constructing it already does the work: it
builds the client, decides between create, update and delete, and fills the result dict.

**Parameter:** Ten keyword arguments: the result __dict__ to fill, `role_name`, `cluster`,
`indicies`, `state`, and the connection arguments `host`, `auth_user`, `auth_pass`,
`verify_certs` and `ca_certs`.

**Return:** The constructor returns nothing. `return_result()` hands the result dict back to the
module, which passes it to `exit_json()`.

Changes are detected against the API, not against the arguments. `handle_present()` reads the
role, writes it, and compares the response before and after, so `changed` stays false when the
role already looked that way. `handle_absent()` only deletes a role that the API reports as
existing.

## `elasticsearch_user`<a id="elasticsearch_user"></a>

### `User()` object

The whole logic of the `elasticsearch_user` module, built the same way as `Role()` above.

**Parameter:** Thirteen keyword arguments: the result __dict__ to fill, `user_name`,
`full_name`, `password`, `email`, `roles`, `enabled`, `state`, and the connection arguments
`host`, `auth_user`, `auth_pass`, `verify_certs` and `ca_certs`.

**Return:** The constructor returns nothing. `return_result()` hands the result dict back to the
module, which passes it to `exit_json()`.

Changes are detected the same way, by comparing the API response before and after the write.
A password cannot be read back, so setting the same password again is not reported as a change,
while setting a different one is not detected either.
