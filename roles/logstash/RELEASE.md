# Release Workflow

## Preparations

### Lint

Make sure to have one last pull request to remove as much lint as possible. Same goes for deprecation warnings, linter exceptions etc.

### Authors

Update the [.mailmap](.mailmap) and [AUTHORS](AUTHORS) files:

```
git log --use-mailmap | grep '^Author:' | cut -f2- -d' ' | sort | uniq > AUTHORS
```

## Tag

Tag the version. Don't use `v` in the name. User semantic versioning.

e.g.

```
git tag -as 7.6.4
```

## Release

Make the tag a release on GitHub

## Ansible Galaxy

Do *not* push this role to Ansible Galaxy. Versioning helps with ongoing projects but we will sum up this role and all related ones in an Ansible collection and push that to GitHub.
