# !usr/bin/env python
# -*- coding: UTF-8 -*-
# Author    : ZhaoChang
# Email     : zhaochang525@126.com
"""
List all flow sub-commands and arguments
"""
import sys
import argparse
from local.cmds.push import prepare_push_parser
from local.cmds.setup import prepare_setup_parser
from local.cmds.update import prepare_update_parser


def main():
    # create the top-level parser
    parser = argparse.ArgumentParser(prog='flow')
    subparsers = parser.add_subparsers()

    # create and prepare the sub_parser for each sub-command
    prepare_setup_parser(subparsers.add_parser('setup'))
    prepare_push_parser(subparsers.add_parser('push'))
    prepare_update_parser(subparsers.add_parser('update'))

    # parse the args and call whatever function was selected
    args = parser.parse_args(sys.argv[1:])
    args.func(args)


if __name__ == '__main__':
    main()
