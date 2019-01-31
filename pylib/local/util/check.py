# !usr/bin/env python
# -*- coding: UTF-8 -*-
# Author    : ZhaoChang
# Email     : zhaochang525@126.com
import sys
import os


def check_is_dev_branch(dir, branch_name):
    """
    Check if branch is dev branch and print info
    :param str dir: project directory
    :param str branch_name:
    :return:
    """

    project_name = os.path.basename(dir)
    if branch_name is None:
        print '\nYou are rebasing in {}'.format(dir)
        print 'Please fix conflicts!'
        return False

    if branch_name == 'master':
        print '[{}] Please checkout into dev branch!'.format(project_name)
        return False

    return True


def check_is_dirty(dir, project):
    """
    Check if branch is dirty and print info
    :param str dir: project directory
    :param GitProject project: project object
    :return:
    """
    project_name = os.path.basename(dir)
    if project.is_dirty():
        print '[{}] You have some changes to be committed!'.format(project_name)
        return False
    else:
        return True
