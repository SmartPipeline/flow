# !usr/bin/env python
# -*- coding: UTF-8 -*-
# Author    : ZhaoChang
# Email     : zhaochang525@126.com
import git
import subprocess


class GitProject(object):
    """
    GitProject is a class that helps us efficiently do things around a git project

    The object is created from a string like 'D:\zhaochang\workspace\flow'
    Thereafter, you can query the following properties:
        * directory - the git project directory, like 'D:\zhaochang\workspace\flow'
        * _repository - the Repo of git project
        * branch_name - the HEAD branch name in git project
        * local_sha - the commit sha of HEAD branch ,like '5f6e4bf5926cf1885683f6777f192f031add267b'

    There are also the following useful methods:
        * is_dirty(self)
        * is_pushed(self)
        * is_merged(self)
        * rebase_master(self)
        * checkout_branch(self, branch)
        * merge_branch(self, branch)
        * push_master(self)
        * retrieve_change(self)
    """

    def __init__(self, directory):
        self.directory = directory
        self._repository = git.Repo(self.directory)
        try:
            self.branch_name = self._repository.head.ref.name
        except TypeError:
            self.branch_name = None

        # the sha key for current HEAD on the current branch
        self.local_sha = self._repository.head.commit.hexsha or None

    def is_dirty(self):
        """if nothing to be committed, return True"""

        return self._repository.is_dirty()

    def is_pushed(self):
        """if branch has been pushed, return True"""

        remote_id = subprocess.check_output("git ls-remote origin | find \'{}\'".format(self.branch_name),
                                            cwd=self.directory)
        try:
            return remote_id.split()[0] in self.local_sha
        except IndexError:
            return False

    def is_merged(self):
        """if branch has been merged into master, return True"""

        remote_id = subprocess.check_output("git ls-remote origin | find \'{}\'".format(self.branch_name),
                                            cwd=self.directory)
        master_id = subprocess.check_output("git ls-remote origin | find \'master\'", cwd=self.directory)
        try:
            return remote_id.split()[0] in master_id
        except IndexError:
            return False

    def rebase_master(self):
        """rebase master branch"""
        subprocess.check_output('git pull --rebase origin master', cwd=self.directory)

    def checkout_branch(self, branch):
        """
        checkout into a specify branch
        :param str branch: name of branch which should be checkout into
        :return:
        """

        subprocess.check_output('git checkout {}'.format(branch), cwd=self.directory)

    def merge_branch(self, branch):
        """merge a specify branch"""

        subprocess.check_output('git merge {}'.format(branch), cwd=self.directory)

    def push_master(self):
        """push master branch"""

        subprocess.check_output('git push origin master', cwd=self.directory)

    def retrieve_change(self):
        """stash changes, rebase master and stash out"""

        if self.is_dirty():
            subprocess.check_output('git stash', cwd=self.directory)
            self.rebase_master()    # TODO: if error, should raise and go on
            subprocess.check_output('git stash pop', cwd=self.directory)
        else:
            self.rebase_master()
