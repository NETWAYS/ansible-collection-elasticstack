#!/usr/bin/python

# Copyright (c) 2024, Tobias Bauriedel <tobias.bauriedel@netways.de>
# GNU General Public License v3.0+ (see LICENSES/GPL-3.0-or-later.txt or
# https://www.gnu.org/licenses/gpl-3.0.txt)

from ansible_collections.netways.elasticstack.plugins.module_utils.api import (
    Api
)

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

        self.client = Api.new_client_basic_auth(host=host, auth_user=auth_user, auth_pass=auth_pass, ca_certs=ca_certs, verify_certs=verify_certs)

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
        if self.user_name not in self.get_all().raw:
            return

        res = self.delete()
        if res['found'] == True:
            self.result['changed'] = True
            self.result['msg'] = self.user_name + " has been deleted"

        return


    def handle_present(self):
        if self.user_name in self.get_all().raw:
            pre_user = self.get()
        else:
            pre_user = None

        res = self.put()

        if res.raw['created'] == True:
            self.result['changed'] = True
            self.result['msg'] = self.user_name + " has been created"
            return

        if pre_user != None and pre_user.raw != self.get().raw:
            self.result['changed'] = True
            self.result['msg'] = self.user_name + " has beed updated"

        return


    def get_all(self):
        return self.client.security.get_user()


    def get(self):
        return self.client.security.get_user(username=self.user_name)

    
    def put(self):
        return self.client.security.put_user(username=self.user_name, password=self.password, email=self.email, full_name=self.full_name, enabled=self.enabled, roles=self.roles)

    
    def delete(self):
        return self.client.security.delete_user(username=self.user_name)