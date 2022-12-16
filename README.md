Ansible Role: Logstash
=========

[![CI](https://github.com/NETWAYS/ansible-role-logstash/workflows/Molecule%20Test/badge.svg?event=push)](https://github.com/NETWAYS/ansible-role-logstash/workflows/Molecule%20Test/badge.svg)

This role installs and configures [Logstash](https://www.elastic.co/products/logstash) on Linux systems.

It can optionally configure two types of Logstash pipelines:
* Pipeline configuration managed in an external git repository
* A default pipeline which will read from different Redis keys and write into Elasticsearch

Details about configured pipelines will be written into `pipelines.yml` as comments. Same goes for logging configuration in `log4j.options`. 

It will work with the standard Elastic Stack packages and Elastics OSS variant.

Requirements
------------

* `community.general` collection

You need to have the Elastic Repos configured on your system. You can use our [role](https://github.com/widhalmt/ansible-role-elastic-repos) for that but you don't have to.

If you want to use the default pipeline configuration you need to have `git` available.

You need to have `curl` installed. We are using `curl` instead of the `uri` module because we got better results. Feel free to file a pull request if you find a working solution. (And please remove this line with it)

If you want to use the default pipeline (or other pipelines communicating via Redis) you might want to install Redis first (e.g. by using an [Ansible Role for Redis](https://galaxy.ansible.com/geerlingguy/redis)

Role Variables
--------------

* *logstash_version*: Version number of Logstash to install (use os specific version string. e.g. `-7.10.1` for RedHat compatible systems or `=1:7.10.1-1` for Debian compatible systems). Only set if you don't want the latest. (default: none). For OSS version see `elastic_variant` below.
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
* *logstash_pipelines*: List of pipelines with optional URL to repo (see docs/pipelines.md for details)
* *logstash_global_ecs*: Set ECS compatibilty mode (default: none. Possible values: `disabled` or `v1`)
* *logstash_elasticsearch_output*: Enable default pipeline to Elasticsearch (default: `true`)
* *logstash_beats_input*: Enable default pipeline with `beats` input (default: `true`)
* *logstash_beats_input_congestion*: Optional congestion threshold for the beats input pipeline
* *logstash_beats_tls*: Activate TLS for the beats input pipeline (default: none but `true` with full stack setup if not set)
* *logstash_beats_tls_encryptkey*: Enable encryption of key for beats input - disabling used as a workaround on certain hosts (default: true)
* *logstash_tls_key_passphrase*: Passphrase for Logstash certificates (default: `ChangeMe`)
* *logstash_connector*: Create pipelines to connect git managed pipelines. (default: `true`)
* *logstash_connector_pipelines*: Definition of connector pipelines. See docs/connector-pipelines.md for details
* *logstash_elasticsearch*: Address of Elasticsearch instance for default output (default: list of Elasticsearch nodes from `elasticsearch` role or `localhost` when used standalone)
* *logstash_security*: Enable X-Security (No default set, but will be activated when in full stack mode)
* *logstash_legacy_monitoring*: Enables legacy monitoring - ignored when `elastic_stack_full_stack` is not set. (default: `true`)

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

*elastic_release*: Major release version of Elastic stack to configure. (default: `7`)
*elastic_variant*: Variant of the stack to install. Valid values: `elastic` or `oss`. (default: `elastic`)

The following variables only apply if you use this role together with our Elasticsearch and Kibana roles.

* *elastic_stack_full_stack*: Use `ansible-role-elasticsearch` as well (default: `false`)
* *elastic_ca_dir*: Directory where the CA and certificates lie on the main Elasticsearch host (default: `/opt/es-ca`)
* *elastic_initial_passwords*: File where initial passwords are stored on the main Elasticsearch host (default: `/usr/share/elasticsearch/initial_passwords`)

Dependencies
------------

This role has no dependencies. As mentioned above you might want to use another role to install Redis

Example Playbook
----------------

This is a simple sample playbook which first uses an Ansible role to install Redis and afterwards install and configure Logstash.

    - hosts: logstash
      roles:
        - geerlingguy.redis
        - logstash


License
-------

GPLv3+

Author Information
------------------

This role was created in 2019 by [Netways](https://www.netways.de/).
