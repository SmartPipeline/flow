# !usr/bin/env python
# -*- coding: UTF-8 -*-
# Author    : ZhaoChang
# Email     : zhaochang525@126.com
"""
flow update core
"""
import os
import argparse

from local.util.check import check_is_dev_branch
from local.util.flow_projects import FlowProjectSpec
from local.util.git_project import GitProject


def prepare_update_parser(parser):
    """
    Create arguments for the "update" sub-command parser

    :param argparse.ArgumentParser parser: update parser
    :return: update parser with arguments
    """
    parser.add_argument('-v', "--verbose", action="store_true", default=False, dest="verbose")
    parser.set_defaults(func=run)
    return parser


def run(args):
    # find workspace of current dir and the active projects
    project_spec = FlowProjectSpec.prompt_user_to_specify(os.getcwd(), 'update')

    # do flow update for these active projects
    for dir in project_spec.get_active_projects():
        project = GitProject(dir)
        dev_branch = project.branch_name
        if check_is_dev_branch(dir, dev_branch):
            project.retrieve_change()
