# 1 Create an Ansible-Vault for the Elasticsearch_Password as such:

a)
- first create a vault with new Elastic management password, to unlock the vault:
```
ansible-vault create management/vars/secret_vars.yml
ansible-vault edit management/vars/secret_vars.yml  
````
- insert inside the vault the privileged password of the `/usr/share/elasticsearch/initial_passwords`: 

```
elastic_password: "password_from_initial_elastic_password"
```


b)
- create second vault with all user secrets
```
ansible-vault create management/files/users.yml
ansible-vault edit management/files/users.yml 
```

info: find the fileformat on `users-toystory-testfile.yml`

c) 
- unlock both vaults at runtime with:
```
ansible-playbook /home/$(id -un)/NW/ansible-nps/elasticsearch.yml -i /home/$(id -un)/NW/ansible-nps/hosts --vault-id user@prompt --vault-id elastic@prompt
```


# 2 Add variables to `/defauls/main.yml`
- add Elasticsearch Host
- Add Elasticsearch Port
- Add Protocol
- Add Elasticsearch-Username

# 3 Adapt your `elasticsearch.yml` for the role-selection
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
