# -*- coding: UTF-8 -*-
import os
import sys
import shutil
import re
import getpass
import subprocess
import yaml
import xml.etree.ElementTree as ET

TEMPLATE_IDEA_PATH = 'S:/archives/code/.idea'


def get_project_list(project_str):
    """
    This will return a list of projects
    :param str project_str: project string
    :return: list of projects
    :rtype: list
    """
    project_list = []
    rex = r'^([a-zA-Z0-9_]+)(|:[-a-zA-Z0-9_])+$'
    rg = re.compile(rex)
    tokens = project_str.replace(",", " ").split(" ")
    for token in tokens:
        match = rg.match(token)
        if match:
            project_list.append(token)
        else:
            print "no match: {}".format(token)

    return project_list


class Setup(object):
    def __init__(self):
        self.workspace_name = ''
        self.workspace_dir = ''
        self.project_list = None
        self.dev_branch = ''
        self.flow_dict = {}

    def get_user_enter(self):
        """This will get user enter contents"""
        while True:
            self.workspace_name = raw_input('Enter workspace name: ')
            if not self.workspace_name:
                continue
            else:
                # check if workspace directory already exist
                self.workspace_dir = os.path.join('D:\\', getpass.getuser(), self.workspace_name)
                if os.path.exists(self.workspace_dir):
                    print '{} already exist!\n'.format(self.workspace_dir)
                    continue
                else:
                    os.makedirs(self.workspace_dir)
                    break

        while True:
            project_str = raw_input(
                'Enter the projects you would like to clone in your workspace (Enter ? for a list of projects): ')
            if not project_str:
                continue
            else:
                if project_str == '?' or project_str == '？':
                    # print list of all projects
                    all_projects = os.listdir('s:/archives/code')
                    all_projects.remove('backups')
                    print all_projects
                    print
                    continue
                else:
                    break

        self.dev_branch = self.workspace_name
        self.project_list = get_project_list(project_str)

    def clone_projects(self):
        """This will clone specify projects and checkout into dev branch"""
        wrong_project = []
        for project in self.project_list:
            # TODO: how to check if project has been cloned successfully?
            if subprocess.call('git clone file://S:\\archives\\code\\{}'.format(project), cwd=self.workspace_dir) == 0:
                subprocess.call('git checkout -b {}'.format(self.dev_branch),
                                cwd=os.path.join(self.workspace_dir, project))
            else:
                wrong_project.append(project)

        self.add_idea()
        self.record_into_yaml(list(set(self.project_list) ^ set(wrong_project)))

    def add_idea(self):
        """Copy template .idea folder into workspace.
        Rename .iml file name and change content in modules.xml, so that new workspace can use it."""

        idea_path = os.path.join(self.workspace_dir, '.idea')
        shutil.copytree(TEMPLATE_IDEA_PATH, idea_path)

        # rename 'pycharm_template.iml' into workspace name
        os.rename(os.path.join(idea_path, 'pycharm_template.iml'),
                  os.path.join(idea_path, '{}.iml'.format(self.workspace_name)))

        # change 'module' content in 'modules.xml'
        tree = ET.parse(os.path.join(idea_path, 'modules.xml'))
        root = tree.getroot()
        for child in root.iter('module'):
            child.attrib = {'fileurl': 'file://$PROJECT_DIR$/.idea/{}.iml'.format(self.workspace_name),
                            'filepath': '$PROJECT_DIR$/.idea/{}.iml'.format(self.workspace_name)}
        tree.write(os.path.join(idea_path, 'modules.xml'))

    def record_into_yaml(self, cloned_projects):
        """
        This will record cloned projects and dev branch into .flow yaml file
        If no project has been cloned, remove workspace and exit, else record.

        :param list cloned_projects: list of projects cloned successfully
        """
        if not cloned_projects:
            # remove workspace directory
            if os.path.exists(self.workspace_dir):
                shutil.rmtree(self.workspace_dir)
                sys.exit(0)
        else:
            print '\n{} have been cloned successfully!'.format(', '.join(cloned_projects))
            self.flow_dict['project_list'] = self.project_list
            self.flow_dict['dev_branch'] = self.dev_branch
            yaml_path = 'D:/{}/{}/.flow'.format(getpass.getuser(), self.workspace_name)
            with open(yaml_path, 'w') as f:
                yaml.dump(self.flow_dict, f)
            print 'Record projects and dev branch names into: {}!'.format(yaml_path)


def prepare_setup_parser(parser):
    """
    Create arguments for the "setup" sub-command parser

    :param argparse.ArgumentParser parser: setup parser
    :return: setup parser with arguments
    """
    parser.set_defaults(func=run)
    return parser


def run(args):
    setup = Setup()
    setup.get_user_enter()
    setup.clone_projects()
