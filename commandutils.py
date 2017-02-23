# -*- coding=utf-8 -*-

import subprocess


class CommandUtils:
    def __init__(self):
        pass

    @staticmethod
    def run_command(cmd_text, is_shell=True):
        sub_process = subprocess.Popen(cmd_text, shell=is_shell)
        sub_process.wait()

        return sub_process


if __name__ == '__main__':
    command = "svn co %s %s --username %s --password %s" % (
        unicode("http://10.0.100.153/svn/develop-code/BOSS界面系统/", 'utf-8'),
        unicode("E:\\product_code\\BOSS\\BOSS界面系统", 'utf-8'),
        'xuwenlong',
        'xuwenlong1'
    )
    cmd_list = ['cmd', '/c', command]
    svn_process = subprocess.Popen(cmd_list, shell=True)
    svn_process.wait()
    # os.system(command)
    print unicode('http://10.0.100.153/svn/develop-code/BOSS界面系统/', 'utf-8')
    print 'done!'
