# git_commit

git_commit module for Ansible

## Ansible-styled documentation

### Summary

The 'git_commit' module creates new branch by 'git checkout -b', adds files by 'git add --all', commits it and pushes changes to remote.  
Check mode is working.

#### OPTIONS (= is mandatory)

- add_files
        Add or not untracked files.
        [Default: false]
        type: bool

- branch
        Name of branch for creation
        [Default: (null)]

- commit
        Commit or not changes.
        [Default: false]
        type: bool

- commit_msg
        Commit message.
        [Default: (null)]

- push
        Push or not changes.
        [Default: false]
        type: bool

- repo
        Path to local repo for working with.
        [Default: (null)]

#### REQUIREMENTS:  git

#### AUTHOR: Sergei Nikitin (@cleargray)

```yaml
      METADATA:
          status:
          - preview
          supported_by: community
```

### EXAMPLES

#### Add untracked files to commit and push

```yaml
- git_commit:
    repo: path/to-local/repo
    branch: feature/new-branch
    commit_msg: "Test commit"
    add_files: true
    commit: true
    push: true
```

#### Just commit changes

```yaml
- git_config:
    repo: path/to-local/repo
    branch: feature/new-branch
    commit_msg: "Test commit"
    commit: true
```

#### Create or checkout existent branch

```yaml
- git_config:
    repo: path/to-local/repo
    branch: feature/new-branch
```

### RETURN VALUES

```yaml
pushed:
  description: Push or not changes
  returned: success
  type: bool
commited:
  description: Commit or not changes
  returned: success
  type: bool
files_added:
  description: Add or not files
  returned: success
  type: bool
branch:
  description: Branch name
  returned: success
  type: str
repo:
  description: Path to repo
  returned: success
  type: str
commit_message:
  description: Commit message
  returned: success
  type: str
```
