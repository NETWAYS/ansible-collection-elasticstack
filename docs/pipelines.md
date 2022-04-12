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

You can add a `version` attribute to your pipeline. It defaults to `main`. You can use every string, [Ansibles git](https://docs.ansible.com/ansible/latest/collections/ansible/builtin/git_module.html) module accepts.

## Input and Output ##

### Basic configuration ###

To have a single Redis input and output to your files, use this.

```
logstash_pipelines:
  syslog:
    name: syslog
    source: https://github.com/widhalmt/syslog-logstash-pipeline.git
    exclusive: false
    input:
      - name: default
        key: syslog-input
    output:
      - name: default
        key: syslog-output
```

This will result in your pipeline checking out the configuration on GitHub and adding these two extras. In extra files, just shown in one place to safe space.

```
input {
  redis {
    host => "localhost"
    data_type => "list"
    key => "syslog-input"
  }
}
output {
  redis {
    host => "localhost"
    data_type => "list"
    key => "syslog-output"
  }
}
```

### Multiple inputs ###

Just give more inputs with `name` and `key`. Every key will be read.

### More complex configuration ###

If you want a bit more control over which outputs are used, the role offers more sophisticated configuration.

If you have several outputs that all have conditions, like just send some messages to a development system or only alerts to a monitoring system.

```
logstash_pipelines:
  syslog:
    name: syslog
    source: https://github.com/widhalmt/syslog-logstash-pipeline.git
    exclusive: false
    input:
      - name: default
        key: input
    output:
      - name: special
        key: myspecial
        condition: '[program] == "special"'
      - name: special2
        key: myspecial2
        condition: '[program] == "special2"'
      - name: default
        key: forwarder
```
This will give you the following configuration:

```
input {

# default output
  redis {
    host => "localhost"
    data_type => "list"
    key => "input"
  }

}

output {

# special output
if [program] == "special"{
  redis {
    host => "localhost"
    data_type => "list"
    key => "myspecial"
  }
}

# special2 output
if [program] == "special2"{
  redis {
    host => "localhost"
    data_type => "list"
    key => "myspecial2"
  }
}

# default output
  redis {
    host => "localhost"
    data_type => "list"
    key => "forwarder"
  }

}
```

Note that the `default` output get's **every** event, the other two outputs only get those where the condition is met.

You can combine several outputs with `else`. That's helpful when you want to split events. Like syslog messages depending on which program logged an event. Just change `exclusive` to `true`.

```
logstash_pipelines:
  syslog:
    name: syslog
    source: https://github.com/widhalmt/syslog-logstash-pipeline.git
    exclusive: true
    input:
      - name: default
        key: input
    output:
      - name: special
        key: myspecial
        condition: '[program] == "special"'
      - name: special2
        key: myspecial2
        condition: '[program] == "special2"'
      - name: default
        key: forwarder
```

This will give you the following Logstash configuration.

```
input {

# default output
  redis {
    host => "localhost"
    data_type => "list"
    key => "input"
  }

}

output {

# special output
if [program] == "special" {
  redis {
    host => "localhost"
    data_type => "list"
    key => "myspecial"
  }
}
# special2 output
else if [program] == "special2" {
  redis {
    host => "localhost"
    data_type => "list"
    key => "myspecial2"
  }
}

# default output
else  {
  redis {
    host => "localhost"
    data_type => "list"
    key => "forwarder"
  }

}

}
```

Here the `default` output only receives the events that haven't already been sent to one of the others.

## Extra configuration ##

### Congestion threshold ###

Every Output can have a `congestion:` option with a numerical value. If the Redis key already holds more items than the value says, the output will stop.

## Caveats ##

There are still some minor issues you need to keep in mind:

* The default output in an `exclusive: true` setup must be the last in the YAML configuration. There's no sorting, the role simply expects the default to be the last one.
* The configuration *should* work but will make no sense if you have `exclusive: true` but two or more outputs without `condition`.

## Custom pipelines ##

If you have other ways of putting pipeline code into the correct directories, you can just skip the `source` option.

```
logstash_pipelines:
  syslog:
    name: syslog
```
**You have to make sure the code is available or Logstash will constantly log errors!**

This will create the directories and integrate all `*.conf` files within via `pipelines.yml`.
