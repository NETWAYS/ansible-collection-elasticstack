# Role `repos`

This role will add the Elastic repositories to the package manager (dnf/yum. apt or zypper). It will not install packages (these can be done with the role `elasticsearch`).

## Requirements

GPG needs to be installed on the systems to verify the package signature. This will be installed as part of the role. Below you can find a list of packages that will be installed.
* Debian family: `apt-transport-https`, `gpg` and `gpg-agent`
* RedHat family: `gnupg`
* Suse family: `gpg2`

For SuSE hosts you will need the Ansible collection `community.general` on your Ansible controller.

## Variables

There are variables that are needed in more than one role of the collection. These are defined inside the "meta" role `elasticstack`. The role `elasticstack` is imported in this role.

**List of variables from `elasticsearch` used inside `repos`:**
* `elasticstack_release`: Major release version of Elastic stack to configure. (default: `7`). `7` and `8` are supported.
* `elasticstack_variant`: Variant of the stack to install. Valid values: `elastic` or `oss`. (default: `elastic`).

Please note that no `oss` versions are available for Elastic Stack later than `7`. This role will fail if you try to install them.

**Variables that are explicity defined inside `repos`:**
* `repos_enable_repos`: Enable repositories after creating them. Only works on RPM based distributions (default: `true`) 
* `repos_deb_remove_legacy_key`: Remove repository key from legacy trusted.gpg keyring (Only needed on older distributions with apt as package manager. Details can be found in [this](https://askubuntu.com/questions/1286545/what-commands-exactly-should-replace-the-deprecated-apt-key) post) (Default: `false`)

## Usage

### Upgrades

If you want to be able to update your operating system without worrying about accidentally upgrading Elastic Stack, set `repos_enable_repos` to `false`. The roles in this collection will enable the repository in case they need it. Keep in mind that this will only work on rpm based distributions.

### Example playbook

The following playbook will add the Elastic repository to the package manager.

```
  - hosts: all
    become: yes
    collections:
      - netways.elasticstack
    roles:
      - repos
```