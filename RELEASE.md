# Release Workflow

How to build, tag and publish a new version of this collection. Maintainers only.

## What a release produces

Two different things, and it helps to keep them apart:

**The git tag** is only a name pointing at a commit. It contains nothing itself, it makes
a state of the source tree findable again. It is what `version:` resolves to when someone
installs the collection straight from git, and it is what the publish workflow checks out.

**The archive** `netways-elasticstack-<VERSION>.tar.gz` is the installable product built
from that state. `ansible-galaxy collection build` packs the collection and adds
`MANIFEST.json` and `FILES.json`, which hold the metadata from `galaxy.yml` and a checksum
for every file. This archive is what Galaxy stores and serves, and what
`ansible-galaxy collection install` unpacks. Whatever `build_ignore` in `galaxy.yml` lists
is left out of it.

The version comes from `galaxy.yml`, not from the tag. Both have to say the same thing.

## Prerequisites

* `antsibull-changelog` installed locally:

  ```bash
  pip install antsibull-changelog
  ```

* The repository or organization secret `GALAXY_API_KEY`, holding an API token of an
  account that owns the `netways` namespace on Ansible Galaxy. Tokens are created in the
  account settings on <https://galaxy.ansible.com>.
* Permission to run workflows in this repository, or the token itself if you intend to
  publish from your own machine. See step 6.

Galaxy versions are **immutable**. Once a version is uploaded it cannot be replaced or
removed, only superseded by a higher version.

## 1. Prepare the code

Make sure the last pull requests before the release removed as much lint as possible. The
same goes for deprecation warnings and linter exceptions.

Update the [AUTHORS](AUTHORS) file. It is generated from the git history and lists
everyone who contributed. `--use-mailmap` folds the alternative addresses in
[.mailmap](.mailmap) into one entry per person, so add a line there first if someone shows
up twice:

```bash
git log --use-mailmap | grep '^Author:' | cut -f2- -d' ' | sort | uniq > AUTHORS
```

## 2. Set the version

Set `version:` in **galaxy.yml** to the version you are about to release. Semantic
versioning, no `v` prefix.

## 3. Write the release summary

This becomes the introductory paragraph of the release in the changelog.

`changelogs/fragments/release_summary.yml`:

```yaml
release_summary: |
  Summary text for this release, for example "Bugfix release".
```

## 4. Generate the changelog

Every pull request brings its own fragment under `changelogs/fragments/`. This folds all
of them into `changelogs/changelog.yaml`, renders `CHANGELOG.md` and deletes the
fragments.

```bash
antsibull-changelog lint
antsibull-changelog release --version <VERSION>
```

Steps 1 to 4 change files in the repository. `main` requires an approving review, so open
a pull request with the version bump, the updated `AUTHORS` and the generated changelog.
Do not push this directly, even though repository admins are technically able to.

## 5. Tag the version

Tag the merge commit on `main`. No `v` prefix, semantic versioning.

```bash
git switch main
git pull
git tag -a <VERSION> -m "<VERSION>"
git push origin <VERSION>
```

If you cannot push tags, skip this and let GitHub create the tag in step 6 instead.

## 6. Create the release on GitHub

[Draft a new release](https://github.com/NETWAYS/ansible-collection-elasticstack/releases/new):

* choose the tag from step 5, or enter the version and let GitHub create the tag now
* use the version as the title
* paste this version's section from `CHANGELOG.md` as the release notes
* credit people by name where a change came from outside: the author of the pull request,
  and the reporter of an issue where the report was the contribution

The release has to exist before step 7, because the archive is uploaded to it.

## 7. Publish to Ansible Galaxy

**Actions** -> **publish** -> **Run workflow**, then enter the tag.

The workflow checks out that tag, builds the collection, publishes it to Galaxy and
attaches the archive to the release from step 6. It is triggered manually and never
automatically, so that a tag can be inspected before an immutable version reaches Galaxy.

Afterwards confirm on
<https://galaxy.ansible.com/ui/repo/published/netways/elasticstack/> that the version
arrived. Publishing can print errors and still have worked.

### If you cannot run workflows

Do the same from your own machine. **Clone the tag into a fresh directory first.**
`ansible-galaxy collection build` packs the working directory and not the git tree, so
untracked local files end up in the archive unless `build_ignore` happens to cover them.

```bash
git clone --branch <VERSION> git@github.com:NETWAYS/ansible-collection-elasticstack.git release_<VERSION>
cd release_<VERSION>
ansible-galaxy collection build -vvv
ansible-galaxy collection publish --token <TOKEN> netways-elasticstack-<VERSION>.tar.gz
```

`-vvv` lists the files that were skipped, so you can see whether `build_ignore` did its
job. Then attach the archive to the release by hand, because nothing uploaded it for you:

```bash
gh release upload <VERSION> netways-elasticstack-<VERSION>.tar.gz
```
