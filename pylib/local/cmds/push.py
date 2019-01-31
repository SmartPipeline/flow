# !usr/bin/env python
# -*- coding: UTF-8 -*-
# Author    : ZhaoChang
# Email     : zhaochang525@126.com
"""
flow push core
"""
import os
import argparse

from local.util.check import check_is_dev_branch, check_is_dirty
from local.util.git_project import GitProject
from local.util.flow_projects import FlowProjectSpec


def prepare_push_parser(parser):
    """
    Create arguments for the "push" sub-command parser

    :param argparse.ArgumentParser parser: push parser
    :return: push parser with arguments
    """
    parser.add_argument('-v', '--verbose', action='store_true', default=False, dest='verbose')
    parser.set_defaults(func=run)
    return parser


def run(args):
    # find workspace of current dir and the active projects
    project_spec = FlowProjectSpec.prompt_user_to_specify(os.getcwd(), 'push')

    # do flow push for these active projects
    for dir in project_spec.get_active_projects():
        project = GitProject(dir)
        dev_branch = project.branch_name
        if check_is_dev_branch(dir, dev_branch):
            if check_is_dirty(dir, project):
                project.rebase_master()
                project.checkout_branch('master')
                project.merge_branch(dev_branch)
                project.push_master()
                project.checkout_branch(dev_branch)
