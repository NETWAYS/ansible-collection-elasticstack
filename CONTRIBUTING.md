# Contributing

Every kind of contribution is welcome. This page describes what we need from a pull
request so that reviewing it does not take longer than writing it.

## Before you build something

There is no written scope for this collection. It gets what is useful and what helps from
an automation point of view, and that is easier to answer per case than in the abstract.
Please open an issue for anything bigger than a bug fix and we will say yes or no before
you invest the work.

For now all pull requests go against `main`.

## What a pull request needs

* **One topic per pull request.** Touching several roles is fine when it is the same
  change in each of them, for example the same fix applied to beats, logstash, kibana and
  elasticsearch. A pull request that bundles unrelated changes gets sent back.
* **A description that says precisely what changes and why.** This is required, not
  optional. A pull request whose purpose can only be reconstructed from the diff gets sent
  back.
* **Evidence that it was tested**, against the new feature or fix and against what sits
  next to it. Please say which Elastic Stack release and which ansible-core version you
  tested with.
* **New or changed variables** belong in the role's `meta/argument_specs.yml` and in its
  README table, otherwise the documentation drifts apart from the code. See "Documenting role
  variables" below.
* **Comments on anything that is not obvious.** Six months later nobody remembers what a
  clever condition was for, and then it gets analysed again from scratch.
* **A changelog fragment.** See below.
* If a change **claims something about how Elastic behaves**, please link the Elastic
  documentation for it.


## Changelog fragments

The changelog is not generated from commit messages. It is assembled from small files
that each pull request brings along, so that the description is written by the person who
knows what changed rather than reconstructed months later at release time.

Add one **new** file per pull request under `changelogs/fragments/`. Name it after the
issue or the change, for example `546_rolling_upgrade.yml`. Do not put your entry into an
existing fragment and do not rename or delete one, so that every entry stays traceable to
the pull request that introduced it. The pipeline rejects both.

```yaml
# changelogs/fragments/546_rolling_upgrade.yml
bugfixes:
  - Raising ``elasticstack_version`` no longer upgrades all Elasticsearch nodes at once
    (https://github.com/NETWAYS/ansible-collection-elasticstack/issues/546).
```

Available sections, one or more per file:

| Section | Use it for |
|---|---|
| `major_changes` | Changes that affect how the collection is used as a whole |
| `minor_changes` | New variables, new options, improved behaviour |
| `breaking_changes` | Anything users have to adapt to, for example a renamed variable |
| `deprecated_features` | Something that still works but will be removed |
| `removed_features` | Something previously deprecated that is now gone |
| `security_fixes` | Fixes with a security impact |
| `bugfixes` | Wrong or broken behaviour that now works |
| `known_issues` | Problems shipped with the release on purpose |
| `trivial` | Not rendered into the changelog. See below |

Fragments are consumed at release time: `antsibull-changelog release` folds them into the
changelog and deletes them, so the directory is empty again after every release. That is
why a new file is always the right answer, never an edit to an existing one.

### Changes that do not belong in the changelog

Some changes are not worth telling users about. They still need a fragment, but the entry
goes into the `trivial` section, which is not rendered into the changelog:

```yaml
# changelogs/fragments/fix_comment_typo.yml
trivial:
  - Fixed a typo in a comment in the elasticsearch role.
```

Typical cases for `trivial`:

* documentation wording, typos and formatting
* CI and workflow changes
* test and Molecule scenario changes
* refactoring with no visible effect on behaviour
* dependency bumps of test tooling

If you are unsure whether something is trivial, ask in the pull request. It is easier to
move an entry than to notice a missing one after the release.

## Documenting role variables

Role variables are documented from each role's `meta/argument_specs.yml`, which is the single
source of truth. When your pull request changes a role's variables:

1. Update that role's `meta/argument_specs.yml` with type, default and description.
2. Regenerate the README variable table. Please do **not** edit it by hand. The table is
   produced by [ansible-docsmith](https://github.com/foundata/ansible-docsmith), install it
   with `pip install ansible-docsmith` if you do not have it:

   ```bash
   ansible-docsmith generate roles/<role> --no-defaults --template-readme .docsmith/readme.md.j2
   ```

3. Commit the regenerated `README.md` together with your change.

The `Test Documentation` workflow checks that each README matches its `argument_specs.yml` and
fails the pull request if they drift apart.

## Documenting modules

Modules document themselves through the `DOCUMENTATION`, `EXAMPLES` and `RETURN` blocks in
their own file. That is the only place, so there is nothing to keep in sync. Check your
changes with `ansible-doc netways.elasticstack.<module>`.

Shared code under `plugins/module_utils/` has no such block, because `ansible-doc` does not
read it. Those functions are described in
[plugins/module_utils/README.md](plugins/module_utils/README.md), please keep it current when
you change them.

## Testing

Besides testing your change against a real setup, the repository has Molecule scenarios that
exercise the whole stack, and it checks for ansible-lint and yamllint errors. To run the linters
locally there is a `makefile`:

```bash
make
```

## Releasing

Maintainers only. See [RELEASE.md](RELEASE.md).
