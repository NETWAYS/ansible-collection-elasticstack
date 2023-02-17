Elastic Repos
=========

![Test Role repos](https://github.com/netways/ansible-collection-elasticstack/actions/workflows/test_role_repos.yml/badge.svg)

The role adds Elastic repositories to the package manager. It's main use is in connection with other roles that provide installation and configuration of the Elastic Stack.

Requirements
------------

* You need `gpg` to be installed because packages / repositories are digitally signed and verified.
* Debian and Ubuntu hosts need to have `apt-transport-https` installed to deal with Elastics repositories.
* Ubuntu hosts also need to have `gpg-agent` installed.
* For SuSE hosts you need the Ansible collection `community.general` on your Ansible controller

Role Variables
--------------

* *elastic_release*: Major release version of Elastic stack to configure. (default: `7`). `7` and `8` are supported.
* *elastic_variant*: Variant of the stack to install. Valid values: `elastic` or `oss`. (default: `elastic`).

Please note that no `oss` versions are available for Elastic Stack later than `7`. This role will fail if you try to install them.

Usage
--------

```
  - hosts: all
    become: yes
    collections:
      - netways.elasticstack
    roles:
      - repos
```
