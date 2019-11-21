# git_commit

git_commit module for Ansible

## Ansible-styled documentation

### Summary

The 'git_commit' module creates new branch by 'git checkout -b', adds files by 'git add --all', commits it and pushes changes to remote.  
Check mode is working.

#### OPTIONS (= is mandatory)

```yaml
    options:
      repo:
        description:
          - Path to local repo for working with.
      branch:
        description:
          - Name of branch for creation
      commit_msg:
        description:
          - Commit message.
      add_files:
        description:
          - Add or not untracked files.
        type: bool
        default: 'false'
      commit:
        description:
          - Commit or not changes.
        type: bool
        default: 'false'
      push:
        description:
          - Push or not changes.
        type: bool
        default: 'false'
```

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
- git_commit:
    repo: path/to-local/repo
    branch: feature/new-branch
    commit_msg: "Test commit"
    commit: true
```

#### Create or checkout existent branch

```yaml
- git_commit:
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
