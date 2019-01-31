# !usr/bin/env python
# -*- coding: UTF-8 -*-
# Author    : ZhaoChang
# Email     : zhaochang525@126.com
import os
import sys

from local.util.find_projects import find_enclosing_git_project, find_child_projects, get_projects_names


class FlowProjectSpec(object):

    def __init__(self, project_dir_list, active_project=None):
        """
        Keeps track of which part of a Workspace Flow should operate on.

        If active_project is None, then that means all projects.
        If active_project is a string, then only that project.

        :param list project_dir_list: list of project directories
        :param str active_project: active project name
        :return:
        """

        self.project_dir_list = project_dir_list
        self.active = active_project

    def get_active_projects(self):
        """
        Returns a list of projects directories that should be acted upon.

        :return: a list of projects directories
        :rtype: list
        """

        if self.active:
            return [self.active]
        else:
            return self.project_dir_list

    @classmethod
    def prompt_user_to_specify(cls, dir, action=None):
        """
        This method will, if needed, ask the user for clarification about the intended action

        :param str dir: the directory where the search for workspace should begin
        :param str action: an action that will operate, 'update' or 'push'
        :return:
        """
        enclosing_project = find_enclosing_git_project(dir)
        if enclosing_project is not None:
            # if we found a git project, we assume its parent is a workspace dir
            workspace_dir = os.path.dirname(enclosing_project)

            # let's test that theory
            child_projects = find_child_projects(workspace_dir)

            # prompt user to specify project which should operate on
            prompt = 'You have these git projects: {p}\nDo you want to {a} all of these projects or not? (y/n) '.format(
                    p=get_projects_names(child_projects),
                    a=action
                )
            all_projects_enter = raw_input(prompt)

            """
            if user says all, then do: return FlowProjectSpec(workspace)
            if user says only one, then do: return FlowProjectSpec(workspace, cwd)
            """
            if all_projects_enter.lower() in ['y', 'yes']:
                return FlowProjectSpec(child_projects)
            else:
                return FlowProjectSpec(child_projects, enclosing_project)
        else:
            # if not found a git project, we assume it is a workspace dir
            child_projects = find_child_projects(dir)
            if not len(child_projects):
                print 'Please run flow command in workspace directory!'
                sys.exit(1)
            return FlowProjectSpec(child_projects)
