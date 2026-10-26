#!/usr/bin/env bash
# Checks for .github/workflows/test_cert_renewal.yml. They run on the runner and look into the
# containers of the molecule scenario elasticstack_default with docker exec.
#
#   record                  remember the certificates and the start time of Kibana
#   changed <component>...  fail if a certificate of these components is the same as recorded
#   unchanged <component>...
#   kibana_not_restarted
#   kibana_available        wait until Kibana reports the status available
#   new_events              wait until Logstash writes new events to Elasticsearch
#
# Components: ca elasticsearch kibana logstash beats
set -euo pipefail

hosts=(
  "elasticstack${ELASTIC_RELEASE}-cluster1-${MOLECULE_DISTRO}"
  "elasticstack${ELASTIC_RELEASE}-cluster2-${MOLECULE_DISTRO}"
)
# The first host is the CA host, the elastic password is stored there
ca_host="${hosts[0]}"
state_dir="${RUNNER_TEMP:-/tmp}/cert-renewal"
failed=0

# The container name is the host name, the roles use it in the file names
cert_file() {
  case "$1" in
    ca) echo "/etc/elasticsearch/certs/ca.crt" ;;
    elasticsearch) echo "/etc/elasticsearch/certs/$2.p12" ;;
    kibana) echo "/etc/kibana/certs/$2-kibana.p12" ;;
    logstash) echo "/etc/logstash/certs/$2-server.crt" ;;
    beats) echo "/etc/beats/certs/$2-beats.crt" ;;
    *) echo "unknown component $1" >&2; exit 2 ;;
  esac
}

checksum() {
  docker exec "$1" sha256sum "$(cert_file "$2" "$1")" | cut -d ' ' -f 1
}

# The certificate Elasticsearch serves. A new file alone does not show that it was restarted.
served_certificate() {
  docker exec "$1" sh -c 'openssl s_client -connect localhost:9200 </dev/null 2>/dev/null | openssl x509 -noout -fingerprint -sha256'
}

kibana_start() {
  docker exec "$1" systemctl show kibana --property ActiveEnterTimestampMonotonic --value
}

elastic_password() {
  docker exec "$ca_host" awk '/PASSWORD elastic /{print $4}' /usr/share/elasticsearch/initial_passwords
}

record() {
  rm -rf "$state_dir"
  mkdir -p "$state_dir"
  for host in "${hosts[@]}"; do
    for component in ca elasticsearch kibana logstash beats; do
      checksum "$host" "$component" > "$state_dir/$host-$component"
    done
    if ! served_certificate "$host" > "$state_dir/$host-served" 2>/dev/null; then
      echo "::error::$host: Elasticsearch does not answer on port 9200"
      exit 1
    fi
    kibana_start "$host" > "$state_dir/$host-kibana-start"
  done
}

compare() {
  local expect="$1"
  shift
  for host in "${hosts[@]}"; do
    for component in "$@"; do
      file=$(cert_file "$component" "$host")
      if ! sum=$(checksum "$host" "$component"); then
        echo "::error::$host: $file is missing"
        failed=1
        continue
      fi
      if [ "$sum" = "$(cat "$state_dir/$host-$component")" ]; then
        result=unchanged
      else
        result=changed
      fi
      if [ "$result" != "$expect" ]; then
        echo "::error::$host: $file is $result, expected $expect"
        failed=1
      else
        echo "$host: $file is $result"
      fi
      if [ "$component" = elasticsearch ] && [ "$expect" = changed ]; then
        served=$(served_certificate "$host" 2>/dev/null || true)
        if [ -z "$served" ]; then
          echo "::error::$host: Elasticsearch does not answer on port 9200"
          failed=1
        elif [ "$served" = "$(cat "$state_dir/$host-served")" ]; then
          echo "::error::$host: Elasticsearch still serves the old certificate"
          failed=1
        fi
      fi
    done
  done
}

kibana_not_restarted() {
  for host in "${hosts[@]}"; do
    if [ "$(kibana_start "$host")" != "$(cat "$state_dir/$host-kibana-start")" ]; then
      echo "::error::$host: Kibana was restarted"
      failed=1
    else
      echo "$host: Kibana was not restarted"
    fi
  done
}

kibana_available() {
  local password level
  password=$(elastic_password)
  for host in "${hosts[@]}"; do
    level=""
    for _ in $(seq 60); do
      level=$(docker exec "$host" curl -s -u "elastic:$password" "http://$host:5601/api/status" |
        jq -r '.status.overall.level' 2>/dev/null || true)
      [ "$level" = available ] && break
      sleep 5
    done
    if [ "$level" != available ]; then
      echo "::error::$host: Kibana status is '$level' after 5 minutes"
      failed=1
    else
      echo "$host: Kibana is available"
    fi
  done
}

# The default pipelines set no index, so Logstash 8 writes to the data stream logs-generic-default
# https://www.elastic.co/docs/reference/logstash/plugins/plugins-outputs-elasticsearch#plugins-outputs-elasticsearch-data_stream
event_count() {
  docker exec "$ca_host" curl -ks -u "elastic:$1" "https://localhost:9200/logs-generic-default/_count" |
    jq -r '.count'
}

# Counts from now on, so events that were written before the renewal do not count
new_events() {
  local password before now
  password=$(elastic_password)
  before=$(event_count "$password")
  for _ in $(seq 60); do
    now=$(event_count "$password")
    if [ "$now" -gt "$before" ]; then
      echo "Logstash writes events: $before before, $now now"
      return
    fi
    sleep 5
  done
  echo "::error::No new events from Logstash within 5 minutes, still $before"
  failed=1
}

case "${1:-}" in
  record) record ;;
  changed) shift; compare changed "$@" ;;
  unchanged) shift; compare unchanged "$@" ;;
  kibana_not_restarted) kibana_not_restarted ;;
  kibana_available) kibana_available ;;
  new_events) new_events ;;
  *) echo "usage: $0 record|changed|unchanged|kibana_not_restarted|kibana_available|new_events" >&2; exit 2 ;;
esac
exit "$failed"
