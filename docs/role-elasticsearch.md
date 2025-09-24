ELASTICSEARCH
=========

![Test Role Elasticsearch](https://github.com/netways/ansible-collection-elasticstack/actions/workflows/test_role_elasticsearch.yml/badge.svg)

This role installs manages Elasticsearch on your hosts. Optionally it can configure Elastics Security components, too.

If you use the role to set up security you, can use its CA to create certificates for Logstash and Kibana, too. When you enable security, the role will check the expiration date of the CA and all certificates every Ansible run and renew the one, which will expire soon default before 30 days.

Please note that setting `elasticsearch_bootstrap_pw` as variable will only take effect when initialising Elasticsearch. Changes after starting elasticsearch for the first time will not change the bootstrap password for the instance and will lead to breaking tests.

Role Variables
--------------

* *elasticsearch_node_types*: List of types of this very node. Please refer to [official docs](https://www.elastic.co/guide/en/elasticsearch/reference/current/modules-node.html) for details. (default: not set. allowed value: array of types)
+ *elasticsearch_nodename*': Node name of the Elasticsearch node. (default: value of `ansible_hostname`)
* *elasticsearch_clustername*: Name the Elasticsearch Cluster (default: `elasticsearch`)
* *elasticsearch_heap*: Heapsize for Elasticsearch. Set to `false` to follow Elastic recommendations for elasticsearch 8.x (default: Half of hosts memory. Min 1GB, Max 30GB)
* *elasticsearch_tls_key_passphrase*: Passphrase for elasticsearch certificates (default: `PleaseChangeMeIndividually`)
* *elasticsearch_cert_validity_period*: number of days that the generated certificates are valid (default: 1095).
* *elasticsearch_cert_expiration_buffer*: Ansible will renew the elasticsearch certificate if its validity is shorter than this value, which should be number of days. (default: 30)
* *elasticsearch_cert_will_expire_soon*: Set it to true to renew elasticsearch certificate (default: `false`), Or run the playbook with `--tags renew_elasticsearch_cert` to do that.
* *elasticsearch_datapath*: Path where Elasticsearch will store it's data. (default: `/var/lib/elasticsearch` - the packages default)
* *elasticsearch_create_datapath*: Create the path for data to store if it doesn't exist. (default: `false` - only useful if you change `elasticsearch_datapath`)
* *elasticsearch_logpath*: Path where Elasticsearch will store it's logs. (default: `/var/log/elasticsearch` - the packages default)
* *elasticsearch_create_logpath*: Create the path for log to store if it doesn't exist. (default: `false` - only useful if you change `elasticsearch_datapath`)
* *elasticsearch_fs_repo*: List of paths that should be registered as repository for snapshots (only filesystem supported so far). (default: none) Remember, that every node needs access to the same share under the same path.
* *elasticsearch_bootstrap_pw*: Bootstrap password for Elasticsearch (Default: `PleaseChangeMe`)
* *elasticsearch_disable_systemcallfilterchecks*: Disable system call filter checks. This has a security impact but is necessary on some systems. Please refer to the [docs](https://www.elastic.co/guide/en/elasticsearch/reference/7.17/_system_call_filter_check.html) for details. (default: `false`)
* *elasticsearch_http_publish_host*: (String) The network address for HTTP clients to contact the node using sniffing. Accepts an IP address, a hostname, or a special value. (default: `not set`)
* *elasticsearch_http_publish_port*: (integer) The port of the HTTP publish address. Configure this setting only if you need the publish port to be different from http.port. (default: `not set`)
* *elasticsearch_pamlimits*: Set pam_limits neccessary for Elasticsearch. (Default: `true`)
* *elasticsearch_check_calculation*: End play in checks (Default: `false`)
* *elasticsearch_network_host*: You can configure multipe network addresses where the networking is bind to. You can assign IP addresses or interfaces by their names. You can also use elasticsearch internal variabels as it set as default. Example: `"_ens190_,_local_"` (Default: `"_local_,"_site_"`) (Optional; if not defined `default` is used)
* *elasticsearch_api_host*: Hostname or IP elasticsearch is listening on. Only used for connection checks by ansible role. (Default: `localhost`)
* *elasticsearch_extra_config*: You can set additional configuration in YAML-notation as you would write in the `elasaticsearch.yml`. Example:

```YAML
...
elasticsearch_extra_config:
  xpack.security.authc.token.enabled: true

    xpack.security.authc.realms:
        native.native1:
            order: 0
            enabled: true
```
* *elasticsearch_keystore_extra*: You can set additional items for the elasticsearch keystore. Example:
```YAML
...
elasticsearch_keystore_extra:
  the.setting.name.to.set: "some value",
  the.other.setting.name.to.set: "some other value"

```

* *elasticsearch_keystore_purge*: Purge items from keystore not set by this role. (Default: false)

This variable activates a workaround to start on systems that have certain hardening measures active. See [Stackoverflow](https://stackoverflow.com/questions/47824643/unable-to-load-jna-native-support-library-elasticsearch-6-x/50371992#50371992) for details and logmessages to look for. **WARNING**: This will change your `/etc/sysconfig/elasticseach`or `/etc/default/elasticsearch` file and overwrite `ES_JAVA_OPTS`. See this [issue](https://github.com/netways/ansible-role-elasticsearch/issues/79) for details.

* *elasticsearch_jna_workaround*: Activate JNA workaround. (default: `false`)
* *elasticsearch_ssl_verification_mode*: Defines how to verify the certificates presented by another party in the TLS connection
* *elasticsearch_transport_port*: The port to bind for communication between nodes
* *elasticsearch_seed_hosts*: Set elasticsearch seed hosts
* *elasticsearch_security_enrollment*: Controls enrollment (of nodes and Kibana) to a local node that’s been autoconfigured for security.

The following variable was only integrated to speed up upgrades of non-production clusters. Use with caution and at your own risk:

* *elasticsearch_unsafe_upgrade_restart*: This will still perform rolling upgrades, but will first update the package and then restart the service. In contrast the default behaviour is to stop the service, do the upgrade and then start again. (default: `false`)

These variables are identical over all our elastic related roles, hence the different naming schemes.

* *elasticstack_ca_host*: Set to the inventory hostname of the host that should house the CA for certificates for inter-node communication. (default: First node in the `elasticsearch` host group)
* *elasticstack_ca_name*: Distinguished name of the CA. (default: `CN=Elastic Certificate Tool Autogenerated CA`)
* *elasticstack_ca_pass*: Password for Elasticsearch CA (default: `PleaseChangeMe`)
* *elasticstack_ca_validity_period*: number of days that the generated CA are valid (default: 1095).
* *elasticstack_ca_expiration_buffer*: Ansible will renew the CA if its validity is shorter than this value, which should be number of days. (default: 30)
* *elasticstack_ca_will_expire_soon*: Set it to true to renew the CA and the certificate of all Elastic Stack components (default: `false`), Or run the playbook with `--tags renew_ca` to do that.
* *elasticstack_release*: Major release version of Elastic stack to configure. (default: `7`)
* *elasticstack_variant*: Variant of the stack to install. Valid values: `elastic` or `oss`. (default: `elastic`)
* *elasticstack_elasticsearch_http_port*: Port of Elasticsearch http (Default: `9200`)

```
- name: Install Elasticsearch
  collections:
    - netways.elasticstack
  hosts: elasticsearch-hosts
  vars:
    elasticstack_variant: oss
    elasticsearch_jna_workaround: true
    elasticsearch_disable_systemcallfilterchecks: true
  roles:
    - repos
    - elasticsearch
```
