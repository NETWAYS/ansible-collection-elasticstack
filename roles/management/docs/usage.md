# 1 Create elastic vault, create users-secretrs-vault, adapt variables

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

b) Adapt your variables: `/defauls/main.yml`

```
elasticsearch_binary_directory: "/usr/share/elasticsearch/"
elastic_username: "elastic"
elasticsearch_http_protocol: "https"
elasticsearch_host: "10.77.14.90"
elasticsearch_port: "9200"

elastic_roles_add_path: "/files/elastic-roles-add.yml"
elastic_roles_delete_path: "/files/elastic-roles-delete.yml"

elastic_users_add_path: "/files/elastic-users-add.yml"
elastic_users_delete_path: "/files/elastic-users-delete.yml"
```

c) Adapt your user-secret-vault

- I. create second vault with *all user secrets*, this is the storage of the variable of the file of:
```
elastic_users_add_path: "/files/elastic-users-add.yml"

- You can create it as such:
```
ansible-vault create management/files/users.yml
ansible-vault edit management/files/users.yml 
```
II. It should have the yaml format of `users-toystory-tesfile.yml` 
III. adapt the variable via the `defaults/main.yml`

# 2 Adapt your `elasticsearch.yml` for the role-selection

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
# 3 Run the playbook
```
ansible-playbook /home/$(id -un)/NW/ansible-nps/elasticsearch.yml -i /home/$(id -un)/NW/ansible-nps/hosts --vault-id user@prompt --vault-id elastic@prompt
```

# 4 Some Outputs stored on disk of the host controller

Currently to make it convenient to track changes the `get`-Tasks store on Disk. You essentially only need to place the `get`-Tasks where you want, to see changes, but they are overwriting previous results as of now, which is open to debate, also if everything should be separate files or one full one.


- `elasticsearch_index_info.txt`
- `elasticsearch_users_and_info.txt`
- `elasticsearch_roles_and_info.yml`

# 5 "Updating" items

A trick is to get the current state, run a deletion, then run an adding. The background is that only delete requests can delete, and only add methods can add.