# Ansible Role: Beats

Installs and configures the Elastic [Beats](https://www.elastic.co/beats) —
Filebeat, Auditbeat and Metricbeat — on Linux systems. The role can run
standalone or together with the other Elastic Stack roles. Beats can ship to
Logstash or directly to Elasticsearch.

## Requirements

* The `community.crypto` collection (used to check certificate expiration).
* The Beats you want to install must be available in your software repositories —
  use the [`repos`](../repos) role or provide them yourself.

## Example

```yaml
- name: Install Beats
  hosts: beats
  collections:
    - netways.elasticstack
  roles:
    - repos
    - beats
```

## Filebeat inputs

Filebeat can read from several sources (log files, syslog, journald, Docker,
modules). For the structure of `beats_filebeat_log_inputs`,
`beats_filebeat_journald_inputs` and the other input variables, see the
[Filebeat inputs documentation](docs/filebeat-inputs.md).

## Tags

Run only parts of the role with `--tags`:

* `configuration` (alias `beats_configuration`) — (re)write the Filebeat and Auditbeat configuration without installing. Use `beats_filebeat_configuration` or `beats_auditbeat_configuration` to limit it to one of them.
* `certificates` — only generate and distribute the TLS certificates.
* `renew_beats_cert` / `renew_ca` — force renewal of the Beats certificate.

<!-- ANSIBLE DOCSMITH MAIN START -->
## Role variables<a id="variables"></a>

| Variable | Type | Default | Choices | Description |
|----------|------|---------|---------|-------------|
| `beats_filebeat` | `bool` | `true` | — | Install and manage Filebeat. |
| `beats_auditbeat` | `bool` | `false` | — | Install and manage Auditbeat. |
| `beats_metricbeat` | `bool` | `false` | — | Install and manage Metricbeat. |
| `beats_target_hosts` | `list` of `str` | `['localhost']` | — | Hosts the Beats ship to. Only used when the role runs standalone; with the other Elastic Stack roles the targets are determined automatically. |
| `beats_fields` | `list` of `str` | N/A | — | Fields added to every input, given as a list of "key: value" strings (the global counterpart to the per-input fields). Unset by default. See the Filebeat inputs documentation. |
| `beats_logging` | `str` | `"file"` | — | Where the Beats log. Set to "file" to log into beats_logpath; any other value leaves the Beats built-in logging. |
| `beats_loglevel` | `str` | `"info"` | — | Log level for all Beats. |
| `beats_logpath` | `str` | `"/var/log/beats"` | — | Directory for the log files when beats_logging is "file". |
| `beats_filebeat_enable` | `bool` | `true` | — | Start and enable the Filebeat service. |
| `beats_filebeat_output` | `str` | `"logstash"` | `logstash`, `elasticsearch` | Where Filebeat sends its events. |
| `beats_filebeat_elastic_monitoring` | `bool` | `false` | — | Report Filebeat monitoring data through the Elastic Stack monitoring features. |
| `beats_filebeat_loadbalance` | `bool` | `true` | — | Enable load balancing for the Filebeat Logstash output. |
| `beats_filebeat_log_input` | `bool` | `true` | — | Read log files with the inputs from beats_filebeat_log_inputs. |
| `beats_filebeat_log_inputs` | `dict` | `{'messages': {'paths': ['/var/log/messages', '/var/log/syslog']}}` | — | Log files to read, keyed by a free name that becomes the filestream id. Each entry has paths and optional fields and multiline settings. See the Filebeat inputs documentation. |
| `beats_filebeat_syslog_tcp` | `bool` | `false` | — | Enable a TCP syslog input. |
| `beats_filebeat_syslog_tcp_port` | `int` | `514` | — | Port of the TCP syslog input. |
| `beats_filebeat_syslog_udp` | `bool` | `false` | — | Enable a UDP syslog input. |
| `beats_filebeat_syslog_udp_port` | `int` | `514` | — | Port of the UDP syslog input. |
| `beats_filebeat_journald` | `bool` | `false` | — | Collect logs from journald. Available since Filebeat 7.16. |
| `beats_filebeat_journald_inputs` | `dict` | `{'everything': {'id': 'everything'}}` | — | Journald inputs, keyed by a free name. Each entry has an id and optional include_matches filters. See the Filebeat inputs documentation. |
| `beats_filebeat_docker` | `bool` | `false` | — | Collect Docker container logs. Only works on Elastic Stack release 7. |
| `beats_filebeat_docker_ids` | `str` | `"*"` | — | IDs of the containers to collect logs from. |
| `beats_filebeat_mysql_slowlog_input` | `bool` | `false` | — | Collect the MySQL/MariaDB slow query log, including multiline handling. |
| `beats_filebeat_modules` | `list` of `str` | N/A | — | List of Filebeat modules to enable (experimental). Unset by default. |
| `beats_auditbeat_enable` | `bool` | `true` | — | Start and enable the Auditbeat service. |
| `beats_auditbeat_output` | `str` | `"elasticsearch"` | `logstash`, `elasticsearch` | Where Auditbeat sends its events. |
| `beats_auditbeat_setup` | `bool` | `true` | — | Run the Auditbeat setup (index management and pipelines). Only effective with the elasticsearch output. |
| `beats_auditbeat_loadbalance` | `bool` | `true` | — | Enable load balancing for the Auditbeat Logstash output. |
| `beats_metricbeat_enable` | `bool` | `true` | — | Start and enable the Metricbeat service. |
| `beats_metricbeat_output` | `str` | `"elasticsearch"` | `logstash`, `elasticsearch` | Where Metricbeat sends its events. |
| `beats_metricbeat_modules` | `list` of `str` | `['system']` | — | Metricbeat modules to enable. |
| `beats_metricbeat_loadbalance` | `bool` | `true` | — | Enable load balancing for the Metricbeat Logstash output. |
| `beats_security` | `bool` | `false` | — | Activate TLS for the connections to the targets. Works with the other roles and elasticstack_full_stack to create certificates automatically, or with the beats_tls_* variables for custom certificates. |
| `beats_ca_dir` | `str` | N/A | — | Base directory for custom CA certificates and keys. Unset by default; the role fills it depending on the stack variant (/opt/ca standalone, or /etc/beats/certs in a full stack). |
| `beats_tls_key` | `str` | `"{{ beats_ca_dir | default('') }}/{{ inventory_hostname }}-beats.key"` | — | Path to the private key file for custom certificates. |
| `beats_tls_cert` | `str` | `"{{ beats_ca_dir | default('') }}/{{ inventory_hostname }}-beats.crt"` | — | Path to the certificate for custom certificates. |
| `beats_tls_cacert` | `str` | `"{{ beats_ca_dir | default('') }}/ca.crt"` | — | Path to the CA certificate for custom certificates. |
| `beats_tls_key_passphrase` | `str` | `"BeatsChangeMe"` | — | Passphrase of the private key. |
| `beats_cert_validity_period` | `int` | `1095` | — | Number of days the generated certificates are valid. |
| `beats_cert_expiration_buffer` | `str` | `"+30d"` | — | Renew the certificate when it would expire within this period. Uses the community.crypto check_period format (e.g. "+30d"), not a plain number. |
| `beats_cert_will_expire_soon` | `bool` | `false` | — | Set to true to force renewal of the Beats certificate. Alternatively run the playbook with the renew_beats_cert tag. |

<!-- ANSIBLE DOCSMITH MAIN END -->

## Shared variables

This role also uses the collection-wide `elasticstack_*` variables (e.g.
`elasticstack_full_stack`, `elasticstack_variant`, `elasticstack_ca_host`,
`elasticstack_ca_pass`, `elasticstack_release`, `elasticstack_version`,
`elasticstack_elasticsearch_http_port`, `elasticstack_beats_port`). They are
documented centrally with the [elasticsearch role](../../docs/role-elasticsearch.md).
