Ansible Role: Kibana
=========

![Test Role Kibana](https://github.com/netways/ansible-collection-elasticstack/actions/workflows/test_role_kibana.yml/badge.svg)

This roles installs and configures Kibana.


Role Variables
--------------

* *kibana_elasticsearch_hosts*: A list of DNS resolvable hostnames of Elasticsearch hosts to connect your Kibana instance to. (default: `- localhost`)
* *kibana_manage_yaml*: Change Kibanas main configuration file (default: `true`)
* *kibana_config_backup*: Keep backups if we change any configuration file (default: `true`)
* *kibana_tls*: Whether to offer `https` for clients or not (default: `false`)
* *kibana_tls_cert*: Path to the certificate Kibana should show to its clients (default: `/etc/kibana/certs/cert.pem`)
* *kibana_tls_key*: Path to the key Kibana should use when communicating with clients (default: `/etc/kibana/certs/key.pem`)

* *kibana_security*: Activate TLS and authentication when connecting to Elasticsearch. **Note**: Only works when `elastic_stack_full_stack` is enabled. (default: `true`)

These variables are identical over all our elastic related roles, hence the different naming scheme.

* *elastic_stack_full_stack*: Use `ansible-role-elasticsearch` as well (default: `false`)
* *elastic_elasticsearch_http_port*: Port of Elasticsearch http (Default: `9200`)
* *kibana_tls_key_passphrase*: Passphrase for kibana certificates (default: `PleaseChangeMe`)
* *kibana_cert_expiration_buffer*: Ansible will renew the kibana certificate if its validity is shorter than this value, which should be number of days. (default: 30)
* *kibana_cert_will_expire_soon*: Set it to true to renew kibana certificate (default: `false`), Or run the playbook with `--tags renew_kibana_cert` to do that.
* *elastic_kibana_host*: Hostname users use to connect to Kibana (default: FQDN of the host the role is executed on)
* *elastic_kibana_port*: Port Kibana webinterface is listening on (default: `5601`)
* *elasticsearch_ca*: Set to the inventory hostname of the host that should house the CA for certificates for inter-node communication. (default: First node in the `elasticsearch` host group)
* *elastic_ca_dir*: Directory where on the Elasticsearch CA host certificates are stored. This is only useful in connection with out other Elastic Stack related roles. (default: `/opt/es-ca`)
* *elastic_ca_pass*: Password for Elasticsearch CA (default: `PleaseChangeMe`)
* *elastic_initial_passwords*: Path to file with initical elasticsearch passwords (default: `/usr/share/elasticsearch/initial_passwords`)
* *elastic_release*: Major release version of Elastic stack to configure. (default: `7`)
* *elastic_variant*: Variant of the stack to install. Valid values: `elastic` or `oss`. (default: `elastic`)

If you use `localhost` in `kibana_elasticsearch_hosts` , certificate verification will skip hostname checks

## Usage

```
- name: Install Kibana
  collections:
    - netways.elasticstack
  hosts: kibana-host
  vars:
    elastic_stack_full_stack: true
    elastic_variant: oss
  roles:
    - repos
    - kibana
```
