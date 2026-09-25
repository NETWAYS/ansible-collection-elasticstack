# Ansible Role: Beats

Installs and configures the Elastic [Beats](https://www.elastic.co/beats) on Linux systems: Filebeat, Auditbeat and Metricbeat. The role can run standalone or together with the other Elastic Stack roles. Beats can ship to Logstash or directly to Elasticsearch.

## Requirements

* The `community.crypto` collection (used to check certificate expiration).
* The Elastic repositories configured: use the [`repos`](../repos/README.md) role or provide them yourself.

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

Filebeat can read from several sources (log files, syslog, journald, Docker, modules). For the structure of `beats_filebeat_log_inputs`, `beats_filebeat_journald_inputs` and the other input variables, see the [Filebeat inputs documentation](docs/filebeat-inputs.md).

## Tags

Run only parts of the role with `--tags`:

* `configuration` (alias `beats_configuration`): (re)write the Filebeat and Auditbeat configuration without installing. Use `beats_filebeat_configuration` or `beats_auditbeat_configuration` to limit it to one of them.
* `certificates`: only generate and distribute the TLS certificates.
* `renew_beats_cert` / `renew_ca`: force renewal of the Beats certificate.

<!-- ANSIBLE DOCSMITH MAIN START -->
## Role variables<a id="variables"></a>

| Variable | Description |
|----------|-------------|
| `beats_filebeat`<br>**Type**: `bool`<br>**Default**: `true` | Install and manage Filebeat. |
| `beats_auditbeat`<br>**Type**: `bool`<br>**Default**: `false` | Install and manage Auditbeat. |
| `beats_metricbeat`<br>**Type**: `bool`<br>**Default**: `false` | Install and manage Metricbeat. |
| `beats_target_hosts`<br>**Type**: `list` of `str`<br>**Default**: `['localhost']` | Hosts the Beats ship to when the role runs standalone; with the other Elastic Stack roles the targets come from the inventory. Applies to whichever output a Beat uses, so set beats_elasticsearch_hosts or beats_logstash_hosts instead when the two outputs need different hosts. |
| `beats_elasticsearch_hosts`<br>**Type**: `list` of `str` | Elasticsearch hosts the Beats ship to. Defaults to the nodes from the elasticsearch group, or to beats_target_hosts when the role runs standalone. |
| `beats_logstash_hosts`<br>**Type**: `list` of `str` | Logstash hosts the Beats ship to. Defaults to the nodes from the logstash group, or to beats_target_hosts when the role runs standalone. |
| `beats_fields`<br>**Type**: `list` of `str` | Global fields added to the log and syslog (tcp/udp) inputs (not to the mysql, journald or docker inputs), given as a list of "key: value" strings. This is the global counterpart to the per-input fields. Unset by default. See the Filebeat inputs documentation. |
| `beats_logging`<br>**Type**: `str`<br>**Default**: `"file"` | Where the Beats log. Set to "file" to log into beats_logpath; any other value leaves the Beats built-in logging. |
| `beats_loglevel`<br>**Type**: `str`<br>**Default**: `"info"` | Log level for all Beats. |
| `beats_logpath`<br>**Type**: `str`<br>**Default**: `"/var/log/beats"` | Directory for the log files when beats_logging is "file". |
| `beats_filebeat_enable`<br>**Type**: `bool`<br>**Default**: `true` | Start and enable the Filebeat service. |
| `beats_filebeat_output`<br>**Type**: `str`<br>**Default**: `"logstash"`<br>**Choices**: `logstash`, `elasticsearch` | Where Filebeat sends its events. With "logstash" they pass through the Logstash pipelines and can be filtered and enriched there, which is what log lines usually need. With "elasticsearch" they go straight into the cluster. |
| `beats_filebeat_elastic_monitoring`<br>**Type**: `bool`<br>**Default**: `false` | Report Filebeat monitoring data through the Elastic Stack monitoring features. |
| `beats_filebeat_loadbalance`<br>**Type**: `bool`<br>**Default**: `true` | Enable load balancing for the Filebeat Logstash output. |
| `beats_filebeat_log_input`<br>**Type**: `bool`<br>**Default**: `true` | Read log files with the inputs from beats_filebeat_log_inputs. |
| `beats_filebeat_log_inputs`<br>**Type**: `dict`<br>**Default**: `{'messages': {'paths': ['/var/log/messages', '/var/log/syslog']}}` | Log files to read, keyed by a free name that becomes the filestream id. Each entry has paths and optional fields and multiline settings. See the Filebeat inputs documentation. |
| `beats_filebeat_syslog_tcp`<br>**Type**: `bool`<br>**Default**: `false` | Enable a TCP syslog input. |
| `beats_filebeat_syslog_tcp_port`<br>**Type**: `int`<br>**Default**: `514` | Port of the TCP syslog input. |
| `beats_filebeat_syslog_udp`<br>**Type**: `bool`<br>**Default**: `false` | Enable a UDP syslog input. |
| `beats_filebeat_syslog_udp_port`<br>**Type**: `int`<br>**Default**: `514` | Port of the UDP syslog input. |
| `beats_filebeat_journald`<br>**Type**: `bool`<br>**Default**: `false` | Collect logs from journald. Available since Filebeat 7.16. |
| `beats_filebeat_journald_inputs`<br>**Type**: `dict`<br>**Default**: `{'everything': {'id': 'everything'}}` | Journald inputs, keyed by a free name. Each entry has an id and optional include_matches filters. See the Filebeat inputs documentation. |
| `beats_filebeat_docker`<br>**Type**: `bool`<br>**Default**: `false` | Collect Docker container logs. Only works on Elastic Stack release 7. |
| `beats_filebeat_docker_ids`<br>**Type**: `str`<br>**Default**: `"*"` | IDs of the containers to collect logs from. |
| `beats_filebeat_mysql_slowlog_input`<br>**Type**: `bool`<br>**Default**: `false` | Collect the MySQL/MariaDB slow query log, including multiline handling. |
| `beats_filebeat_modules`<br>**Type**: `list` of `str` | List of Filebeat modules to enable (experimental). Unset by default. |
| `beats_auditbeat_enable`<br>**Type**: `bool`<br>**Default**: `true` | Start and enable the Auditbeat service. |
| `beats_auditbeat_output`<br>**Type**: `str`<br>**Default**: `"elasticsearch"`<br>**Choices**: `logstash`, `elasticsearch` | Where Auditbeat sends its events. Defaults to "elasticsearch" because audit events already arrive structured and gain nothing from passing through Logstash. Set it to "logstash" to route them through the pipelines anyway. |
| `beats_auditbeat_setup`<br>**Type**: `bool`<br>**Default**: `true` | Run the Auditbeat setup (index management, ingest pipelines and Kibana dashboards). Only effective with the elasticsearch output; loading the dashboards additionally requires Kibana to be reachable. |
| `beats_auditbeat_loadbalance`<br>**Type**: `bool`<br>**Default**: `true` | Enable load balancing for the Auditbeat Logstash output. |
| `beats_metricbeat_enable`<br>**Type**: `bool`<br>**Default**: `true` | Start and enable the Metricbeat service. |
| `beats_metricbeat_output`<br>**Type**: `str`<br>**Default**: `"elasticsearch"`<br>**Choices**: `logstash`, `elasticsearch` | Where Metricbeat sends its events. Defaults to "elasticsearch" because metrics already arrive structured and gain nothing from passing through Logstash. Set it to "logstash" to route them through the pipelines anyway. |
| `beats_metricbeat_modules`<br>**Type**: `list` of `str`<br>**Default**: `['system']` | Metricbeat modules to enable. |
| `beats_metricbeat_loadbalance`<br>**Type**: `bool`<br>**Default**: `true` | Enable load balancing for the Metricbeat Logstash output. |
| `beats_security`<br>**Type**: `bool`<br>**Default**: `false` | Activate TLS for the connections to the targets. Works with the other roles and elasticstack_full_stack to create certificates automatically, or with the beats_tls_* variables for custom certificates. |
| `beats_ca_dir`<br>**Type**: `str` | Base directory for the Beats certificate, key and CA file. The role fills it per variant (/opt/ca standalone, /etc/beats/certs in a full stack) if you did not set it. |
| `beats_tls_key`<br>**Type**: `str`<br>**Default**: `"{{ beats_ca_dir \| default('') }}/{{ inventory_hostname }}-beats.key"` | Path to the Beats private key. Defaults under beats_ca_dir; set it to bring your own. |
| `beats_tls_cert`<br>**Type**: `str`<br>**Default**: `"{{ beats_ca_dir \| default('') }}/{{ inventory_hostname }}-beats.crt"` | Path to the Beats certificate. Defaults under beats_ca_dir; set it to bring your own. |
| `beats_tls_cacert`<br>**Type**: `str`<br>**Default**: `"{{ beats_ca_dir \| default('') }}/ca.crt"` | Path to the CA certificate Beats trusts. Defaults under beats_ca_dir; set it to bring your own. |
| `beats_tls_key_passphrase`<br>**Type**: `str`<br>**Default**: `"BeatsChangeMe"` | Passphrase of the Beats private key. |
| `beats_cert_validity_period`<br>**Type**: `int`<br>**Default**: `1095` | Number of days the generated certificates are valid. |
| `beats_cert_expiration_buffer`<br>**Type**: `str`<br>**Default**: `"+30d"` | Renew the certificate when it would expire within this period. Uses the community.crypto check_period format (e.g. "+30d"), not a plain number. |
| `beats_cert_will_expire_soon`<br>**Type**: `bool`<br>**Default**: `false` | Set to true to force renewal of the Beats certificate. Alternatively run the playbook with the renew_beats_cert tag. |

<!-- ANSIBLE DOCSMITH MAIN END -->

## Shared variables

This role also uses the collection-wide `elasticstack_*` variables (e.g. `elasticstack_full_stack`, `elasticstack_variant`, `elasticstack_ca_host`, `elasticstack_ca_pass`, `elasticstack_release`, `elasticstack_version`, `elasticstack_elasticsearch_http_port`, `elasticstack_beats_port`). They are documented centrally with the [elasticstack role](../elasticstack/README.md).
