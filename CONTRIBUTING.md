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
  elasticsearch. What is hard to review is a pull request that bundles unrelated changes,
  because then a problem in one part holds up all the others.
* **A description that says precisely what changes and why.** If the diff is the only
  place where the purpose can be found, the review is already too slow.
* **Evidence that it was tested**, against the new feature or fix and against what sits
  next to it. Please say which Elastic Stack release and which ansible-core version you
  tested with.
* **New or changed variables** belong in the role's `meta/argument_specs.yml` and in its
  README table, otherwise the documentation drifts apart from the code. See the
  Contributing section of the main README for how the table is generated.
* **Comments on anything that is not obvious.** Six months later nobody remembers what a
  clever condition was for, and then it gets analysed again from scratch.
* **A changelog fragment.** See below.
* If a change **claims something about how Elastic behaves**, please link the Elastic
  documentation for it.

Contributions written with the help of AI tools are welcome under the same rules. One
addition: be able to explain any line if we ask. That is the whole difference between a
vetted change and something nobody understands.

## Changelog fragments

The changelog is not generated from commit messages. It is assembled from small files
that each pull request brings along, so that the description is written by the person who
knows what changed rather than reconstructed months later at release time.

Add one file per pull request under `changelogs/fragments/`. Name it after the issue or
the change, for example `546_rolling_upgrade.yml`. Never edit an existing fragment, so
that every entry can be traced back to the pull request that introduced it.

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

The pull request pipeline fails when no fragment was added.

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

## Releasing

Maintainers only. See [RELEASE.md](RELEASE.md).
