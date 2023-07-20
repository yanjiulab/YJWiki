#!/usr/bin/python3

"""
首先根据各个文件夹内容生成 README.md 的内容：
1. 遍历文件夹
    1. 读取 Readme 文件，生成字典，表示当前完成情况。
    2. 读取其他文件，生成新字典，
    3. 合并字典
    4. 生成新列表
    5. 生成新 Readme
2. 遍历文件夹
    1. 读取 READme 文件，根据当前完成情况，生成 sidebar
"""
import os
import os.path

dd = {
    'algorithm': '数据结构与算法',
    'c': 'C 语言',
    'db': '数据库',
    'go': 'Go 语言',
    'linux': 'Linux',
    'networking': '计算机网络',
    'python': 'Python 语言',
    'tool': '开发工具'}

with open('_sidebar.md', 'w') as ff:
    for d in os.listdir():
        if os.path.isdir(d) and not d.startswith('.') and d != 'node_modules':
            ff.write('- [%s](/%s/)\n' % (dd[d], d))
            print('- [%s](/%s/)' % (dd[d], d))
            for x in os.listdir(d):
                p = os.path.join(d, x)
                if not os.path.isdir(p) and x != 'README.md':
                    with open(p, 'r') as f:
                        title = f.readline()[2:-1]
                        if not title:
                            title = x[:-3]
                        print('  - [%s](/%s)' % (title, p))
                        ff.write('  - [%s](/%s)\n' % (title, p))
