# Requirements

Software requirements, supported Ansible and Python versions and external libraries are listed
in the [README](../README.md#tested-with-ansible). This page describes what the roles expect
from your setup.

Some of these will be refactored and disappear from this list.

## Inventory group names

The collection provides roles for several tools, and some tasks fetch hosts from a specific
inventory group. The group names are customizable through variables, but using group names that
differ from those variables results in errors.

| Variable | Default group name |
|---|---|
| `elasticstack_elasticsearch_group_name` | `elasticsearch` |
| `elasticstack_logstash_group_name` | `logstash` |
| `elasticstack_kibana_group_name` | `kibana` |

## elasticstack_ca_host

This variable defines the host that acts as the certificate authority. It has a default: the
first host in the group named by `elasticstack_elasticsearch_group_name`.

That default only resolves when that group exists. If you use different group names without
setting them in the variables above, the variable ends up empty and the run fails.
