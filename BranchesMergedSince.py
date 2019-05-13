#!/usr/bin/env python

"""Merges since upload to itunes connect
"""

from __future__ import print_function
import os
import sys
import datetime as DateTime
import subprocess
from io import StringIO

itunesConnectDateFormat = '%b %d, %Y at %I:%M %p'
gitLogDateFormat = '%a %b %d %H:%M:%S %Y %z'

def main(arguments):
    args = sys.argv[1:]
    date_string = args[0].strip()
    timezone = DateTime.timezone(DateTime.timedelta(hours=-4))
    target_date = DateTime.datetime.strptime(date_string, itunesConnectDateFormat) #Mar 29, 2018 at 2:56 PM http://strftime.org
    target_date = target_date.replace(tzinfo=timezone)

    branch = subprocess.check_output(('/usr/bin/git', 'rev-parse', '--abbrev-ref', 'HEAD')).decode("utf-8").strip()
    target_date_git_format = target_date.strftime(gitLogDateFormat)
    gitLog = subprocess.check_output(('/usr/bin/git', 'log', '--merges', '--since=' + target_date_git_format)).decode("utf-8")

    i = 0
    git_IO = StringIO(gitLog)
    line_date = DateTime.datetime.now()

    last_date = target_date

    for (i, line) in enumerate(git_IO):
        if line.strip().startswith('Date:'):
            line_date_string = line.split('  ')[1].strip()
            line_date = DateTime.datetime.strptime(line_date_string, gitLogDateFormat) #Tue Mar 27 09:40:06 2018 -0400
            if line_date < target_date:
                break
            last_date = line_date
        elif line.strip().endswith(' to ' + branch):
            parts = line.split()
            print(parts[-3])
    print('last date', last_date)

if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
