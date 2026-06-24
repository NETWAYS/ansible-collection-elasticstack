Ansible Role: Kibana
=========

![Test Role Kibana](https://github.com/netways/ansible-collection-elasticstack/actions/workflows/test_role_kibana.yml/badge.svg)

This roles installs and configures Kibana.

Role Variables
--------------

* *kibana_manage_yaml*: Change Kibanas main configuration file (default: `true`)
* *kibana_config_backup*: Keep backups if we change any configuration file (default: `true`)
* *kibana_tls*: Whether to offer `https` for clients or not (default: `false`)
* *kibana_tls_cert*: Path to the certificate Kibana should show to its clients (default: `/etc/kibana/certs/cert.pem`)
* *kibana_tls_key*: Path to the key Kibana should use when communicating with clients (default: `/etc/kibana/certs/key.pem`)
* *kibana_extra_config*: You can add arbitraty configuration options with this option. Just start it with `|-` and indent the following lines. So you can add as many lines and options to `kibana.yml` as you like. (default: none)

* *kibana_security*: Activate TLS and authentication when connecting to Elasticsearch. **Note**: Only works when `elasticstack_full_stack` is enabled. (default: `true`)

These variables are identical over all our elastic related roles, hence the different naming scheme.

* *elasticstack_full_stack*: Use `ansible-role-elasticsearch` as well (default: `false`). If you set to `true`, you will be able to use the following variables:
    * *kibana_elasticsearch_hosts*: A list of DNS resolvable hostnames of Elasticsearch hosts to connect your Kibana instance to. (default: `- localhost`)
    * *elasticstack_elasticsearch_http_port*: Port of Elasticsearch http (Default: `9200`)
    * *kibana_sniff_on_start*: Attempt to find other Elasticsearch nodes on startup (default: `false`)
    * *kibana_sniff_on_connection_fault* Update the list of Elasticsearch nodes immediately following a connection fault (default: `false`)
    * *kibana_sniff_interval*: Time in milliseconds between requests to check Elasticsearch for an updated list of nodes (default: `not set`)

* *kibana_tls_key_passphrase*: Passphrase for kibana certificates (default: `PleaseChangeMe`)
* *kibana_cert_validity_period*: number of days that the generated certificates are valid (default: 1095).
* *kibana_cert_expiration_buffer*: Ansible will renew the kibana certificate if its validity is shorter than this value, which should be number of days. (default: 30)
* *kibana_cert_will_expire_soon*: Set it to true to renew kibana certificate (default: `false`), Or run the playbook with `--tags renew_kibana_cert` to do that.
* *elasticstack_kibana_host*: Hostname users use to connect to Kibana (default: FQDN of the host the role is executed on)
* *elasticstack_kibana_port*: Port Kibana webinterface is listening on (default: `5601`)
* *elasticstack_ca_host*: Set to the inventory hostname of the host that should house the CA for certificates for inter-node communication. (default: First node in the `elasticsearch` host group)
* *elasticstack_ca_dir*: Directory where on the Elasticsearch CA host certificates are stored. This is only useful in connection with out other Elastic Stack related roles. (default: `/opt/es-ca`)
* *elasticstack_ca_pass*: Password for Elasticsearch CA (default: `PleaseChangeMe`)
* *elasticstack_initial_passwords*: Path to file with initical elasticsearch passwords (default: `/usr/share/elasticsearch/initial_passwords`)
* *elasticstack_release*: Major release version of Elastic stack to configure. (default: `7`)
* *elasticstack_variant*: Variant of the stack to install. Valid values: `elastic` or `oss` (default: `elastic`)


If you use `localhost` in `kibana_elasticsearch_hosts` , certificate verification will skip hostname checks

## Usage

```
- name: Install Kibana
  collections:
    - netways.elasticstack
  hosts: kibana-host
  vars:
    elasticstack_full_stack: true
    elasticstack_variant: oss
  roles:
    - repos
    - kibana
```
