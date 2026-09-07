# Versions and upgrades

## Choosing a version

`elasticstack_version` holds the version number of the tools to install, for example `8.19.4`.
Only set it if you do not want the newest available version on a new setup. There is no default.

If you already have an installation of the Elastic Stack, the collection queries the installed
version of Elasticsearch on the CA host and uses it for all further installations in the same
setup. This only happens when you run the `elasticsearch` role before all others.

All packages are installed with `state: present`:

* When `elasticstack_version` is set to a version number, that exact version is installed and
  pinned.
* When it is left unset, the package is installed without a version. A new setup gets the newest
  available version, and existing installations are not upgraded automatically on later runs.

`elasticstack_release` holds the major release, for example `8` (default). If you set both, make
sure they match.

For the OSS variant see `elasticstack_variant`, described with the
[elasticstack role](../roles/elasticstack/README.md).

Both variables can be set per role, which is how you keep components on different versions:

```yaml
roles:
  - role: netways.elasticstack.kibana
    vars:
      elasticstack_version: 8.7.1
  - role: netways.elasticstack.elasticsearch
    vars:
      elasticstack_version: 8.8.1
```

## Upgrading

Set `elasticstack_version` to the version you want to upgrade to.

Before you do, read and understand Elastic's changelog and the breaking changes of your target
version **and of every version between your current one and the target**. Do not upgrade without
a valid backup.

Elasticsearch nodes are upgraded one at a time. The role disables shard allocation, stops the
node, installs the new package, starts it again and waits for the node to rejoin before it
touches the next one.

If an upgrade fails, you can try re-running the collection with the same settings. Several tasks
provide a degree of self-healing. Do not rely on these mechanisms, they are a convenience
recovery for the easier cases and not a substitute for a backup.
