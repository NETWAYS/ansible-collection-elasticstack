# Pipelines #

This only refers to "non-connector" pipelines.

## Git managed ##

If you have pipeline code managed in (and available via) Git repositories, you can use this role to check them out and integrate them into `pipelines.yml`.

```
logstash_pipelines:
  syslog:
    name: syslog
    source: https://github.com/widhalmt/syslog-logstash-pipeline.git
```

## Custom pipelines ##

If you have other ways of putting pipeline code into the correct directories, you can just skip the `source` option.

```
logstash_pipelines:
  syslog:
    name: syslog
```
**You have to make sure the code is available or Logstash will constantly log errors!**

This will create the directories and integrate all `*.conf` files within via `pipelines.yml`.
