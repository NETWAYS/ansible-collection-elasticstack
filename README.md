Elastic Repos
=========

[![CI](https://github.com/widhalmt/ansible-role-elastic-repos/workflows/CI/badge.svg?event=push)](https://github.com/widhalmt/ansible-role-elastic-repos/actions?query=workflow%3ACI)

The role adds Elastic repositories to the package manager. It's main use is in connection with other roles that provide installation and configuration of the Elastic Stack.

Requirements
------------

You need `gpg` to be installed because packages / repositories are digitally signed and verified.

Debian and Ubuntu hosts need to have `apt-transport-https` installed to deal with Elastics repositories.

Role Variables
--------------

*elastic_release*: Major release version of Elastic stack to configure. (default: `7`)

Dependencies
------------

None.

Example Playbook
----------------

Including an example of how to use your role (for instance, with variables passed in as parameters) is always nice for users too:

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
