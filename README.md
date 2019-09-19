Ansible Role: Logstash
=========

This role installs and configures [Logstash](https://www.elastic.co/products/logstash) on Linux systems.

It can optionally configure two types of Logstash pipelines:
* Pipeline configuration managed in an external git repository
* A default pipeline which will read from different Redis keys and write into Elasticsearch

Requirements
------------

This role has no Requirements.

If you want to use the default pipeline (or other pipelines communicating via Redis) you might want to install Redis first (e.g. by using an [Ansible Role for Redis](https://galaxy.ansible.com/geerlingguy/redis)

Role Variables
--------------

This role is still in development. Please refer to `defaults/main.yml` for the current set of available variables.

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
