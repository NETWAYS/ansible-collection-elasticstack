# Ansible Role: Logstash

Installs and configures [Logstash](https://www.elastic.co/products/logstash) on
Linux systems. The role can manage `logstash.yml`, the log4j2 logging, the JVM
heap, TLS, and the Elasticsearch writer role/user. For pipelines it can create
two default pipelines — a Beats input and an Elasticsearch forwarder, both using
Redis — and manage your own pipelines, whose configuration can be checked out
from external git repositories.

It works with the standard Elastic Stack packages and with Elastic's OSS variant.

## Requirements

* The `community.general` collection.
* `passlib` (Python, on the controller) unless you disable password hashing for the Logstash user.
* `curl` on the target host.
* `git` on the target host if you use git-based pipelines.
* Redis if you use the default pipeline or other pipelines that talk to Redis
  (e.g. via the [`geerlingguy.redis`](https://galaxy.ansible.com/geerlingguy/redis) role).

You also need the Elastic repositories configured — use the [`repos`](../repos) role.

## Example

```yaml
- name: Install Logstash
  hosts: logstash
  collections:
    - netways.elasticstack
  roles:
    - repos
    - logstash
```

## Pipelines

For how to configure pipelines (built-in Redis/Beats and external git
repositories), see the [pipelines documentation](docs/pipelines.md).

## Tags

Run only parts of the role with `--tags`:

* `configuration` (alias `logstash_configuration`) — only (re)write the configuration, skip installation.
* `certificates` — only generate and distribute the TLS certificates.
* `renew_logstash_cert` / `renew_ca` — force renewal of the Logstash certificate.
* `mermaid` — only regenerate the pipeline overview (`pipelines.mermaid`).

<!-- ANSIBLE DOCSMITH MAIN START -->
## Role variables<a id="variables"></a>

| Variable | Type | Default | Choices | Description |
|----------|------|---------|---------|-------------|
| `logstash_enable` | `bool` | `true` | — | Start and enable the Logstash service. |
| `logstash_config_backup` | `bool` | `false` | — | Keep backups of every configuration file the role changes. |
| `logstash_manage_yaml` | `bool` | `true` | — | Manage and overwrite logstash.yml. |
| `logstash_manage_logging` | `bool` | `false` | — | Manage the log4j2 logging configuration. |
| `logstash_heap` | `str` | `"1"` | — | JVM heap size in GB. Sets both -Xms and -Xmx via an LS_JAVA_OPTS systemd drop-in.<br><br>Elastic recommends 4-8 GB for typical ingestion and staying below 50-75% of physical memory. Keep it low when Logstash shares a host with Elasticsearch so they do not compete for memory. |
| `logstash_plugins` | `list` of `str` | N/A | — | List of Logstash plugins to install. Unset by default. |
| `logstash_config_autoreload` | `bool` | `true` | — | Enable automatic reload of the Logstash configuration. |
| `logstash_config_autoreload_interval` | `str` | N/A | — | Interval between configuration reload checks (e.g. "3s"). Only used when logstash_config_autoreload is enabled. Unset by default. |
| `logstash_config_path_data` | `str` | `"/var/lib/logstash"` | — | Logstash data directory (path.data). |
| `logstash_config_path_logs` | `str` | `"/var/log/logstash"` | — | Logstash log directory (path.logs). |
| `logstash_http_host` | `str` | N/A | — | Bind address of the Logstash monitoring API (http.host). Unset by default. |
| `logstash_http_port` | `str` | N/A | — | Port (or port range, e.g. "9600-9700") of the monitoring API (http.port). Unset by default. |
| `logstash_global_ecs` | `str` | N/A | `disabled`, `v1` | Set the global ECS compatibility mode (pipeline.ecs_compatibility). Unset by default. |
| `logstash_pipeline_unsafe_shutdown` | `bool` | N/A | — | Force Logstash to exit during shutdown even if there are in-flight events. Unset by default. |
| `logstash_legacy_monitoring` | `bool` | `true` | — | Enable legacy X-Pack monitoring. Ignored unless elasticstack_full_stack is set and only effective on Elastic Stack releases lower than 8. |
| `logstash_manage_pipelines` | `bool` | `true` | — | Manage pipelines.yml. |
| `logstash_no_pipelines` | `bool` | `false` | — | Disable all pipeline management entirely. |
| `logstash_pipelines` | `list` of `dict` | … | — | List of pipelines to configure.<br><br>Each entry needs a name. A pipeline either points to an external git repository (source/version) or defines simple input/output keys that connect to Redis. See the pipelines documentation for details. |
| &nbsp;&nbsp;&nbsp;&nbsp;↳ `name` | `str` | N/A | — | Unique name of the pipeline. Becomes the pipeline directory and pipeline.id. |
| &nbsp;&nbsp;&nbsp;&nbsp;↳ `exclusive` | `bool` | N/A | — | Mark this pipeline as the only one allowed to handle its events. |
| &nbsp;&nbsp;&nbsp;&nbsp;↳ `source` | `str` | N/A | — | URL of a git repository holding the pipeline configuration. |
| &nbsp;&nbsp;&nbsp;&nbsp;↳ `version` | `str` | N/A | — | Git branch/tag/commit to check out from source (default "main"). |
| &nbsp;&nbsp;&nbsp;&nbsp;↳ `queue_type` | `str` | N/A | `memory`, `persisted` | Queue type for this pipeline (default "memory"). Use "persisted" for an on-disk persistent queue. |
| &nbsp;&nbsp;&nbsp;&nbsp;↳ `queue_max_bytes` | `str` | N/A | — | Maximum queue size for this pipeline (default "1gb"). |
| &nbsp;&nbsp;&nbsp;&nbsp;↳ `input` | `list` of `dict` | … | — | Simple Redis inputs for this pipeline. |
| &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;↳ `name` | `str` | N/A | — | Name of the input. |
| &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;↳ `key` | `str` | N/A | — | Redis key to read from. |
| &nbsp;&nbsp;&nbsp;&nbsp;↳ `output` | `list` of `dict` | … | — | Simple Redis outputs for this pipeline. |
| &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;↳ `name` | `str` | N/A | — | Name of the output. |
| &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;↳ `key` | `str` | N/A | — | Redis key to write to. |
| &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;↳ `condition` | `str` | N/A | — | Optional Logstash conditional. The output only receives events matching it. With exclusive set, the conditions are chained with else if. |
| &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;↳ `congestion` | `int` | N/A | — | Optional congestion threshold. The output stops once the target Redis key holds more items than this value. |
| `logstash_elasticsearch_output` | `bool` | `true` | — | Create the default pipeline that forwards events to Elasticsearch. |
| `logstash_beats_input` | `bool` | `true` | — | Create the default pipeline with a Beats input. |
| `logstash_beats_input_congestion` | `int` | N/A | — | Congestion threshold for the default Beats input pipeline: it stops writing to Redis once the buffer key holds more items than this value. Unset by default. |
| `logstash_beats_timeout` | `str` | N/A | — | Timeout for idle client connections on the Beats input (e.g. "60s"). Unset by default. |
| `logstash_beats_tls` | `bool` | N/A | — | Activate TLS on the Beats input pipeline. Unset by default, but enabled automatically in a full stack setup unless overridden. |
| `logstash_input_queue_type` | `str` | `"memory"` | `memory`, `persisted` | Queue type for the default Beats input pipeline. Use "persisted" for an on-disk persistent queue. |
| `logstash_input_queue_max_bytes` | `str` | `"1gb"` | — | Maximum queue size for the default Beats input pipeline. |
| `logstash_forwarder_queue_type` | `str` | `"memory"` | `memory`, `persisted` | Queue type for the default Elasticsearch forwarder pipeline. Use "persisted" for an on-disk persistent queue. |
| `logstash_forwarder_queue_max_bytes` | `str` | `"1gb"` | — | Maximum queue size for the default Elasticsearch forwarder pipeline. |
| `logstash_redis_password` | `str` | N/A | — | Password used when the simple inputs/outputs connect to Redis. Unset by default. |
| `logstash_elasticsearch` | `list` of `str` | N/A | — | Elasticsearch hosts for the default output. Defaults to the nodes from the elasticsearch group, or localhost when used standalone. |
| `logstash_validate_after_inactivity` | `str` | `"300"` | — | Seconds Logstash waits before validating a previously idle connection to Elasticsearch. |
| `logstash_sniffing` | `bool` | `false` | — | Enable sniffing for additional Elasticsearch nodes. |
| `logstash_sniffing_delay` | `str` | N/A | — | Seconds to wait between sniffing attempts. Unset by default. |
| `logstash_sniffing_path` | `str` | N/A | — | HTTP path used for the sniffing requests. Unset by default. |
| `logstash_security` | `bool` | N/A | — | Enable X-Pack security (TLS) for Logstash. No default; enabled automatically in full stack mode with the elastic variant. |
| `logstash_tls_key_passphrase` | `str` | `"LogstashChangeMe"` | — | Passphrase for the generated Logstash certificates. |
| `logstash_certs_dir` | `str` | `"/etc/logstash/certs"` | — | Directory holding the Logstash certificates. Used to build several file paths. |
| `logstash_cert_validity_period` | `int` | `1095` | — | Number of days the generated certificates are valid. |
| `logstash_cert_expiration_buffer` | `int` | `30` | — | Renew the certificate when its remaining validity (in days) drops below this value. |
| `logstash_cert_will_expire_soon` | `bool` | `false` | — | Set to true to force renewal of the Logstash certificate. Alternatively run the playbook with the renew_logstash_cert tag. |
| `logstash_create_role` | `bool` | `true` | — | Create the Logstash writer role in Elasticsearch. |
| `logstash_role_name` | `str` | `"logstash_writer"` | — | Name of the Logstash writer role. |
| `logstash_role_cluster_privileges` | `list` of `str` | `['manage_index_templates', 'monitor', 'manage_ilm']` | — | Cluster privileges granted to the Logstash writer role. |
| `logstash_role_indicies_names` | `list` of `str` | `['ecs-logstash*', 'logstash*', 'logs*']` | — | Index patterns the Logstash writer role may access. |
| `logstash_role_indicies_privileges` | `list` of `str` | `['write', 'create', 'delete', 'create_index', 'manage', 'manage_ilm']` | — | Index privileges the Logstash writer role holds on its index patterns. |
| `logstash_create_user` | `bool` | `true` | — | Create the Logstash writer user in Elasticsearch. |
| `logstash_user_name` | `str` | `"logstash_writer"` | — | Name of the Logstash user connecting to Elasticsearch. |
| `logstash_user_password` | `str` | `"password"` | — | Password of the Logstash user. Must be at least 6 characters long. |
| `logstash_user_email` | `str` | `""` | — | Email address linked to the Logstash user. |
| `logstash_user_fullname` | `str` | `"Internal Logstash User"` | — | Full name linked to the Logstash user. |
| `logstash_logging_console` | `bool` | `true` | — | Log to the console (syslog when run via systemd). Only effective when logstash_manage_logging is enabled. |
| `logstash_logging_file` | `bool` | `true` | — | Log to the log file. Only effective when logstash_manage_logging is enabled. |
| `logstash_logging_slow_console` | `bool` | `true` | — | Log the slowlog to the console (syslog when run via systemd). Only effective when logstash_manage_logging is enabled. |
| `logstash_logging_slow_file` | `bool` | `true` | — | Log the slowlog to the log file. Only effective when logstash_manage_logging is enabled. |
| `logstash_ident` | `bool` | `true` | — | Add a field identifying the node that processed an event. |
| `logstash_ident_field_name` | `str` | `"[netways][instance]"` | — | Name of the field that identifies the instance. |
| `logstash_pipeline_identifier` | `bool` | `true` | — | Add a field identifying which pipeline processed an event. |
| `logstash_pipeline_identifier_field_name` | `str` | `"[netways][pipeline]"` | — | Name of the pipeline identifier field. |
| `logstash_pipeline_identifier_defaults` | `bool` | `false` | — | Also add pipeline identifiers in the default pipelines. This can let the defaults dominate statistics with little value. |
| `logstash_mermaid` | `bool` | `true` | — | Produce an overview of the Logstash pipelines in Mermaid syntax. |
| `logstash_mermaid_logstash` | `bool` | `true` | — | Place the Mermaid syntax into /etc/logstash/pipelines.mermaid on the Logstash hosts. |
| `logstash_mermaid_local` | `bool` | `false` | — | Place the Mermaid syntax into a temporary file on the control node. |
| `logstash_mermaid_extra` | `str` | N/A | — | Extra Mermaid syntax to append to the output (YAML multiline supported). Unset by default. |
| `logstash_freshstart` | `dict` | `{'changed': False}` | — | Internal state used by the role to detect a fresh install. Do not set manually. |

<!-- ANSIBLE DOCSMITH MAIN END -->

## Shared variables

This role also uses the collection-wide `elasticstack_*` variables (e.g.
`elasticstack_full_stack`, `elasticstack_ca_host`, `elasticstack_ca_pass`,
`elasticstack_release`, `elasticstack_variant`). They are documented centrally
with the [elasticstack role](../../docs/role-elasticsearch.md).
