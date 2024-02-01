# !/usr/bin/python3

# Copyright (c) 2024, Tobias Bauriedel <tobias.bauriedel@netways.de>
# GNU General Public License v3.0+ (see LICENSES/GPL-3.0-or-later.txt or
# https://www.gnu.org/licenses/gpl-3.0.txt)

from difflib import restore
from pickle import NONE
from xml.sax.saxutils import prepare_input_source
from elasticsearch import Elasticsearch
import ssl

def new_client_basic_auth(host, auth_user, auth_pass, ca_certs, verify_certs) -> Elasticsearch:
    ctx = ssl.create_default_context(cafile=ca_certs)
    ctx.check_hostname = False
    ctx.verify_mode = False
    return Elasticsearch(hosts=[host], basic_auth=(auth_user, auth_pass), ssl_context=ctx, verify_certs=verify_certs)


class Role():
    def __init__(self, result, role_name, cluster, indicies, state, host, auth_user, auth_pass, verify_certs, ca_certs): 
        self.role_name = role_name
        self.cluster = cluster
        self.indicies = indicies
        self.state = state
        self.result = result

        self.client = new_client_basic_auth(host=host, auth_user=auth_user, auth_pass=auth_pass, verify_certs=verify_certs, ca_certs=ca_certs)

        self.handle()


    def return_result(self) -> dict:
        return self.result
  

    def handle(self):
        all_roles = self.get_all()

        if self.state == 'absent':
            if self.role_name in all_roles:
                res = self.delete()
                if res['found'] == True:
                    self.result['changed'] = True
                    self.result['msg'] = self.role_name + " has been deleted"
                return

        elif self.state == 'present':
            if self.role_name in all_roles.raw:
                pre_role = self.get()
            else:
                pre_role = None

            res = self.put()

            if res.raw['role']['created'] == True:
                self.result['changed'] = True
                self.result['msg'] = self.role_name + " has been created"
                return

            if pre_role != None:
                if pre_role.raw != self.get().raw:
                    self.result['changed'] = True
                    self.result['msg'] = self.role_name + " has been updated"
                    return
        
        return
        

    def get_all(self):
        return self.client.security.get_role()


    def get(self):
        return self.client.security.get_role(name=self.role_name)


    def put(self):
        return self.client.security.put_role(name=self.role_name, cluster=self.cluster, indices=self.indicies)

    
    def delete(self):
        return self.client.security.delete_role(name=self.role_name)


class User():
    def __init__(self, result, user_name, full_name, password, email, roles, enabled, state, host, auth_user, auth_pass, verify_certs, ca_certs):
        self.user_name = user_name
        self.full_name = full_name
        self.password = password
        self.email = email
        self.roles = roles
        self.enabled = enabled
        self.state = state
        self.result = result

        self.client = new_client_basic_auth(host=host, auth_user=auth_user, auth_pass=auth_pass, ca_certs=ca_certs, verify_certs=verify_certs)

        self.handle()

    
    def return_result(self) -> dict:
        return self.result
    

    def handle(self):
        all_users = self.get_all()

        if self.state == 'absent':
            if self.user_name in all_users:
                res = self.delete()
                if res['found'] == True:
                    self.result['changed'] = True
                    self.result['msg'] = self.user_name + " has been deleted"
            return
        
        elif self.state == 'present':
            if self.user_name in all_users.raw:
                pre_user = self.get()
            else:
                pre_user = None

            res = self.put()

            if res.raw['created'] == True:
                self.result['changed'] = True
                self.result['msg'] = self.user_name + " has been created"
                return
            
            if pre_user != None:
                if pre_user.raw != self.get().raw:
                    self.result['changed'] = True
                    self.result['msg'] = self.user_name + " has beed updated"
                    return

        return


    def get_all(self):
        return self.client.security.get_user()


    def get(self):
        return self.client.security.get_user(username=self.user_name)

    
    def put(self):
        return self.client.security.put_user(username=self.user_name, password=self.password, email=self.email, full_name=self.full_name, enabled=self.enabled, roles=self.roles)

    
    def delete(self):
        return self.client.security.delete_user(username=self.user_name)