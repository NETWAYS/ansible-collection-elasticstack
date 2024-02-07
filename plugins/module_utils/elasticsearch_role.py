#!/usr/bin/python

# Copyright (c) 2024, Tobias Bauriedel <tobias.bauriedel@netways.de>
# GNU General Public License v3.0+ (see LICENSES/GPL-3.0-or-later.txt or
# https://www.gnu.org/licenses/gpl-3.0.txt)

from ansible_collections.netways.elasticstack.plugins.module_utils.api import (
    Api
)

class Role():
    def __init__(self, result, role_name, cluster, indicies, state, host, auth_user, auth_pass, verify_certs, ca_certs): 
        self.role_name = role_name
        self.cluster = cluster
        self.indicies = indicies
        self.state = state
        self.result = result

        self.client = Api.new_client_basic_auth(host=host, auth_user=auth_user, auth_pass=auth_pass, verify_certs=verify_certs, ca_certs=ca_certs)

        self.handle()


    def return_result(self) -> dict:
        return self.result
  

    def handle(self):

        if self.state == 'absent':
           self.handle_absent()
        elif self.state == 'present':
            self.handle_present()
        
        return


    def handle_absent(self):
        if self.role_name not in self.get_all().raw:
            return
        
        res = self.delete()
        if res['found'] == True:
            self.result['changed'] = True
            self.result['msg'] = self.role_name + " has been deleted"
        
        return


    def handle_present(self):
        if self.role_name in self.get_all().raw:
            pre_role = self.get()
        else:
            pre_role = None

        res = self.put()

        if res.raw['role']['created'] == True:
            self.result['changed'] = True
            self.result['msg'] = self.role_name + " has been created"
            return

        if pre_role == None:
            return

        if pre_role.raw != self.get().raw:
            self.result['changed'] = True
            self.result['msg'] = self.role_name + " has been updated"

        return
        

    def get_all(self):
        return self.client.security.get_role()


    def get(self):
        return self.client.security.get_role(name=self.role_name)


    def put(self):
        return self.client.security.put_role(name=self.role_name, cluster=self.cluster, indices=self.indicies)

    
    def delete(self):
        return self.client.security.delete_role(name=self.role_name)
