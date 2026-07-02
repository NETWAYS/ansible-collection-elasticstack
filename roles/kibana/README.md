# Ansible Role: Kibana

Installs and configures [Kibana](https://www.elastic.co/kibana) on Linux systems.
The role can manage `kibana.yml`, the connection to Elasticsearch, TLS for the
Kibana server, and — in a full stack setup — the X-Pack security certificates.

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
| `kibana_extra_config` | `str` | N/A | — | Extra configuration appended verbatim to kibana.yml (YAML). Unset by default. |
| `kibana_freshstart` | `dict` | `{'changed': False}` | — | Internal state used by the role to detect a fresh install. Do not set manually. |

<!-- ANSIBLE DOCSMITH MAIN END -->

## Shared variables

This role also uses the collection-wide `elasticstack_*` variables (e.g.
`elasticstack_full_stack`, `elasticstack_variant`, `elasticstack_release`,
`elasticstack_ca_host`, `elasticstack_ca_pass`, `elasticstack_kibana_host`,
`elasticstack_kibana_port`, `elasticstack_elasticsearch_http_port`). They are
documented centrally with the [elasticsearch role](../../docs/role-elasticsearch.md).
