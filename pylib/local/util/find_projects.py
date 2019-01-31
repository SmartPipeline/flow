# !usr/bin/env python
# -*- coding: UTF-8 -*-
# Author    : ZhaoChang
# Email     : zhaochang525@126.com
import os
import git


def find_enclosing_git_project(dir):
    """
    Returns the path to the directory at the current level or above
    If there is no such directory, it returns None

    :param str dir: starting directory for search
    :return: the directory that was found, or None
    :rtype: str|None
    """

    found = False
    while True:
        git_dir = os.path.join(dir, '.git')
        if git.repo.fun.is_git_dir(git_dir):
            found = True
            break

        dir = os.path.abspath(os.path.join(dir, '..'))
        if len(dir) < 5:  # TODO: Fix this, should be :is_root(dir)
            break

    if found:
        return dir
    else:
        return None


def find_child_projects(dir):
    """
    Returns a set of subdirectories (only one level deep) that are git projects

    :param str dir: starting directory for search
    :return: the list of directory that was found
    """

    project_dir_set = set()
    for sub_pro in os.listdir(dir):
        if os.path.isdir(os.path.join(dir, sub_pro)):
            for sub_dir in os.listdir(os.path.join(dir, sub_pro)):
                if git.repo.fun.is_git_dir(os.path.join(dir, sub_pro, sub_dir)):
                    project_dir_set.add(os.path.join(dir, sub_pro))

    return list(project_dir_set)


def get_projects_names(project_dir_set):
    """
    Returns project names list

    :param set project_dir_set: project dir set
    :return: project names list
    """
    project_name_list = []
    for dir in project_dir_set:
        project_name_list.append(os.path.split(dir)[1])
    return project_name_list
