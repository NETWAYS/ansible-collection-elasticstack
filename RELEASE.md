# Release Workflow

How to build, tag and publish a new version of this collection.

## Prerequisites

* `antsibull-changelog` installed locally:

  ```bash
  pip install antsibull-changelog
  ```

* The repository or organization secret `GALAXY_API_KEY`, holding an API token of an
  account that owns the `netways` namespace on Ansible Galaxy. The token is created in
  the account settings on <https://galaxy.ansible.com>. The same token is used for
  `netways.icinga`, so whoever releases that collection can tell you where it lives.
* Permission to run workflows in this repository, or the token itself if you intend to
  publish from your own machine. See step 6.

Galaxy versions are **immutable**. Once a version is uploaded it cannot be replaced or
removed, only superseded by a higher version. Check the built archive before publishing.

## 1. Prepare the code

Make sure the last pull requests before the release removed as much lint as possible.
The same goes for deprecation warnings and linter exceptions.

Update the [.mailmap](.mailmap) and [AUTHORS](AUTHORS) files:

```bash
git log --use-mailmap | grep '^Author:' | cut -f2- -d' ' | sort | uniq > AUTHORS
```

## 2. Set the version

The version of this collection as seen by Ansible Galaxy comes from **galaxy.yml**, not
from the git tag. Set it to the version you are about to release. Use semantic
versioning and do not use a `v` prefix.

## 3. Write the release summary

This becomes the introductory paragraph of the release in the changelog.

`changelogs/fragments/release_summary.yml`:

```yaml
release_summary: |
  Summary text for this release, for example "Bugfix release".
```

## 4. Generate the changelog

Every pull request adds its own fragment under `changelogs/fragments/`. This step folds
all of them into `changelogs/changelog.yaml`, renders `CHANGELOG.md` and deletes the
fragments.

```bash
antsibull-changelog lint
antsibull-changelog release --version <VERSION>
```

Steps 1 to 4 change files in the repository. `main` requires an approving review, so open
a pull request with the version bump, the updated `AUTHORS` and the generated changelog.
Do not skip this and push directly, even though repository admins are technically able
to.

## 5. Tag the version

Tag the merge commit on `main`. No `v` prefix, semantic versioning.

```bash
git switch main
git pull
git tag -a <VERSION> -m "<VERSION>"
git push origin <VERSION>
```

If you cannot push tags, create the GitHub release first and let GitHub create the tag
for you. In that case do step 7 before step 6, because the workflow in step 6 needs the
tag to exist.

## 6. Publish to Ansible Galaxy

There is a workflow for this. It is triggered **manually only**, so that a tag can be
inspected before an immutable version reaches Galaxy.

**Actions** -> **publish** -> **Run workflow**, then enter the tag from step 5.

The workflow checks out that tag, builds the collection and publishes it. The version it
publishes comes from `galaxy.yml` at that tag.

If you are not allowed to run workflows in this repository, do the same from your own
machine with the token:

```bash
ansible-galaxy collection build -vvv
ansible-galaxy collection publish --token <TOKEN> netways-elasticstack-<VERSION>.tar.gz
```

`-vvv` lists the files that were skipped, so you can see whether `build_ignore` in
`galaxy.yml` did its job. Publishing may print errors and still have worked. Check
<https://galaxy.ansible.com/ui/repo/published/netways/elasticstack/> to confirm.

## 7. Create the release on GitHub

[Draft a new release](https://github.com/NETWAYS/ansible-collection-elasticstack/releases/new):

* choose the tag from step 5
* use the version as the title
* paste this version's section from `CHANGELOG.md` as the release notes
* credit contributors by name where it fits, for example behind the issue they reported

Attaching the built archive to the release is optional. It lets people install the
collection without Galaxy and without git:

```bash
ansible-galaxy collection install netways-elasticstack-<VERSION>.tar.gz
```

If you published through the workflow in step 6, no archive exists on your machine. Build
one locally if you want to attach it.
