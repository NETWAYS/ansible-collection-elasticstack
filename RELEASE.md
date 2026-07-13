# Release Workflow

*NOTE*: This is a work in progress. While we are approaching our first release, we're collecting valuable information about tasks and put them here.

## Preparations

### WIP note

Remove the note above saying that this is a work and progress before the first release. And remove this section.

### Lint

Make sure to have one last pull request to remove as much lint as possible. Same goes for deprecation warnings, linter exceptions etc.

### Authors

Update the [.mailmap](.mailmap) and [AUTHORS](AUTHORS) files:

```
git log --use-mailmap | grep '^Author:' | cut -f2- -d' ' | sort | uniq > AUTHORS
```

## Tag

Tag the version. Don't use `v` in the name. Use semantic versioning.

e.g.

```
git tag -as 7.6.4
```

## Release

Make the tag a release on GitHub.
