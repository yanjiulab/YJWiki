#!/usr/bin/python3

import os
import os.path
import argparse

dd = {
    'algorithm': '数据结构与算法',
    'c': 'C 语言',
    'db': '数据库',
    'go': 'Go 语言',
    'linux': 'Linux',
    'networking': '计算机网络',
    'python': 'Python 语言',
    'tool': '开发工具'}


def autosidebar():
    with open('_sidebar.md', 'w') as ff:
        for d in os.listdir():
            if d == '_draft':
                continue
            if os.path.isdir(d) and not d.startswith('.') and d != 'node_modules':
                ff.write('- [%s](/%s/)\n' % (dd[d], d))
                print('- [%s](/%s/)' % (dd[d], d))
                for x in sorted(os.listdir(d)):
                    p = os.path.join(d, x)
                    if not os.path.isdir(p) and x != 'README.md':
                        with open(p, 'r') as f:
                            title = f.readline()[2:-1]
                            if not title:
                                title = x[:-3]
                            print('  - [%s](/%s)' % (title, p))
                            ff.write('  - [%s](/%s)\n' % (title, p))


def autogit():
    print('autogit')


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-d', '--draft', help='drafting wiki')
    parser.add_argument('-p', '--publish', help='publishing wiki')
    parser.add_argument(
        '-g', '--git', action='store_true', help='automatic git add,commit,pull,push')
    parser.add_argument(
        '-u', '--update', choices=['sb'], help='update file')
    args = parser.parse_args()

    if args.draft:
        d, f = args.draft.split('/')
        print(d, f)
        if os.path.exists(d + '/' + f + '.md'):
            os.system('mv %s/%s.md _draft/' % (d, f))
        else:
            print('file not exist in %s' % d)
        if os.path.exists(d + '/' + f + '.assets'):
            os.system('mv %s/%s.assets _draft/' % (d, f))
        else:
            print('assets not exist in %s' % d)
    elif args.publish:
        d, f = args.publish.split('/')
        # check file
        if os.path.exists('_draft/' + f + '.md'):
            os.system('mv _draft/%s.md %s/' % (f, d))
        else:
            print('file not exist in draft')
        # check assets
        if os.path.exists('_draft/' + f + '.assets'):
            os.system('mv _draft/%s.assets/ %s/' % (f, d))
        else:
            print('assets not exist in draft')
    elif args.update:
        if args.update == 'sb':
            autosidebar()
    elif args.git:
        autogit()
    else:
        parser.print_help()
