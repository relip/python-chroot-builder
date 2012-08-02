#!/usr/bin/env python
# -*- coding: utf-8 -*-

#python-chroot-builder                                                 
#Copyright (C) 2012 Ji-hoon Kim         
#
#This program is free software: you can redistribute it and/or modify
#it under the terms of the GNU General Public License as published by
#the Free Software Foundation, either version 3 of the License, or
#(at your option) any later version.
#
#This program is distributed in the hope that it will be useful,
#but WITHOUT ANY WARRANTY; without even the implied warranty of
#MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#GNU General Public License for more details.
#
#You should have received a copy of the GNU General Public License
#along with this program.  If not, see <http://www.gnu.org/licenses/>.

import sys
import ldd
import os
import glob
import shutil
import errno 

chrootTargetDir = "/chroot" 

Files = [
	'/proc',
	'/home/relip',
	'/dev',
	'/boot',
	'/root',
	'/var',
	'/sys',
	'/opt',
	'/etc/passwd',
	'/etc/passwd-',
	'/etc/shadow',
	'/etc/shadow-',
	'/etc/bashrc',
	'/etc/bash_completion.d/*',
	'/etc/group',
	'/etc/group-',
	'/etc/DIR_COLORS',
	'/etc/DIR_COLORS.256color',
	'/etc/DIR_COLORS.lightbgcolor',
	'/etc/motd',
	'/etc/profile',
	'/etc/shells',
	'/etc/inputrc',
	'/etc/termcap',
	'/etc/nsswitch.conf',
	'/etc/profile.d/colorls.sh',
	'/etc/profile.d/lang.sh',
	'/etc/profile.d/less.sh',
	'/etc/profile.d/which2.sh',
	'/etc/sysconfig/i18n',
	'/usr/share/terminfo/*/*',
	'/root/.bash_profile',
	'/root/.bashrc',
	'/usr/lib/locale/locale-archive',

	'/lib64/libnss_files.so.2', # IMPORTANT
]

Commands = [
	'/bin/cat',
	'/bin/cp',
	'/bin/mv',
	'/bin/rm',
	'/bin/bash',
	'/bin/sh',
	'/bin/nano',
	'/bin/chown',
	'/bin/chmod',
	'/bin/chgrp',
	'/bin/mkdir',
	'/bin/more',
	'/bin/touch',
	'/bin/ln',
	'/bin/ls',
	'/bin/date',
	'/bin/false',
	'/bin/true',
	'/bin/env',
	'/bin/echo',
	'/bin/find',
	'/bin/pwd',
	'/bin/vi',
	'/bin/sed',
	'/bin/su',
	'/bin/awk',
	'/bin/gawk',
	'/bin/hostname',
	'/bin/tar',
	'/bin/gzip',
	'/bin/sort',
	'/bin/sleep',
	'/bin/rmdir',
	'/bin/sleep',
	'/bin/dd',
	'/sbin/consoletype',
	'/usr/bin/less',
	'/usr/bin/passwd',
	'/usr/bin/iconv',
	'/usr/bin/base64',
	'/usr/bin/[',
	'/usr/bin/bunzip2',
	'/usr/bin/bzip2',
	'/usr/bin/clear',
	'/usr/bin/curl',
	'/usr/bin/diff',
	'/usr/bin/dir',
	'/usr/bin/dircolors',
	'/usr/bin/mesg',
	'/usr/bin/file',
	'/usr/bin/git',
	'/usr/bin/head',
	'/usr/bin/tail',
	'/usr/bin/killall',
	'/usr/bin/locale',
	'/usr/bin/tty',
	'/usr/bin/groups',
	'/usr/bin/getent',
	'/usr/bin/sqlite3',
	'/usr/bin/id',
	'/usr/bin/tail',
	'/usr/bin/unzip',
	'/usr/bin/users',
	'/usr/bin/wget',
	'/usr/bin/whoami',
	'/usr/bin/which',
	'/usr/bin/whereis',
	'/usr/bin/xargs',
	'/usr/bin/yes',
	'/usr/bin/zip',
]

#=============== DO NOT EDIT BELOW THIS LINE =======================

def mkdir_p(path):
	try:
		os.makedirs(path)
		print "Create directory: %s"%(path)
		return True
	except OSError as exc: # Python >2.5
		if exc.errno == errno.EEXIST:
			return False
		else: raise


if not mkdir_p(chrootTargetDir):
	print "Something exists"


for x in Commands:
	if not os.path.isfile(x) and not os.path.islink(x): # doesn't exists or it is directory
		print "cannot access %s: No such file or symbolic link."%(x)
		continue
	
	# Libraries.extend(f for f in ldd.ldd(x) if f not in Libraries)

	if x not in Files: Files.extend([x])
	Files.extend(f for f in ldd.ldd(x) if f not in Files)

# Checking files 

for x in Files:
	if not x.startswith('/'): x = os.path.abspath(x)

	if "*" in x: # Wildcard search 
		Files.extend(f for f in glob.glob(x) if f not in Files)
		continue

	elif os.path.exists(x) == False:
		print "cannot access '%s': No such file or directory."%(x)
		continue 


	elif os.path.isdir(x) == True:
		mkdir_p(chrootTargetDir+"/"+x)	

	else:
		t = '/'.join(x.split('/')[:-1])

		if t != "": 
			mkdir_p(chrootTargetDir+"/"+t)

		print "Copy: %s"%(chrootTargetDir+"/"+x)
		shutil.copy2(x, chrootTargetDir+"/"+x)
