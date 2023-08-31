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
- I. create second vault with *all user secrets* as such via ansible-vault.
```
ansible-vault create management/files/users.yml
ansible-vault edit management/files/users.yml 
```
II Then place all your user secrets inside in the demo format of `users-toystory-tesfile.yml` inside.
III adapt the variable via the `defaults/main.yml`

Testing-Mode: In this case deletion and installation is the *same file* for users, and another one for roles. In Production you just add different files.
Trick: One trick I thought to update roles would be to run the delete task first -> then the add task. This allows updating. (because on th API there are different Request methods for adding & deleting).

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

# 5 Info: Saving Files on Disk

I decided for some tasks like index-size, current users, current roles -> to store them on disk, as this makes creating decisions easier and provides current states without having to search through runtime logs.
