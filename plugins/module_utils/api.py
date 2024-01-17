# !/usr/bin/python3

# Copyright (c) 2024, Tobias Bauriedel <tobias.bauriedel@netways.de>
# GNU General Public License v3.0+ (see LICENSES/GPL-3.0-or-later.txt or
# https://www.gnu.org/licenses/gpl-3.0.txt)

from asyncio.constants import SENDFILE_FALLBACK_READBUFFER_SIZE
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

        if auth_user == "" or auth_pass == "":
            result['stderr'] = "'basic_auth' for authentication defined but 'auth_user' or auth_pass' is empty"
            return
        self.client = new_client_basic_auth(host=host, auth_user=auth_user, auth_pass=auth_pass, verify_certs=verify_certs, ca_certs=ca_certs)

        self.handle()


    def return_result(self) -> dict:
        return self.result
  

    def handle(self):
        if self.state == 'absent':
            res = self.delete()
            if res['found'] == True:
                self.result['changed'] = True
                self.result['msg'] = self.role_name + " has been deleted."
            return

        elif self.state == 'present':
            pre_role = self.get()
            self.result['foo1'] = pre_role.raw
            res = self.put()

            if res.raw['role']['created'] == True:
                self.result['changed'] = True
                self.result['msg'] = self.role_name + " has been created."
                return

            self.result['foo2'] = self.get().raw
            if pre_role.raw != self.get().raw:
                self.result['changed'] = True
                self.result['msg'] = self.role_name + " has been updated"
                return
        
        return
        

    def get(self):
        return self.client.security.get_role(name=self.role_name)


    def put(self):                
        return self.client.security.put_role(name=self.role_name, cluster=self.cluster, indices=self.indicies)

    
    def delete(self):
        return self.client.security.delete_role(name=self.role_name)