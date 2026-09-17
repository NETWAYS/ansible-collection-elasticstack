# Release Workflow

How to build, tag and publish a new version of this collection. Maintainers only.


## Prerequisites

* `antsibull-changelog` installed locally:

  ```bash
  pip install "antsibull-changelog==0.35.1"
  ```

* The repository or organization secret `GALAXY_API_KEY`, holding an API token of an account that owns the `netways` namespace on Ansible Galaxy. Tokens are created in the account settings on <https://galaxy.ansible.com>.
* Permission to run workflows in this repository, or the token itself if you intend to publish from your own machine. See step 7.

Galaxy versions are **immutable**. Once a version is uploaded it cannot be replaced or removed, only superseded by a higher version.

## 1. Clone into a fresh directory

`git clone` into a directory that does not exist yet, then branch off `main`:

```bash
git clone git@github.com:NETWAYS/ansible-collection-elasticstack.git release_<VERSION>
cd release_<VERSION>
git switch -c release_<VERSION>
```

Do the whole release from that clone. An everyday working copy carries untracked leftovers, and two steps below pick them up: `antsibull-changelog release` folds every file under `changelogs/fragments/` into the changelog, and `ansible-galaxy collection build` packs the working directory rather than the git tree.

## 2. Set the version

Set `version:` in **galaxy.yml** to the version you are about to release. Semantic versioning, no `v` prefix.

## 3. Write the release summary

This becomes the introductory paragraph of the release in the changelog.

`changelogs/fragments/release_summary.yml`:

```yaml
release_summary: |
  Summary text for this release, for example "Bugfix release".
```

## 4. Generate the changelog

Every pull request brings its own fragment under `changelogs/fragments/`. This folds all of them into `changelogs/changelog.yaml`, renders `CHANGELOG.md` and deletes the fragments.

```bash
antsibull-changelog lint
antsibull-changelog release --version <VERSION>
```

Steps 2 to 4 change files in the repository. `main` requires an approving review, so open a pull request with the version bump and the generated changelog. Do not push this directly, even though repository admins are technically able to.

The `changelog_fragment` check would normally reject that pull request, because a release consumes the fragments instead of adding one. It recognises a release by its shape, a folded `changelogs/changelog.yaml` together with deleted fragments and nothing else, and skips itself. Keep the release pull request to exactly those files, anything else makes the check ask for a fragment again.

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
* credit people by name where a change came from outside: the author of the pull request, and the reporter of an issue where the report was the contribution. `git shortlog -sn HEAD` lists everyone with their number of commits, folded per person through [.mailmap](.mailmap)

The release has to exist before step 7, because the archive is uploaded to it.

## 7. Publish to Ansible Galaxy

**Actions** -> **publish** -> **Run workflow**, then enter the tag.

The workflow checks out that tag, builds the collection, publishes it to Galaxy and attaches the archive to the release from step 6. It is triggered manually and never automatically, so that a tag can be inspected before an immutable version reaches Galaxy.

Afterwards confirm on <https://galaxy.ansible.com/ui/repo/published/netways/elasticstack/> that the version arrived. Publishing can print errors and still have worked.

### If you cannot run workflows

Do the same from your own machine, from a fresh clone of the tag and not from the clone of step 1, which by now carries the release branch and whatever the earlier steps left behind.

```bash
git clone --branch <VERSION> git@github.com:NETWAYS/ansible-collection-elasticstack.git publish_<VERSION>
cd publish_<VERSION>
ansible-galaxy collection build -vvv
ansible-galaxy collection publish --token <TOKEN> netways-elasticstack-<VERSION>.tar.gz
```

`-vvv` lists the files that were skipped, so you can see whether `build_ignore` did its job. Then attach the archive to the release by hand, because nothing uploaded it for you:

```bash
gh release upload <VERSION> netways-elasticstack-<VERSION>.tar.gz
```
