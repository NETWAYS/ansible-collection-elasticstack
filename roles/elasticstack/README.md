# Ansible Role: elasticstack

The shared base role of the collection. Every component role (elasticsearch,logstash, kibana, beats, repos) imports it automatically on first use, so you normally do not call it directly. It installs the common dependencies and, above all, defines the collection-wide `elasticstack_*` variables — the settings shared across all roles: release and variant, the inventory host groups, ports, the package repositories, and the stack CA.

Set these variables once (in `group_vars`, the play, or via `-e`) and every role picks them up. This page is the central reference for them.

## Requirements

You do not run this role directly — the component roles import it automatically. It installs the shared Python libraries (`cryptography` and the `elasticsearch` client) and packages (`openssl`, `unzip`) that the collection needs.

## Example

You normally set the shared variables rather than invoking the role directly:

```yaml
# group_vars/all.yml
elasticstack_release: 8
elasticstack_variant: elastic
elasticstack_ca_pass: "a strong secret"
```

The role runs automatically the first time any component role is applied to a host.

<!-- ANSIBLE DOCSMITH MAIN START -->
## Role variables<a id="variables"></a>

| Variable | Description |
|----------|-------------|
| `elasticstack_release`<br>**Type**: `int`<br>**Default**: `8` | Major Elastic Stack release to install and configure (e.g. 7 or 8). Drives the package repository and release-dependent behaviour. |
| `elasticstack_variant`<br>**Type**: `str`<br>**Default**: `"elastic"`<br>**Choices**: `elastic`, `oss` | Distribution to install. "elastic" (the default) includes X-Pack; "oss" is the Apache-licensed build without X-Pack. OSS Elasticsearch and Kibana exist only up to release 7, while OSS Logstash and Beats are available on later releases too. |
| `elasticstack_version`<br>**Type**: `str` | Exact package version to install (e.g. "8.8.1"). Unset by default: the collection then installs the latest, or reuses the version already present on the CA host. |
| `elasticstack_full_stack`<br>**Type**: `bool`<br>**Default**: `true` | Treat the hosts as one coordinated stack (roles read each other's hosts, share the CA and wire the connections). Set to false to run a role standalone. |
| `elasticstack_security`<br>**Type**: `bool`<br>**Default**: `true` | Enable X-Pack security across the stack. Only effective with the elastic variant. |
| `elasticstack_override_beats_tls`<br>**Type**: `bool`<br>**Default**: `false` | When true, do not auto-enable TLS between Beats and Logstash in a full stack (also skips Beats certificate generation). |
| `elasticstack_elasticsearch_group_name`<br>**Type**: `str`<br>**Default**: `"elasticsearch"` | Inventory group that holds the Elasticsearch hosts. |
| `elasticstack_logstash_group_name`<br>**Type**: `str`<br>**Default**: `"logstash"` | Inventory group that holds the Logstash hosts. |
| `elasticstack_kibana_group_name`<br>**Type**: `str`<br>**Default**: `"kibana"` | Inventory group that holds the Kibana hosts. |
| `elasticstack_elasticsearch_http_port`<br>**Type**: `int`<br>**Default**: `9200` | Elasticsearch HTTP API port. |
| `elasticstack_kibana_host`<br>**Type**: `str`<br>**Default**: `"{{ ansible_fqdn }}"` | Host name Kibana publishes itself under (server.publicBaseUrl). Defaults to the fully qualified domain name of the Kibana host. Set it when users reach Kibana under a different name, for example behind a reverse proxy or a load balancer. |
| `elasticstack_kibana_port`<br>**Type**: `int`<br>**Default**: `5601` | Kibana HTTP port (also used to build the public base URL). |
| `elasticstack_beats_port`<br>**Type**: `int`<br>**Default**: `5044` | Port of the Logstash Beats input that the Beats ship to. |
| `elasticstack_enable_repos`<br>**Type**: `bool`<br>**Default**: `true` | Configure the Elastic package repositories (see the repos role). |
| `elasticstack_repo_url`<br>**Type**: `str`<br>**Default**: `"https://artifacts.elastic.co/packages"` | Base URL of the Elastic package repositories. |
| `elasticstack_repo_key`<br>**Type**: `str`<br>**Default**: `"https://artifacts.elastic.co/GPG-KEY-elasticsearch"` | URL of the Elastic repository signing (GPG) key. |
| `elasticstack_rpm_workaround`<br>**Type**: `bool`<br>**Default**: `false` | Enable a workaround for importing the repository GPG key on RPM-based systems. |
| `elasticstack_ca_host`<br>**Type**: `str`<br>**Default**: `"{{ groups[elasticstack_elasticsearch_group_name][0] \| default('') }}"` | Inventory host that holds the stack CA and signs all component certificates. Must be an Elasticsearch host: signing uses elasticsearch-certutil, which ships with the elasticsearch package. Defaults to the first host in the elasticsearch group; override it only to pin the CA and the initial_passwords file to a specific Elasticsearch node. Only used when elasticstack_full_stack is true. |
| `elasticstack_ca_dir`<br>**Type**: `str`<br>**Default**: `"/opt/es-ca"` | Directory on the CA host where the CA and generated certificates are stored. |
| `elasticstack_ca_name`<br>**Type**: `str`<br>**Default**: `"CN=Elastic Certificate Tool Autogenerated CA"` | Distinguished name (DN) of the generated CA. |
| `elasticstack_ca_pass`<br>**Type**: `str`<br>**Default**: `"PleaseChangeMe"` | Password protecting the CA private key. |
| `elasticstack_ca_validity_period`<br>**Type**: `int`<br>**Default**: `1095` | Number of days the generated CA is valid. |
| `elasticstack_ca_expiration_buffer`<br>**Type**: `int`<br>**Default**: `30` | Renew the CA when its remaining validity (in days) drops below this value. |
| `elasticstack_ca_will_expire_soon`<br>**Type**: `bool`<br>**Default**: `false` | Set to true to force renewal of the CA and all component certificates. Alternatively run the playbook with the renew_ca tag. |
| `elasticstack_cert_pass`<br>**Type**: `str` | Common passphrase for all component certificates. Unset by default; when set, it overrides each role's individual certificate passphrase. |
| `elasticstack_initial_passwords`<br>**Type**: `str`<br>**Default**: `"/usr/share/elasticsearch/initial_passwords"` | Path on the CA host where the generated initial passwords are stored. |
| `elasticstack_no_log`<br>**Type**: `bool`<br>**Default**: `true` | Hide the output of tasks that could reveal passwords. Set to false for debugging. |
| `elasticstack_manage_pip`<br>**Type**: `bool`<br>**Default**: `false` | Install pip on the target host. |
| `elasticstack_force_pip`<br>**Type**: `bool`<br>**Default**: `false` | Force installation of the required Python modules via pip (useful when the distribution packages are too old). See PEP 668. |
| `elasticstack_ci`<br>**Type**: `bool`<br>**Default**: `false` | Internal test flag. Set to true only by the collection's molecule scenarios to enable resource workarounds needed on constrained test runners (cache cleanup, relaxed Elasticsearch disk watermarks). Never set this on a real installation. |

<!-- ANSIBLE DOCSMITH MAIN END -->
