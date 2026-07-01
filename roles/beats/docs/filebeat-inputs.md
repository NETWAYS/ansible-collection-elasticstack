# Filebeat inputs #

Filebeat can read from several sources. Each source is turned into a Filebeat
input by the role. This document describes the variables that configure them.
For the meaning of the individual Filebeat options, follow the links to the
official Filebeat documentation.

## Log files ##

Set with `beats_filebeat_log_input` (default `true`) and `beats_filebeat_log_inputs`.

`beats_filebeat_log_inputs` is a **dictionary keyed by a free name**. That key
becomes the id of the generated
[`filestream`](https://www.elastic.co/docs/reference/beats/filebeat/filebeat-input-filestream)
input (`<key>-filestream`) — there is no separate `name` field. Each entry needs
`paths`; `fields` and `multiline` are optional.

The default reads the system log:

```yaml
beats_filebeat_log_inputs:
  messages:
    paths:
      - /var/log/messages
      - /var/log/syslog
```

A longer example with several paths and multiline handling:

```yaml
beats_filebeat_log_inputs:
  messages:
    paths:
      - /var/log/messages
      - /var/log/secure
      - /var/log/httpd/*access_log*
    multiline:
      type: pattern
      pattern: '^[[:space:]]+(at|\.{3})[[:space:]]+\b|^Caused by:'
      negate: false
      match: after
```

`multiline` maps directly to the Filebeat multiline parser (`type`, `pattern`,
`negate`, `match`). See
[Manage multiline messages](https://www.elastic.co/docs/reference/beats/filebeat/multiline-examples).

## Fields ##

There are two ways to add fields, and they use **different shapes**:

* **Per input** — the optional `fields` inside a log input is a **dictionary**
  (`key: value`), added only to that input:

  ```yaml
  beats_filebeat_log_inputs:
    messages:
      paths:
        - /var/log/messages
      fields:
        environment: production
  ```

* **Globally** — `beats_fields` is a **list of `"key: value"` strings**. In the
  current templates it is added to the log, TCP and UDP inputs; the journald,
  Docker and MySQL slow-log inputs do not receive it:

  ```yaml
  beats_fields:
    - "environment: production"
    - "team: platform"
  ```

## Syslog over TCP/UDP ##

Enable a listening syslog input with `beats_filebeat_syslog_tcp` /
`beats_filebeat_syslog_udp` and set the port with `beats_filebeat_syslog_tcp_port`
/ `beats_filebeat_syslog_udp_port` (both default `514`). They become a
[`tcp`](https://www.elastic.co/docs/reference/beats/filebeat/filebeat-input-tcp)
or [`udp`](https://www.elastic.co/docs/reference/beats/filebeat/filebeat-input-udp)
input listening on `0.0.0.0:<port>`. The global `beats_fields` are applied here too.

```yaml
beats_filebeat_syslog_tcp: true
beats_filebeat_syslog_tcp_port: 514
```

## Journald ##

Enable with `beats_filebeat_journald` (default `false`, available since Filebeat
7.16) and configure inputs with `beats_filebeat_journald_inputs`.

Like the log inputs, this is a **dictionary keyed by a free name**. Each entry
needs an `id`; `include_matches` is optional and is itself a dictionary whose
values are the match expressions.

```yaml
beats_filebeat_journald_inputs:
  everything:
    id: everything
  ssh-only:
    id: ssh-only
    include_matches:
      unit: '_SYSTEMD_UNIT=sshd.service'
```

See the
[`journald`](https://www.elastic.co/docs/reference/beats/filebeat/filebeat-input-journald)
input.

## Docker ##

Enable with `beats_filebeat_docker` (default `false`) and select containers with
`beats_filebeat_docker_ids` (default `*`). **Only works on Elastic Stack release
7.** Docker metadata is added automatically.

```yaml
beats_filebeat_docker: true
beats_filebeat_docker_ids: "*"
```

## MySQL/MariaDB slow log ##

Set `beats_filebeat_mysql_slowlog_input` to `true` to collect
`/var/log/mysql/*-slow.log` with the matching multiline pattern already
configured. The events are tagged with `mysql.logtype: slowquery`.

## Modules ##

`beats_filebeat_modules` is a list of Filebeat module names to enable
(**experimental**, unset by default). The role runs `filebeat modules enable`
and sets up their ingest pipelines.

On Elastic Stack release 8 and newer (`elasticstack_release > 7`), enabling any
modules also deploys a predefined **System module** configuration to
`modules.d/system.yml`, which collects the syslog files (`/var/log/syslog`,
`/var/log/messages`) through the system module's `syslog` fileset.

```yaml
beats_filebeat_modules:
  - system
  - nginx
```

See the
[Filebeat modules](https://www.elastic.co/docs/reference/beats/filebeat/filebeat-modules)
reference for the available modules.
