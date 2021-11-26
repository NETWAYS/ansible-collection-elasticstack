# Connector pipelines #

This type of pipelines is special to this role. They are used to connect other pipelines so you don't have to mess with `input` and `output` configuration. This helps a lot with building reusable pipelines which can be shared between setups.

The problem with sharing Logstash configuration was that you never know which events are processed which naming scheme is used and how pipelines interact. This role is up to mitigate these problems:

* You'll find more and more pipelines that work for different kinds of logs. Just put them into your configuration and you're good
* Field related naming scheme issues are tackled by Elastic via ECS (Elastic Common Schema)
* Connector pipelines make sure you can combine pipelines just as you like without having to change anything in the pipeline itself.

An example:

Imagine you have a pipeline for parsing syslog events (remove header, fix timestamp etc.). To have it easily reusable it's output configuration looks like this:

```
output {
  redis {
    host => "localhost"
    data_type => "list"
    key => "syslog-output"
  }
}
```

This seems to be rather universal and you can use it in different setups. But what if you find another pipeline online, that can process events that were already processed by the beforementioned pipeline? Say, one for dissecting `sshd` specific logs? It's Input might look like this:

```
input {
  redis {
    host => "localhost"
    data_type => "list"
    key => "sshd-input"
  }
}
```

Now you have two pipelines perfectly working together but you have no way of getting events from one into to the other. One option is to change the `key` option but that would mean you'd break upstream compatibility and can't easily pull new code via version control.

The option you get from this role is called *connector pipeline*. It's basically just this:

```
input {
  redis {
    host => "localhost"
    data_type => "list"
    key => "syslog-output"
  }
}
output {
  redis {
    host => "localhost"
    data_type => "list"
    key => "sshd-input"
  }
}
```

This pipeline will connect the two others. Given, this costs some extra ressources and makes the configuration a true nightmare to support. But it helps a lot with automatisation and if you rely on the role to manage your configuration you shouldn't have a hard time. #hugops

## Basic configuration ##

To get the connector pipeline from above, you can set the following variable:

```
logstash_connector_pipelines:
  - name: syslog-sshd
    exclusive: false
    input:
      - name: default
        key: syslog-output
    output:
      - name: default
        key: sshd-input
```

### More complex configuration ###

If you want a bit more control over which outputs are used, the role offers more sophisticated configuration.

If you have several outputs that all have conditions, like just send some messages to a development system or only alerts to a monitoring system.

```
logstash_connector_pipelines:
  - name: default
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

# default connector
  redis {
    host => "localhost"
    data_type => "list"
    key => "input"
  }

}

output {

# special connector
if [program] == "special"{
  redis {
    host => "localhost"
    data_type => "list"
    key => "myspecial"
  }
}

# special2 connector
if [program] == "special2"{
  redis {
    host => "localhost"
    data_type => "list"
    key => "myspecial2"
  }
}

# default connector
  redis {
    host => "localhost"
    data_type => "list"
    key => "forwarder"
  }

}
```

Note that the `default` connector get's **every** event, the other two output only get those where the condition is met.

You can combine several outputs with `else`. That's helpful when you want to split events. Like syslog messages depending on which program logged an event. Just change `exclusive` to `true`.

```
logstash_connector_pipelines:
  - name: default
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

# default connector
  redis {
    host => "localhost"
    data_type => "list"
    key => "input"
  }

}

output {

# special connector
if [program] == "special" {
  redis {
    host => "localhost"
    data_type => "list"
    key => "myspecial"
  }
}

# special2 connector
else if [program] == "special2" {
  redis {
    host => "localhost"
    data_type => "list"
    key => "myspecial2"
  }
}

# default connector
else  {
  redis {
    host => "localhost"
    data_type => "list"
    key => "forwarder"
  }

}

}
```

Here the `default` connector only receives the events that haven't already been sent to one of the others.

## Extra configuration ##

### Congestion threshold ###

Every Output can have a `congestion:` option with a numerical value. If the Redis key already holds more items than the value says, the output will stop.

## Caveats ##

There are still some minor issues you need to keep in mind:

* The default connector in an `exclusive: true` setup must be the last in the YAML configuration. There's no sorting, the role simple expects the default to be the last one.
* The configuration *should* work but will make no sense if you have `exclusive: true` but two or more outputs without `condition`.
