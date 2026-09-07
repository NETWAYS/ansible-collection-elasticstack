# Ansible Collection - netways.elasticstack

This collection installs and manages the Elastic Stack. It provides roles for every component
of the Stack, and it can install either the default Elastic distribution or the Apache-licensed
OSS packages.

Every role can be used on its own or together with the others. Running a single role against an
existing or external cluster works, but a few of those paths are still incomplete. See the open
issues for details.

## Tested with Ansible

The minimum required version is declared in [meta/runtime.yml](meta/runtime.yml) and enforced by
`ansible-galaxy` on install.

| | |
|---|---|
| ansible-core | `>= 2.18`, tested with 2.19 and 2.20 |
| Python on the control node | `>= 3.11` |
| Python on the target hosts | `>= 3.9` |
| Elastic Stack | release 8 |

We test on the following Linux distributions, each one with Elastic Stack 8:

* Rocky Linux 9
* Ubuntu 22.04 LTS
* Debian 13

## External requirements

Ansible collections, both are declared as dependencies and installed for you when you install
this collection with `ansible-galaxy`:

* `community.general`, for the `zypper` modules on SUSE hosts and the Logstash plugin module
* `community.crypto`, used by the beats role to check when a certificate expires

Python libraries on the control node:

* `passlib`, unless you disable password hashing for the Logstash user and you want to use the
  logstash role. Install it with `pip`.
* `elasticsearch`. Current versions are compatible either with Elasticsearch 9 or with versions
  lower than 9, there seems to be no version that serves both. For now we install a client
  older than 9, and this needs revisiting when the collection becomes compatible with Elastic
  Stack 9.

Ansible roles:

* `geerlingguy.redis` if you want to use the logstash role. There are other ways to get Redis
  running, but this one is easy and convenient.

  ```bash
  ansible-galaxy install geerlingguy.redis
  ```

Some very basic packages such as `openssl` are handled by the collection itself. The list above
only contains what applies to special cases or what you need to decide about yourself.

Beyond software, the roles expect a few things from your inventory. See
[Requirements](docs/requirements.md).

## Included content

Roles:

* [beats](roles/beats/README.md)
* [elasticsearch](roles/elasticsearch/README.md)
* [kibana](roles/kibana/README.md)
* [logstash](roles/logstash/README.md)
* [repos](roles/repos/README.md)
* [elasticstack](roles/elasticstack/README.md), the meta role that holds the collection-wide
  `elasticstack_*` variables

Modules:

* `cert_info`, reads information from a PKCS12 certificate
* `elasticsearch_role`, creates, updates and deletes roles in Elasticsearch
* `elasticsearch_user`, creates, updates and deletes users in Elasticsearch

Each module documents its own parameters, return values and examples. Read them with
`ansible-doc`, for example:

```bash
ansible-doc netways.elasticstack.elasticsearch_role
```

## Collection documentation

* [Getting started](docs/getting-started.md), example playbook, inventory groups, first run
* [Requirements](docs/requirements.md), what the roles expect from your inventory
* [Versions and upgrades](docs/upgrades.md), pinning versions and upgrading the stack

Every role documents all of its variables in its own README, linked above. Those tables are
generated from each role's `meta/argument_specs.yml`. Module documentation comes from the
modules themselves and is read with `ansible-doc`.

## Using this collection

Install the collection with `ansible-galaxy`:

```bash
ansible-galaxy collection install netways.elasticstack
```

To pin a version, use a `requirements.yml`:

```yaml
collections:
  - name: netways.elasticstack
    version: 0.1.0
```

```bash
ansible-galaxy collection install -r requirements.yml
```

The same file works for Tower and AWX. You can also install straight from git, which gives you
the current state of `main` instead of a release:

```bash
ansible-galaxy collection install git+https://github.com/NETWAYS/ansible-collection-elasticstack.git
```

Then refer to the roles by their fully qualified name:

```yaml
- hosts: elasticsearch
  become: true
  roles:
    - netways.elasticstack.elasticsearch
```

The execution order of the roles matters, and the roles interact with hosts from other inventory
groups. Read [Getting started](docs/getting-started.md) before your first run.

## Caveats and information for long time users

### Variable renaming

If you have been using this collection before version `1.0.0`, note that a significant number of
variables had to be renamed because of naming schema changes made by Ansible. Please review the
variables you set in your playbooks and variable files.

### Ulimit management for Elasticsearch

The role no longer configures `ulimit`. Make sure the system's open file limit is set correctly,
packages usually handle this. Verify with `ulimit -n` or by checking `/proc/<pid>/limits`. If
your version does not, please
[open an issue](https://github.com/NETWAYS/ansible-collection-elasticstack/issues).

## Contributing to this collection

Every kind of contribution is welcome. Open
[issues](https://github.com/NETWAYS/ansible-collection-elasticstack/issues) or provide
[pull requests](https://github.com/NETWAYS/ansible-collection-elasticstack/pulls).

Pull requests go against `main`. If you need a stable state, pin a release tag.

Please read [CONTRIBUTING.md](CONTRIBUTING.md) first. It describes what a pull request needs,
including the changelog fragment that every pull request has to bring along, how role variables
are documented and how to run the tests.

## Release notes

See the [releases page](https://github.com/NETWAYS/ansible-collection-elasticstack/releases).
The same notes are collected in `CHANGELOG.md`, which is generated from the changelog fragments
when a version is released.

## Licensing

GPL-3.0-or-later, see [LICENSE](LICENSE).
