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

| Variable | Description |
|----------|-------------|
| `logstash_enable`<br>**Type**: `bool`<br>**Default**: `true` | Start and enable the Logstash service. |
| `logstash_config_backup`<br>**Type**: `bool`<br>**Default**: `false` | Keep backups of every configuration file the role changes. |
| `logstash_manage_yaml`<br>**Type**: `bool`<br>**Default**: `true` | Manage and overwrite logstash.yml. |
| `logstash_manage_logging`<br>**Type**: `bool`<br>**Default**: `false` | Manage the log4j2 logging configuration. |
| `logstash_heap`<br>**Type**: `str`<br>**Default**: `"1"` | JVM heap size in GB. Sets both -Xms and -Xmx via an LS_JAVA_OPTS systemd drop-in.<br><br>Elastic recommends 4-8 GB for typical ingestion and staying below 50-75% of physical memory. Keep it low when Logstash shares a host with Elasticsearch so they do not compete for memory. |
| `logstash_plugins`<br>**Type**: `list` of `str` | List of Logstash plugins to install. Unset by default. |
| `logstash_config_autoreload`<br>**Type**: `bool`<br>**Default**: `true` | Enable automatic reload of the Logstash configuration. |
| `logstash_config_autoreload_interval`<br>**Type**: `str` | Interval between configuration reload checks (e.g. "3s"). Only used when logstash_config_autoreload is enabled. Unset by default. |
| `logstash_config_path_data`<br>**Type**: `str`<br>**Default**: `"/var/lib/logstash"` | Logstash data directory (path.data). |
| `logstash_config_path_logs`<br>**Type**: `str`<br>**Default**: `"/var/log/logstash"` | Logstash log directory (path.logs). |
| `logstash_http_host`<br>**Type**: `str` | Bind address of the Logstash monitoring API (http.host). Unset by default. |
| `logstash_http_port`<br>**Type**: `str` | Port (or port range, e.g. "9600-9700") of the monitoring API (http.port). Unset by default. |
| `logstash_global_ecs`<br>**Type**: `str`<br>**Choices**: `disabled`, `v1` | Set the global ECS compatibility mode (pipeline.ecs_compatibility). Unset by default. |
| `logstash_pipeline_unsafe_shutdown`<br>**Type**: `bool` | Force Logstash to exit during shutdown even if there are in-flight events. Unset by default. |
| `logstash_legacy_monitoring`<br>**Type**: `bool`<br>**Default**: `true` | Enable legacy X-Pack monitoring. Ignored unless elasticstack_full_stack is set and only effective on Elastic Stack releases lower than 8. |
| `logstash_manage_pipelines`<br>**Type**: `bool`<br>**Default**: `true` | Manage pipelines.yml. |
| `logstash_no_pipelines`<br>**Type**: `bool`<br>**Default**: `false` | Disable all pipeline management entirely. |
| `logstash_pipelines`<br>**Type**: `list` of `dict` | List of pipelines to configure.<br><br>Each entry needs a name. A pipeline either points to an external git repository (source/version) or defines simple input/output keys that connect to Redis. See the pipelines documentation for details. |
| &nbsp;&nbsp;&nbsp;&nbsp;↳ `name`<br>**Type**: `str`<br>**Required**: Yes | Unique name of the pipeline. Becomes the pipeline directory and pipeline.id. |
| &nbsp;&nbsp;&nbsp;&nbsp;↳ `exclusive`<br>**Type**: `bool` | Mark this pipeline as the only one allowed to handle its events. |
| &nbsp;&nbsp;&nbsp;&nbsp;↳ `source`<br>**Type**: `str` | URL of a git repository holding the pipeline configuration. |
| &nbsp;&nbsp;&nbsp;&nbsp;↳ `version`<br>**Type**: `str` | Git branch/tag/commit to check out from source (default "main"). |
| &nbsp;&nbsp;&nbsp;&nbsp;↳ `queue_type`<br>**Type**: `str`<br>**Choices**: `memory`, `persisted` | Queue type for this pipeline (default "memory"). Use "persisted" for an on-disk persistent queue. |
| &nbsp;&nbsp;&nbsp;&nbsp;↳ `queue_max_bytes`<br>**Type**: `str` | Maximum queue size for this pipeline (default "1gb"). |
| &nbsp;&nbsp;&nbsp;&nbsp;↳ `input`<br>**Type**: `list` of `dict` | Simple Redis inputs for this pipeline. |
| &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;↳ `name`<br>**Type**: `str` | Name of the input. |
| &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;↳ `key`<br>**Type**: `str` | Redis key to read from. |
| &nbsp;&nbsp;&nbsp;&nbsp;↳ `output`<br>**Type**: `list` of `dict` | Simple Redis outputs for this pipeline. |
| &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;↳ `name`<br>**Type**: `str` | Name of the output. |
| &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;↳ `key`<br>**Type**: `str` | Redis key to write to. |
| &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;↳ `condition`<br>**Type**: `str` | Optional Logstash conditional. The output only receives events matching it. With exclusive set, the conditions are chained with else if. |
| &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;↳ `congestion`<br>**Type**: `int` | Optional congestion threshold. The output stops once the target Redis key holds more items than this value. |
| `logstash_elasticsearch_output`<br>**Type**: `bool`<br>**Default**: `true` | Create the default pipeline that forwards events to Elasticsearch. |
| `logstash_beats_input`<br>**Type**: `bool`<br>**Default**: `true` | Create the default pipeline with a Beats input. |
| `logstash_beats_input_congestion`<br>**Type**: `int` | Congestion threshold for the default Beats input pipeline: it stops writing to Redis once the buffer key holds more items than this value. Unset by default. |
| `logstash_beats_timeout`<br>**Type**: `str` | Timeout for idle client connections on the Beats input (e.g. "60s"). Unset by default. |
| `logstash_beats_tls`<br>**Type**: `bool` | Activate TLS on the Beats input pipeline. Unset by default, but enabled automatically in a full stack setup unless overridden. |
| `logstash_input_queue_type`<br>**Type**: `str`<br>**Default**: `"memory"`<br>**Choices**: `memory`, `persisted` | Queue type for the default Beats input pipeline. Use "persisted" for an on-disk persistent queue. |
| `logstash_input_queue_max_bytes`<br>**Type**: `str`<br>**Default**: `"1gb"` | Maximum queue size for the default Beats input pipeline. |
| `logstash_forwarder_queue_type`<br>**Type**: `str`<br>**Default**: `"memory"`<br>**Choices**: `memory`, `persisted` | Queue type for the default Elasticsearch forwarder pipeline. Use "persisted" for an on-disk persistent queue. |
| `logstash_forwarder_queue_max_bytes`<br>**Type**: `str`<br>**Default**: `"1gb"` | Maximum queue size for the default Elasticsearch forwarder pipeline. |
| `logstash_redis_password`<br>**Type**: `str` | Password used when the simple inputs/outputs connect to Redis. Unset by default. |
| `logstash_redis_input_host`<br>**Type**: `str`<br>**Default**: `"localhost"` | Redis host that simple pipeline inputs (and the default forwarder input) read from. |
| `logstash_redis_output_host`<br>**Type**: `str`<br>**Default**: `"localhost"` | Redis host that simple pipeline outputs (and the default input pipeline) write to. |
| `logstash_redis_tls`<br>**Type**: `bool`<br>**Default**: `false` | Enable TLS on the simple Redis inputs/outputs (`ssl`/`ssl_enabled`). |
| `logstash_redis_ssl_certificate`<br>**Type**: `str` | Path to the SSL certificate for the Redis outputs (the redis output plugin only; the input plugin has no such option). Rendered only when logstash_redis_tls is true. |
| `logstash_redis_ssl_key`<br>**Type**: `str` | Path to the SSL key for the Redis outputs. Rendered only when logstash_redis_tls is true. |
| `logstash_redis_ssl_key_passphrase`<br>**Type**: `str` | Passphrase for logstash_redis_ssl_key. Rendered only when logstash_redis_tls is true. |
| `logstash_redis_ssl_certificate_authorities`<br>**Type**: `list` of `str` | List of CA certificate paths used to verify the Redis server on the Redis outputs. Rendered only when logstash_redis_tls is true. |
| `logstash_redis_ssl_supported_protocols`<br>**Type**: `str` | TLS protocol version accepted on the Redis outputs (for example "TLSv1.3"). Rendered only when logstash_redis_tls is true. |
| `logstash_redis_ssl_verification_mode`<br>**Type**: `str` | Certificate verification mode for the Redis outputs ("full" or "none"). Rendered only when logstash_redis_tls is true. |
| `logstash_elasticsearch`<br>**Type**: `list` of `str` | Elasticsearch hosts for the default output. Defaults to the nodes from the elasticsearch group, or localhost when used standalone. |
| `logstash_validate_after_inactivity`<br>**Type**: `str`<br>**Default**: `"300"` | Seconds Logstash waits before validating a previously idle connection to Elasticsearch. |
| `logstash_sniffing`<br>**Type**: `bool`<br>**Default**: `false` | Enable sniffing for additional Elasticsearch nodes. |
| `logstash_sniffing_delay`<br>**Type**: `str` | Seconds to wait between sniffing attempts. Unset by default. |
| `logstash_sniffing_path`<br>**Type**: `str` | HTTP path used for the sniffing requests. Unset by default. |
| `logstash_security`<br>**Type**: `bool` | Enable X-Pack security (TLS) for Logstash. No default; enabled automatically in full stack mode with the elastic variant. |
| `logstash_tls_key_passphrase`<br>**Type**: `str`<br>**Default**: `"LogstashChangeMe"` | Passphrase for the generated Logstash certificates. |
| `logstash_certs_dir`<br>**Type**: `str`<br>**Default**: `"/etc/logstash/certs"` | Directory holding the Logstash certificates. Used to build several file paths. |
| `logstash_cert_validity_period`<br>**Type**: `int`<br>**Default**: `1095` | Number of days the generated certificates are valid. |
| `logstash_cert_expiration_buffer`<br>**Type**: `int`<br>**Default**: `30` | Renew the certificate when its remaining validity (in days) drops below this value. |
| `logstash_cert_will_expire_soon`<br>**Type**: `bool`<br>**Default**: `false` | Set to true to force renewal of the Logstash certificate. Alternatively run the playbook with the renew_logstash_cert tag. |
| `logstash_create_role`<br>**Type**: `bool`<br>**Default**: `true` | Create the Logstash writer role in Elasticsearch. |
| `logstash_role_name`<br>**Type**: `str`<br>**Default**: `"logstash_writer"` | Name of the Logstash writer role. |
| `logstash_role_cluster_privileges`<br>**Type**: `list` of `str`<br>**Default**: `['manage_index_templates', 'monitor', 'manage_ilm']` | Cluster privileges granted to the Logstash writer role. |
| `logstash_role_indicies_names`<br>**Type**: `list` of `str`<br>**Default**: `['ecs-logstash*', 'logstash*', 'logs*']` | Index patterns the Logstash writer role may access. |
| `logstash_role_indicies_privileges`<br>**Type**: `list` of `str`<br>**Default**: `['write', 'create', 'delete', 'create_index', 'manage', 'manage_ilm']` | Index privileges the Logstash writer role holds on its index patterns. |
| `logstash_create_user`<br>**Type**: `bool`<br>**Default**: `true` | Create the Logstash writer user in Elasticsearch. |
| `logstash_user_name`<br>**Type**: `str`<br>**Default**: `"logstash_writer"` | Name of the Logstash user connecting to Elasticsearch. |
| `logstash_user_password`<br>**Type**: `str`<br>**Default**: `"password"` | Password of the Logstash user. Must be at least 6 characters long. |
| `logstash_user_email`<br>**Type**: `str`<br>**Default**: `""` | Email address linked to the Logstash user. |
| `logstash_user_fullname`<br>**Type**: `str`<br>**Default**: `"Internal Logstash User"` | Full name linked to the Logstash user. |
| `logstash_logging_console`<br>**Type**: `bool`<br>**Default**: `true` | Log to the console (syslog when run via systemd). Only effective when logstash_manage_logging is enabled. |
| `logstash_logging_file`<br>**Type**: `bool`<br>**Default**: `true` | Log to the log file. Only effective when logstash_manage_logging is enabled. |
| `logstash_logging_slow_console`<br>**Type**: `bool`<br>**Default**: `true` | Log the slowlog to the console (syslog when run via systemd). Only effective when logstash_manage_logging is enabled. |
| `logstash_logging_slow_file`<br>**Type**: `bool`<br>**Default**: `true` | Log the slowlog to the log file. Only effective when logstash_manage_logging is enabled. |
| `logstash_logging_retention`<br>**Type**: `str`<br>**Default**: `"7D"` | Age at which rotated log files (plain, json, slowlog, deprecation and per-pipeline routing logs) are deleted by log4j2 at rollover time. Uses log4j2 IfLastModified duration syntax such as "7D", "24H" or "P30D". Only effective when logstash_manage_logging is enabled. |
| `logstash_ident`<br>**Type**: `bool`<br>**Default**: `true` | Add a field identifying the node that processed an event. |
| `logstash_ident_field_name`<br>**Type**: `str`<br>**Default**: `"[netways][instance]"` | Name of the field that identifies the instance. |
| `logstash_pipeline_identifier`<br>**Type**: `bool`<br>**Default**: `true` | Add a field identifying which pipeline processed an event. |
| `logstash_pipeline_identifier_field_name`<br>**Type**: `str`<br>**Default**: `"[netways][pipeline]"` | Name of the pipeline identifier field. |
| `logstash_pipeline_identifier_defaults`<br>**Type**: `bool`<br>**Default**: `false` | Also add pipeline identifiers in the default pipelines. This can let the defaults dominate statistics with little value. |
| `logstash_mermaid`<br>**Type**: `bool`<br>**Default**: `true` | Produce an overview of the Logstash pipelines in Mermaid syntax. |
| `logstash_mermaid_logstash`<br>**Type**: `bool`<br>**Default**: `true` | Place the Mermaid syntax into /etc/logstash/pipelines.mermaid on the Logstash hosts. |
| `logstash_mermaid_local`<br>**Type**: `bool`<br>**Default**: `false` | Place the Mermaid syntax into a temporary file on the control node. |
| `logstash_mermaid_extra`<br>**Type**: `str` | Extra Mermaid syntax to append to the output (YAML multiline supported). Unset by default. |
| `logstash_freshstart`<br>**Type**: `dict`<br>**Default**: `{'changed': False}` | Internal state used by the role to detect a fresh install. Do not set manually. |

<!-- ANSIBLE DOCSMITH MAIN END -->

## Shared variables

This role also uses the collection-wide `elasticstack_*` variables (e.g.
`elasticstack_full_stack`, `elasticstack_ca_host`, `elasticstack_ca_pass`,
`elasticstack_release`, `elasticstack_variant`). They are documented centrally
with the [elasticstack role](../elasticstack/README.md).
