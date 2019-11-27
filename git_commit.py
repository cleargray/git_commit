#!/usr/bin/python
# -*- coding: utf-8 -*-

# (c) 2019, Sergey Nikitin <cleargray@gmail.com>
#
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function
__metaclass__ = type


ANSIBLE_METADATA = {'metadata_version': '1.1',
                    'status': ['preview'],
                    'supported_by': 'community'}


DOCUMENTATION = '''
---
module: git_commit
author:
  - Sergei Nikitin (@cleargray)
version_added: 2.8
requirements: ['git']
short_description: Creates new branch, commit and push changes to remote
description:
  - The C(git_commit) module creates new branch by 'git checkout -b',
    adds files by 'git add --all', commits it and pushes changes to remote.
    Check mode is working.
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
'''

EXAMPLES = '''
# Add untracked files to commit and push
- git_commit:
    repo: path/to-local/repo
    branch: feature/new-branch
    commit_msg: "Test commit"
    add_files: true
    commit: true
    push: true
# Just commit changes
- git_commit:
    repo: path/to-local/repo
    branch: feature/new-branch
    commit_msg: "Test commit"
    commit: true
# Create or checkout existent branch
- git_commit:
    repo: path/to-local/repo
    branch: feature/new-branch
'''

RETURN = '''
---
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
'''
from ansible.module_utils.basic import AnsibleModule
from string import Template
import os


class git_wrapper(object):
    def __init__(self, module, dir):
        self.groupObject = None
        self.projectObject = None
        self._module = module
        self.git_path = self._module.get_bin_path('git', True)
        self.dir = dir

    '''
    @param branch dir
    '''
    def branch_exists(self, branch):
        args = [self.git_path, 'branch', '--list']
        (rc, out, err) = self._module.run_command(' '.join(args), cwd=self.dir)
        if rc >= 1:
            self._module.fail_json(rc=rc, msg="Failed to check branch: %s " % err, cmd=' '.join(args))

        if branch in out:
            return True

        return False

    def checkout_branch(self, branch):
        args = [self.git_path, 'checkout']
        exists = self.branch_exists(branch)
        if exists:
            if self._module.check_mode:
                return False
            else:
                args.append(branch)
                (rc, out, err) = self._module.run_command(' '.join(args), cwd=self.dir)
                if rc >= 1:
                    self._module.fail_json(rc=rc, msg="Failed to checkout existent branch: %s " % err, cmd=' '.join(args))
                return False
        else:
            if self._module.check_mode:
                return True
            else:
                args.append('-b'+branch)

                (rc, out, err) = self._module.run_command(' '.join(args), cwd=self.dir)
                if rc >= 1:
                    self._module.fail_json(rc=rc, msg="Failed to create branch: %s " % err, cmd=' '.join(args))
                return True

    def add_files(self):
        args = [self.git_path, 'add', '--all', '-v']
        if self._module.check_mode:
            args.append('--dry-run')

        (rc, out, err) = self._module.run_command(' '.join(args), cwd=self.dir)
        if rc >= 1:
            self._module.fail_json(rc=rc, msg="Can`t add file(s): %s " % err, cmd=' '.join(args))

        if out:
            return True

        return False

    def commit_changes(self, commit_msg):
        args = [self.git_path, 'commit', '-a', '-m'+commit_msg]
        changed = False
        if self._module.check_mode:
            args.append('--dry-run')
        (rc, out, err) = self._module.run_command(' '.join(args), cwd=self.dir)
        if rc == 1 and 'nothing to commit' in out:
            changed = False
        elif rc >= 2:
            self._module.fail_json(rc=rc, msg=err, cmd=' '.join(args))
        else:
            changed = True

        return (changed, out)

    def push_changes(self, branch):
        args = [self.git_path, 'push', '--set-upstream', 'origin', branch]
        changed = False
        if self._module.check_mode:
            args.append('--dry-run')
        (rc, out, err) = self._module.run_command(' '.join(args), cwd=self.dir)
        if rc == 0 and 'Everything up-to-date' in err:
            changed = False
        elif rc >= 1:
            self._module.fail_json(rc=rc, msg="Can`t push changes: %s " % err, cmd=' '.join(args))
        else:
            changed = True

        return changed


def main():
    module = AnsibleModule(
        argument_spec=dict(
            repo=dict(type='path'),
            branch=dict(type='str'),
            add_files=dict(required=False, type='bool', default=False),
            commit=dict(required=False, type='bool', default=False),
            push=dict(required=False, type='bool', default=False),
            commit_msg=dict(required=False, type='str', default='Commit from git_commit module')
        ),
        supports_check_mode=True,
    )

    params = module.params
    # Set the locale to C to ensure consistent messages.
    module.run_command_environ_update = dict(LANG='C', LC_ALL='C', LC_MESSAGES='C', LC_CTYPE='C')

    add_files = params['add_files']
    commit_msg = params['commit_msg']
    dir = params['repo']
    raw_branch = params['branch']
    commit = params['commit']
    push = params['push']

    git = git_wrapper(module, dir)
    temp = Template(raw_branch)
    
    changed = False
    diff = ''

    branch = temp.substitute(os.environ)
    changed = git.checkout_branch(branch)

    if add_files:
        changed = git.add_files()

    if commit:
        (changed, diff) = git.commit_changes(commit_msg)

    if push:
        changed = git.push_changes(branch)

    module.exit_json(
        msg='Success',
        diff=dict(
            before_header="",
            before="\n",
            after_header="Commit changes:",
            after=(diff or "") + "\n"
        ),
        changed=changed,
        pushed=push,
        commited=commit,
        files_added=add_files,
        branch=branch,
        repo=dir,
        commit_message=commit_msg,
    )


if __name__ == '__main__':
    main()
