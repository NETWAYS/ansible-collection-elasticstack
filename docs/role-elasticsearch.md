ELASTICSEARCH
=========

![Test Role Elasticsearch](https://github.com/netways/ansible-collection-elasticstack/actions/workflows/test_role_elasticsearch.yml/badge.svg)

This role installs manages Elasticsearch on your hosts. Optionally it can configure Elastics Security components, too.

If you use the role to set up security you can use its CA to create certificates for Logstash and Kibana, too.

Please note that setting `elasticsearch_bootstrap_pw` as variable will only take effect when initialising Elasticsearch. Changes after starting elasticsearch for the first time will not change the bootstrap password for the instance and will lead to breaking tests.

Role Variables
--------------

* *elasticsearch_enable*: Start and enable Elasticsearch (default: `true`)
* *elasticsearch_heap*: Heapsize for Elasticsearch. (Half of free memory on host. Maximum 30GB. (default: Half of hosts memory. Min 1GB, Max 30GB)
* *elasticsearch_ca*: Set to the inventory hostname of the host that should house the CA for certificates for inter-node communication. (default: First node in the `elasticsearch` host group)
* *elasticsearch_datapath*: Path where Elasticsearch will store it's data. (default: `/var/lib/elasticsearch` - the packages default)
* *elasticsearch_create_datapath*: Create the path for data to store if it doesn't exist. (default: `false` - only useful if you change `elasticsearch_datapath`)
* *elasticsearch_fs_repo*: List of paths that should be registered as repository for snapshots (only filesystem supported so far). (default: none) Remember, that every node needs access to the same share under the same path.
* *elasticsearch_bootstrap_pw*: Bootstrap password for Elasticsearch (Default: `PleaseChangeMe`)
* *elasticsearch_disable_systemcallfilterchecks*: Disable system call filter checks. This has a security impact but is necessary on some systems. Please refer to the [docs](https://www.elastic.co/guide/en/elasticsearch/reference/7.17/_system_call_filter_check.html) for details. (default: `false`)
* *elasticsearch_pamlimits*: Set pam_limits neccessary for Elasticsearch. (Default: `true`)

This variable activates a workaround to start on systems that have certain hardening measures active. See [Stackoverflow](https://stackoverflow.com/questions/47824643/unable-to-load-jna-native-support-library-elasticsearch-6-x/50371992#50371992) for details and logmessages to look for. **WARNING**: This will change your `/etc/sysconfig/elasticseach`or `/etc/default/elasticsearch` file and overwrite `ES_JAVA_OPTS`. See this [issue](https://github.com/netways/ansible-role-elasticsearch/issues/79) for details.

* *elasticsearch_jna_workaround*: Activate JNA workaround. (default: `false`)

These variables are identical over all our elastic related roles, hence the different naming schemes.

* *elastic_release*: Major release version of Elastic stack to configure. (default: `7`)
* *elastic_variant*: Variant of the stack to install. Valid values: `elastic` or `oss`. (default: `elastic`)

```
- name: Install Elasticsearch
  collections:
    - netways.elasticstack
  hosts: elasticsearch-hosts
  vars:
    elastic_variant: oss
    elasticsearch_jna_workaround: true
    elasticsearch_disable_systemcallfilterchecks: true
  roles:
    - repos
    - elasticsearch
```
