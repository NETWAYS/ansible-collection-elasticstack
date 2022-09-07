Elastic Repos
=========

[![CI](https://github.com/widhalmt/ansible-role-elastic-repos/workflows/CI/badge.svg?event=push)](https://github.com/widhalmt/ansible-role-elastic-repos/actions?query=workflow%3ACI)

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

Dependencies
------------

None.

Example Playbook
----------------

    ---
    - hosts: localhost
      become: yes
      roles:
        - elastic-repos

License
-------

GPL 3.0

Author Information
------------------

* Thomas Widhalm <thomas.widhalm@netways.de>
