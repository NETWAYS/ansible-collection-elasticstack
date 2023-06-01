Ansible Role: Logstash
=========

![Test Role Logstash](https://github.com/netways/ansible-collection-elasticstack/actions/workflows/test_role_logstash.yml/badge.svg)

This role installs and configures [Logstash](https://www.elastic.co/products/logstash) on Linux systems.

It can optionally configure two types of Logstash pipelines:
* Pipeline configuration managed in an external git repository
* A default pipeline which will read from different Redis keys and write into Elasticsearch

For details on how to configure pipelines please refer to our [docs about pipelines](./logstash-pipelines.md).

Details about configured pipelines will be written into `pipelines.yml` as comments. Same goes for logging configuration in `log4j.options`.

It will work with the standard Elastic Stack packages and Elastics OSS variant.

Requirements
------------

* `community.general` collection
* `cryptography` >= 2.5

You need to have the Elastic Repos configured on your system. You can use our [role](./role-repos.md)

If you want to use the default pipeline configuration you need to have `git` available.

You need to have `curl` installed. We are using `curl` instead of the `uri` module because we got better results. Feel free to file a pull request if you find a working solution. (And please remove this line with it)

If you want to use the default pipeline (or other pipelines communicating via Redis) you might want to install Redis first (e.g. by using an [Ansible Role for Redis](https://galaxy.ansible.com/geerlingguy/redis)

Role Variables
--------------

* *elasticstack_version*: Version number of Logstash to install (e.g. `7.10.1`). Only set if you don't want the latest. (default: none). For OSS version see `elasticstack_variant` below.
* *logstash_enable*: Start and enable Logstash service (default: `true`)
* *logstash_config_backup*: Keep backups of all changed configuration (default: `no`)
* *logstash_manage_yaml*: Manage and overwrite `logstash.yml` (default: `true`)
* *logstash_manage_logging*: Manage log4j configuration (default: `false`)
* *logstash_plugins*: List of plugins to install (default: none)
* *logstash_certs_dir*: Path to certificates. Will be used to build paths of several files. (Default: `/etc/logstash/certs`)

If `logstash.yml` is managed, the following settings apply.

* *logstash_config_autoreload*: Enable autoreload of Logstash configuration (default: `true`)
* *logstash_config_path_data*: Logstash data directory (default: `/var/lib/logstash`)
* *logstash_config_path_logs*: Logstash log directory (default: `/var/log/logstash`)

Aside from `logstash.yml` we can manage Logstashs pipelines.

* *logstash_manage_pipelines*: Manage `pipelines.yml` (default: `true`)
* *logstash_no_pipelines*: Don't manage pipelines at all (default: `false`)
* *logstash_pipelines*: List of pipelines with optional URL to repo (see [pipelines documentation](file:///roles/logstash/docs/pipelines.md) for details)
* *logstash_global_ecs*: Set ECS compatibilty mode (default: none. Possible values: `disabled` or `v1`)
* *logstash_elasticsearch_output*: Enable default pipeline to Elasticsearch (default: `true`)
* *logstash_ident*: Add a field identifying the node that processed an event (default: `true`)
* *logstash_ident_field_name*: Name of the identifying the instance (default: `"[netways][instance]"`)
* *logstash_beats_input*: Enable default pipeline with `beats` input (default: `true`)
* *logstash_beats_input_congestion*: Optional congestion threshold for the beats input pipeline
* *logstash_beats_tls*: Activate TLS for the beats input pipeline (default: none but `true` with full stack setup if not set)
* *logstash_tls_key_passphrase*: Passphrase for Logstash certificates (default: `LogstashChangeMe`)
* *elasticstack_ca_pass*: Password for Elasticsearch CA (default: `PleaseChangeMe`)
* *logstash_cert_expiration_buffer*: Ansible will renew the Logstash certificate if its validity is shorter than this value, which should be number of days. (default: 30)
* *logstash_cert_will_expire_soon*: Set it to true to renew logstash certificate (default: `false`), Or run the playbook with `--tags renew_logstash_cert` to do that.
* *logstash_elasticsearch*: Address of Elasticsearch instance for default output (default: list of Elasticsearch nodes from `elasticsearch` role or `localhost` when used standalone)
* *logstash_security*: Enable X-Security (No default set, but will be activated when in full stack mode)
* *logstash_user*: Name of the user to connect to Elasticsearch (Default: `logstash_writer`)
* *logstash_password*: Password of Elasticsearch user (Default: `password`)
* *logstash_user_indices*: Indices the user has access to (Default: `'"ecs-logstash*", "logstash*", "logs*"'`)
* *logstash_reset_writer_role*: Reset user and role with every run: (Default: `true`)
* *logstash_validate_after_inactivity*: How long should logstash wait, before starting a new connection and leave the old one with elasticsearch, when the connection with elasticsearch get lost: (Default: `300`).
* *logstash_queue_type*: What kind of queue should Logstash use per default: (Default: `persisted`, alternative: `memory`)
* *logstash_queue_max_bytes*: The total capacity of ansible-forwarder queue in number of bytes: (Default: `2gb`)



* *logstash_legacy_monitoring*: Enables legacy monitoring - ignored when `elasticstack_full_stack` is not set. (default: `true`)

The following variables configure Log4j for Logstash. All default to `true` as this is the default after the installation.

* *logstash_logging_console*: Log to console - syslog when run via systemd
* *logstash_logging_file*: Log to logfile
* *logstash_logging_slow_console*: Log slowlog to console - syslog when run via systemd
* *logstash_logging_slow_file*: Log slowlog to logfile

The following variables configure extra fields in your events that help with identifying which pipelines have been passed or which pipeline is used how much.

* *logstash_pipeline_identifier*: Activate this feature (default: `true`)
* *logstash_pipeline_identifier_field_name*: Name of the field to add (default: `"[netways][pipeline]"`)
* *logstash_pipeline_identifier_defaults*: Use identifiers in default pipelines, too (default: `false`) This could lead to the defaults dominating all statistics with virtually no value, but if you want to see, them, you can.

The following variables are identical over all our elastic related roles, hence the different naming scheme.

*elasticstack_release*: Major release version of Elastic stack to configure. (default: `7`)
*elasticstack_variant*: Variant of the stack to install. Valid values: `elastic` or `oss`. (default: `elastic`)

The following variables only apply if you use this role together with our Elasticsearch and Kibana roles.

* *elasticstack_full_stack*: Use `ansible-role-elasticsearch` as well (default: `false`)
* *elasticstack_ca_dir*: Directory where the CA and certificates lie on the main Elasticsearch host (default: `/opt/es-ca`)
* *elasticstack_elasticsearch_http_port*: Port of Elasticsearch to send events to (Default: `9200`)
* *elasticstack_initial_passwords*: File where initial passwords are stored on the main Elasticsearch host (default: `/usr/share/elasticsearch/initial_passwords`)

## Usage

```
- name: Install Logstash
  hosts: logstash-host
  collections:
    - netways.elasticstack
  roles:
    - repos
    - logstash
```
