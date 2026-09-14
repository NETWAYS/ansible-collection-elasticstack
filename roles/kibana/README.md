# Ansible Role: Kibana

Installs and configures [Kibana](https://www.elastic.co/kibana) on Linux systems.
The role manages `kibana.yml` and can enable TLS for the Kibana web interface,
using a certificate you provide. In a full stack setup together with the
elasticsearch role, it also configures the connection to Elasticsearch — the TLS
trust and the `kibana_system` credentials — using the Elasticsearch CA.

## Requirements

* The Elastic repositories configured — use the [`repos`](../repos) role.
* A reachable Elasticsearch instance for Kibana to connect to.
* For browser-facing TLS (`kibana_tls: true`): a certificate and key from a CA your
  users trust (corporate PKI or a public CA), provided via `kibana_tls_cert` and
  `kibana_tls_key`. The role does **not** generate a browser certificate.

## Example

```yaml
- name: Install Kibana
  hosts: kibana
  collections:
    - netways.elasticstack
  roles:
    - repos
    - kibana
```

By default Kibana only logs to the journal, readable with
`journalctl -u kibana`. Set `kibana_manage_logging` to write a log file that
Kibana rotates itself, no logrotate needed:

```yaml
- name: Install Kibana with file logging
  hosts: kibana
  collections:
    - netways.elasticstack
  vars:
    kibana_manage_logging: true
    kibana_logpath: /var/log/kibana
    kibana_loglevel: info
    kibana_logging_rotate_size: 100mb
    kibana_logging_rotate_keep: 10
  roles:
    - repos
    - kibana
```

This writes `/var/log/kibana/kibana.log` in a human readable layout and keeps
ten rotated files. Set `kibana_logging_layout` to `json` when a log shipper
reads the file, and `kibana_logging_console` to `false` to stop logging to the
journal as well.

## Tags

Run only parts of the role with `--tags`:

* `certificates` — only generate and distribute the TLS certificates.
* `renew_kibana_cert` / `renew_ca` — force renewal of the Kibana certificate.

<!-- ANSIBLE DOCSMITH MAIN START -->
## Role variables<a id="variables"></a>

| Variable | Type | Default | Choices | Description |
|----------|------|---------|---------|-------------|
| `kibana_enable` | `bool` | `true` | — | Start and enable the Kibana service. |
| `kibana_config_backup` | `bool` | `true` | — | Keep a backup of kibana.yml whenever the role changes it. |
| `kibana_manage_yaml` | `bool` | `true` | — | Manage and overwrite kibana.yml. |
| `kibana_elasticsearch_hosts` | `list` of `str` | N/A | — | Elasticsearch hosts Kibana connects to. Defaults to the nodes from the elasticsearch group, or localhost when used standalone. |
| `kibana_security` | `bool` | `true` | — | Enable X-Pack security: connect to Elasticsearch over HTTPS with authentication and set up the encryption keys. Only effective in a full stack setup with the elastic variant. |
| `kibana_sniff_on_start` | `bool` | `false` | — | Ask Elasticsearch for the list of nodes at startup (elasticsearch.sniffOnStart). |
| `kibana_sniff_on_connection_fault` | `bool` | `false` | — | Update the list of Elasticsearch nodes on connection fault (elasticsearch.sniffOnConnectionFault). |
| `kibana_sniff_interval` | `str` | N/A | — | Interval between sniffing attempts (elasticsearch.sniffInterval, in milliseconds). Unset by default. |
| `kibana_tls` | `bool` | `false` | — | Enable TLS on the Kibana server itself (server.ssl). |
| `kibana_tls_cert` | `str` | `"/etc/kibana/certs/cert.pem"` | — | Path to the certificate for the Kibana server TLS. |
| `kibana_tls_key` | `str` | `"/etc/kibana/certs/key.pem"` | — | Path to the private key for the Kibana server TLS. |
| `kibana_tls_key_passphrase` | `str` | `"PleaseChangeMe"` | — | Passphrase for the generated Kibana security certificate (X-Pack, full stack). Overridden by elasticstack_cert_pass when that is set. |
| `kibana_cert_validity_period` | `int` | `1095` | — | Number of days the generated certificates are valid. |
| `kibana_cert_expiration_buffer` | `int` | `30` | — | Renew the certificate when its remaining validity (in days) drops below this value. |
| `kibana_cert_will_expire_soon` | `bool` | `false` | — | Set to true to force renewal of the Kibana certificate. Alternatively run the playbook with the renew_kibana_cert tag. |
| `kibana_manage_logging` | `bool` | `false` | — | Manage Kibana's own logging configuration and write log files to disk. When disabled, Kibana keeps its default behaviour and only logs to the journal. |
| `kibana_logpath` | `str` | `"/var/log/kibana"` | — | Directory for the Kibana log files. The role creates it for the kibana user when kibana_manage_logging is enabled. |
| `kibana_logfile` | `str` | `"kibana.log"` | — | Name of the log file inside kibana_logpath. |
| `kibana_loglevel` | `str` | `"info"` | `all`, `trace`, `debug`, `info`, `warn`, `error`, `fatal`, `off` | Log level of the root logger (logging.root.level). |
| `kibana_logging_layout` | `str` | `"pattern"` | `pattern`, `json` | Layout of the log file. Use "pattern" for human readable logs and "json" when the file is picked up by a log shipper. |
| `kibana_logging_console` | `bool` | `true` | — | Keep logging to the console (and therefore the journal) in addition to the log file. Set to false to log to the file only. |
| `kibana_logging_rotate_policy` | `str` | `"size-limit"` | `size-limit`, `time-interval` | Rotation policy of the log file. Kibana supports only one policy per appender, either by size (kibana_logging_rotate_size) or by time (kibana_logging_rotate_interval). |
| `kibana_logging_rotate_size` | `str` | `"100mb"` | — | Size at which the log file is rotated. Only used when kibana_logging_rotate_policy is "size-limit". |
| `kibana_logging_rotate_interval` | `str` | `"24h"` | — | Interval at which the log file is rotated. Only used when kibana_logging_rotate_policy is "time-interval". |
| `kibana_logging_rotate_keep` | `int` | `10` | — | Number of rotated log files to keep (strategy max). |
| `kibana_extra_config` | `str` | N/A | — | Extra configuration appended verbatim to kibana.yml (YAML). Unset by default. |
| `kibana_freshstart` | `dict` | `{'changed': False}` | — | Internal state used by the role to detect a fresh install. Do not set manually. |

<!-- ANSIBLE DOCSMITH MAIN END -->

## Shared variables

This role also uses the collection-wide `elasticstack_*` variables (e.g.
`elasticstack_full_stack`, `elasticstack_variant`, `elasticstack_release`,
`elasticstack_ca_host`, `elasticstack_ca_pass`, `elasticstack_kibana_host`,
`elasticstack_kibana_port`, `elasticstack_elasticsearch_http_port`). They are
documented centrally with the [elasticstack role](../elasticstack/README.md).
