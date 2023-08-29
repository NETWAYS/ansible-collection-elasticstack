# 1 Create Ansible-Vault as such

```
ansible-vault create management/vars/secret_vars.yml
ansible-vault edit management/vars/secret_vars.yml  
````

# 2 Add variables to '/defauls/main.yml' 
- add Elasticsearch Host
- Add Elasticsearch Port
- Add Protocol
- Add Username
- User-Passwort unlocks via Vault


# 3 Adapt your elasticsearch.yml for the role-selection

```
---
- hosts: els
  # remote_user:
  become: true
  collections:
    - netways.elasticstack
  vars:
    elastic_variant: elastic #oss
    elasticsearch_jna_workaround: true
    elastic_override_beats_tls: true
    #  elastic_release: 8 #7
    # pre_tasks:
    #   - name: Install Rsyslog
    #     package:
    #       name: rsyslog
    #   - name: Start rsyslog
    #     service:
    #       name: rsyslog
    #       state: started
    #       enabled: true
  roles:
               - management
    #          - repos
    #          - elasticsearch
    #          - geerlingguy.redis
    #          - logstash
    #          - kibana
    #          - beats

```
# 4 Run the Playbook

```
ansible-playbook /home/px/NW/ansible-nps/elasticsearch.yml -i /home/px/NW/ansible-nps/hosts --ask-vault-pass

```
