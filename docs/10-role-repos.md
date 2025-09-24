Elastic Repos
=========

![Test Role repos](https://github.com/netways/ansible-collection-elasticstack/actions/workflows/test_role_repos.yml/badge.svg)

The role adds Elastic repositories to the package manager. It's main use is in connection with other roles that provide installation and configuration of the Elastic Stack.

Requirements
------------

GPG needs to be installed on the systems to verify the package signature. This will be installed as part of the role. Below you can find a list of packages that will be installed.
* Debian family: `apt-transport-https`, `gpg` and `gpg-agent`
* RedHat family: `gnupg`
* Suse family: `gpg2`

For SuSE hosts you will need the Ansible collection `community.general` on your Ansible controller.

Role Variables
--------------

* *elasticstack_release*: Major release version of Elastic stack to configure. (default: `7`). `7` and `8` are supported.
* *elasticstack_variant*: Variant of the stack to install. Valid values: `elastic` or `oss`. (default: `elastic`).
* *elasticstack_enable_repos*: Enable repositories after creating them. (default: `true`) Only works on RPM based distributions!

Please note that no `oss` versions are available for Elastic Stack later than `7`. This role will fail if you try to install them.

Usage
--------

Upgrades
========

If you want to be able to update your operating system without worrying about accidentally upgrading Elastic Stack, set `elasticstack_enable_repos` to `false`. The roles in this collection will enable the repository in case they need it. Keep in mind that this will only work on rpm based distributions.

Example playbook
================

```
  - hosts: all
    become: yes
    collections:
      - netways.elasticstack
    roles:
      - repos
```
