# Ansible Role: Elasticsearch

Installs and configures [Elasticsearch](https://www.elastic.co/elasticsearch) on
Linux systems. The role manages `elasticsearch.yml` and the JVM configuration
(heap and options). With security enabled (the default) it creates a self-signed
CA and a certificate for each node, enables transport and HTTP TLS, manages the
keystore, and generates the initial passwords; the same CA is reused by the
Logstash, Kibana and Beats roles for their own certificates. It configures
cluster discovery for single- or multi-node setups and upgrades the nodes one at
a time when you raise `elasticstack_version`.

The OSS variant is only available up to Elastic Stack 7; from release 8 on only
the default `elastic` variant exists, and security is required.

## Requirements

* The Elastic repositories configured — use the [`repos`](../repos) role.
* For the default security setup the role generates certificates with the
  bundled `elasticsearch-certutil` and `openssl`. The required Python libraries
  (`cryptography`, `elasticsearch`) are installed for you by the shared
  `elasticstack` role.

## Example

```yaml
- name: Install Elasticsearch
  hosts: elasticsearch
  collections:
    - netways.elasticstack
  roles:
    - repos
    - elasticsearch
```

## Tags

Run only parts of the role with `--tags`:

* `certificates` — only generate and distribute the TLS certificates.
* `renew_es_cert` — force renewal of the Elasticsearch node certificate.
* `renew_ca` — force renewal of the stack CA and all component certificates.

<!-- ANSIBLE DOCSMITH MAIN START -->
## Role variables<a id="variables"></a>

| Variable | Type | Default | Choices | Description |
|----------|------|---------|---------|-------------|
| `elasticsearch_enable` | `bool` | `true` | — | Start and enable the Elasticsearch service. |
| `elasticsearch_manage_yaml` | `bool` | `true` | — | Manage and overwrite elasticsearch.yml. |
| `elasticsearch_config_backup` | `bool` | `false` | — | Keep a backup of elasticsearch.yml whenever the role changes it. |
| `elasticsearch_clustername` | `str` | `"elasticsearch"` | — | Name of the Elasticsearch cluster (cluster.name). |
| `elasticsearch_nodename` | `str` | N/A | — | Name of this Elasticsearch node (node.name). Defaults to the host's ansible_hostname. |
| `elasticsearch_node_types` | `list` of `str` | N/A | — | Node roles for this node (node.roles), e.g. master, data, ingest. When unset, Elasticsearch uses its own defaults. See the Elasticsearch node-roles documentation for valid values. |
| `elasticsearch_datapath` | `str` | `"/var/lib/elasticsearch"` | — | Directory where Elasticsearch stores its data (path.data). |
| `elasticsearch_create_datapath` | `bool` | `false` | — | Create the data directory if it does not exist. Useful when you change elasticsearch_datapath. |
| `elasticsearch_logpath` | `str` | `"/var/log/elasticsearch"` | — | Directory where Elasticsearch stores its logs (path.logs). |
| `elasticsearch_create_logpath` | `bool` | `false` | — | Create the log directory if it does not exist. Useful when you change elasticsearch_logpath. |
| `elasticsearch_conf_dir` | `str` | `"/etc/elasticsearch/"` | — | Elasticsearch configuration directory. Used to place the jvm.options.d drop-ins. |
| `elasticsearch_group` | `str` | `"elasticsearch"` | — | OS group that owns the jvm.options.d drop-ins. The service reads them through this group, so it must match the group the package runs the service as (elasticsearch). Changing it is not recommended. |
| `elasticsearch_fs_repo` | `list` of `str` | N/A | — | Filesystem paths registered as snapshot repositories (path.repo). Every node must reach the same share under the same path. Unset by default. |
| `elasticsearch_heap` | `str` | `"{{ [[(ansible_memtotal_mb // 1024) // 2, 30] \| min, 1] \| max }}"` | — | JVM heap size in GB. Sets both -Xms and -Xmx via a jvm.options.d drop-in. The default is half of the host memory, capped between 1 and 30 GB. Set to false to leave heap sizing to Elasticsearch/the JVM. |
| `elasticsearch_heap_dump_path` | `str` | `"/var/lib/elasticsearch"` | — | Directory for JVM heap dumps (-XX:HeapDumpPath). |
| `elasticsearch_jvm_custom_parameters` | `raw` | `""` | — | Extra JVM options written to a jvm.options.d drop-in, provided as a list of option lines (e.g. ["-XX:+UseG1GC"]). Empty by default. |
| `elasticsearch_api_host` | `str` | `"localhost"` | — | Host or IP the role uses for its own Elasticsearch API connection checks. |
| `elasticsearch_network_host` | `str` | N/A | — | Network addresses Elasticsearch binds to (network.host). Accepts IPs, interface names, or Elasticsearch special values, e.g. "_ens190_,_local_". Defaults to "_local_", "_site_" when unset. |
| `elasticsearch_http_publish_host` | `str` | N/A | — | Address HTTP clients use to reach this node when sniffing (http.publish_host). Unset by default. |
| `elasticsearch_http_publish_port` | `int` | N/A | — | HTTP publish port, only needed when it must differ from http.port (http.publish_port). Unset by default. |
| `elasticsearch_transport_port` | `int` | N/A | — | Port for inter-node transport communication (transport.port). Unset by default. |
| `elasticsearch_seed_hosts` | `list` of `str` | N/A | — | Seed hosts for cluster discovery (discovery.seed_hosts). Overrides the list the role builds from the elasticsearch group. Unset by default. |
| `elasticsearch_check_calculation` | `bool` | `false` | — | When true, Elasticsearch is not installed, configured, or started: the role runs only the node-role validation and then stops each host (meta: end_host). The validation derives each node's role (master/data/other) from elasticsearch_node_types, groups the nodes, and asserts an odd number of master-eligible nodes (required for a valid quorum). Requires elasticsearch_node_types. Useful as a pre-flight inventory/topology check (before scaling or in CI) without a full deployment. |
| `elasticsearch_disable_systemcallfilterchecks` | `bool` | `false` | — | Disable the system call filter check (bootstrap.system_call_filter). Has a security impact and is only applied on Elastic Stack release 7. |
| `elasticsearch_jna_workaround` | `bool` | `false` | — | Work around systems where JNA cannot load its native library. WARNING this rewrites the sysconfig/default file and overwrites ES_JAVA_OPTS. |
| `elasticsearch_unsafe_upgrade_restart` | `bool` | `false` | — | During upgrades, update the package first and then restart the service, instead of stopping it, upgrading and starting again. Only for non-production clusters, use at your own risk. |
| `elasticsearch_security` | `bool` | `true` | — | Enable X-Pack security (transport TLS, keystore, CA and certificates). Required on Elastic Stack release 8 and later with the elastic variant. |
| `elasticsearch_http_security` | `bool` | `true` | — | Enable TLS on the HTTP layer (xpack.security.http.ssl). Only effective when elasticsearch_security is enabled. |
| `elasticsearch_security_enrollment` | `bool` | N/A | — | Control node/Kibana enrollment on a node autoconfigured for security (xpack.security.enrollment.enabled). Unset by default. |
| `elasticsearch_ml_enabled` | `bool` | `true` | — | Enable Machine Learning (xpack.ml.enabled). Only applied with the elastic variant. |
| `elasticsearch_monitoring_enabled` | `bool` | `true` | — | Enable X-Pack monitoring collection (xpack.monitoring.collection.enabled). Only applied on Elastic Stack release 7. |
| `elasticsearch_bootstrap_pw` | `str` | `"PleaseChangeMe"` | — | Bootstrap password stored in the keystore. Only takes effect when Elasticsearch is initialised for the first time; later changes do not update it. |
| `elasticsearch_http_protocol` | `str` | `"http"` | `http`, `https` | Protocol the role uses to talk to the Elasticsearch API. Set automatically to https once HTTP security is active. |
| `elasticsearch_ssl_verification_mode` | `str` | `"full"` | `full`, `certificate`, `none` | How certificates presented by the other party are verified (xpack.security.transport.ssl.verification_mode). |
| `elasticsearch_tls_key_passphrase` | `str` | `"PleaseChangeMeIndividually"` | — | Passphrase for the generated Elasticsearch certificates. Overridden by elasticstack_cert_pass when that is set. |
| `elasticsearch_cert_validity_period` | `int` | `1095` | — | Number of days the generated certificates are valid. |
| `elasticsearch_cert_expiration_buffer` | `int` | `30` | — | Renew the certificate when its remaining validity (in days) drops below this value. |
| `elasticsearch_cert_will_expire_soon` | `bool` | `false` | — | Set to true to force renewal of the Elasticsearch certificate. Alternatively run the playbook with the renew_es_cert tag. |
| `elasticsearch_extra_config` | `dict` | N/A | — | Additional elasticsearch.yml settings, given as a mapping and rendered as YAML into the configuration (via to_nice_yaml). Unset by default. |
| `elasticsearch_initialized_file` | `str` | `"{{ elasticstack_initial_passwords \| default('') \| dirname }}/cluster_initialized"` | — | Marker file the role writes once the cluster is initialised, used to detect an existing setup. Advanced; usually left at its default. |
| `elasticsearch_freshstart` | `dict` | `{'changed': False}` | — | Internal state used by the role to detect a fresh install. Do not set manually. |
| `elasticsearch_freshstart_security` | `dict` | `{'changed': False}` | — | Internal state used by the role to detect a fresh security setup. Do not set manually. |

<!-- ANSIBLE DOCSMITH MAIN END -->

## Shared variables

This role also uses the collection-wide `elasticstack_*` variables (e.g.
`elasticstack_full_stack`, `elasticstack_variant`, `elasticstack_release`,
`elasticstack_ca_host`, `elasticstack_ca_pass`, `elasticstack_ca_dir`,
`elasticstack_elasticsearch_http_port`, `elasticstack_initial_passwords`). They
are documented centrally with the
[elasticstack role](../elasticstack/README.md).
