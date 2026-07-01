# Ansible Role: Repos

Adds the Elastic package repositories to the target host so the other roles can
install Elastic Stack packages. It supports apt (Debian/Ubuntu), yum (RedHat) and
zypper (SUSE), for both the standard Elastic and the OSS variant.

Its main use is together with the other roles of this collection, which expect
the Elastic repositories to be present.

## Requirements

* The `community.general` collection — only needed on SUSE hosts, where the role
  uses the `zypper` modules.
* Network access from the target host to the Elastic repository URL.

The role installs the required signing tools (`gpg`/`gnupg`) itself.

## Example

```yaml
- name: Configure Elastic repositories
  hosts: all
  collections:
    - netways.elasticstack
  roles:
    - repos
```

<!-- ANSIBLE DOCSMITH MAIN START -->
## Role variables<a id="variables"></a>

No variables are defined for this role.

<!-- ANSIBLE DOCSMITH MAIN END -->

## Shared variables

This role is configured through the collection-wide `elasticstack_*` variables —
mainly `elasticstack_release`, `elasticstack_variant`, `elasticstack_enable_repos`,
`elasticstack_repo_url`, `elasticstack_repo_key` and `elasticstack_rpm_workaround`.
They are documented centrally with the
[elasticsearch role](../../docs/role-elasticsearch.md).
