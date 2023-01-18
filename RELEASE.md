# Release Workflow

*NOTE*: This is a work in progress. While we are approaching our first release, we're collecting valuable information about tasks and put them here.

## Preparations

### WIP note

Remove the note above saying that this is a work and progress before the first release. And remove this section.

### Authors

Update the [.mailmap](.mailmap) and [AUTHORS](AUTHORS) files:

```
git log --use-mailmap | grep '^Author:' | cut -f2- -d' ' | sort | uniq > AUTHORS
```
