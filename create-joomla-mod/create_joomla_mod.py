#!/usr/bin/python

import os
import sys
import getopt
import subprocess
from shutil import copyfile

help_string = './create_joomla_mod.py -n mod_whatever -v 0.1.0 -d "this is a' \
              ' module description"'
var_pack_org = "Stoffels_IT"
var_author = "Sarah Stoffels"


def main(argv):
    mod_name = ''
    mod_version = ''
    mod_descr = ''

    try:
        opts, args = getopt.getopt(argv, "hn:v:d:", ["mod_n=", "mod_v=",
                                                     "mod_d"])
    except getopt.GetoptError:
        print help_string
        sys.exit(2)

    for opt, arg in opts:
        if opt == '-h':
            print help_string
            sys.exit()
        elif opt in ("-n", "--mod_n"):
            mod_name = arg
        elif opt in ("-v", "--mod_v"):
            mod_version = arg
        elif opt in ("-d", "--mod_d"):
            mod_descr = arg

    if mod_name and mod_version and mod_descr:
        name_list = mod_name.split("_")
        name_list_upper = map(str.title, name_list)
        pack_name = '_'.join(name_list_upper)
        class_name = ''.join(name_list_upper) + 'Helper'

        create_files(mod_name)
        substitute_vars(mod_name, pack_name, class_name, mod_version,
                        mod_descr)

    else:
        print help_string


def create_files(mod_name):
    if not os.path.exists(mod_name):
        os.mkdir(mod_name, 0755)
    else:
        overwrite = raw_input('Directory ' + mod_name + ' exists. Do you'
                              ' want to overwrite it? (y/n)')

    if not overwrite == 'y':
        sys.exit(0)

    if not os.path.exists(mod_name + "/tmpl"):
        os.mkdir(mod_name + "/tmpl", 0755)

    copyfile('defaults/index.html',   mod_name + '/index.html')
    copyfile('defaults/index.html',   mod_name + '/tmpl/index.html')
    copyfile('defaults/default.php',  mod_name + '/tmpl/default.php')
    copyfile('defaults/helper.php',   mod_name + '/helper.php')
    copyfile('defaults/mod_name.php', mod_name + '/' + mod_name + '.php')
    copyfile('defaults/mod_name.xml', mod_name + '/' + mod_name + '.xml')


def substitute_vars(mod_name, pack_name, class_name, mod_version, mod_descr):
    subprocess.call(["sed -i -e 's/<var_name>/" + mod_name +
                     "/g' $(find " + mod_name + "/ -type f)"], shell=True)
    subprocess.call(["sed -i -e 's/<var_pack_name>/" + pack_name +
                     "/g' $(find " + mod_name + "/ -type f)"], shell=True)
    subprocess.call(["sed -i -e 's/<var_class_name>/" + class_name +
                     "/g' $(find " + mod_name + "/ -type f)"], shell=True)
    subprocess.call(["sed -i -e 's/<var_version>/" + mod_version +
                     "/g' $(find " + mod_name + "/ -type f)"], shell=True)
    subprocess.call(["sed -i -e 's/<var_descr>/" + mod_descr +
                     "/g' $(find " + mod_name + "/ -type f)"], shell=True)
    subprocess.call(["sed -i -e 's/<var_pack_org>/" + var_pack_org +
                     "/g' $(find " + mod_name + "/ -type f)"], shell=True)
    subprocess.call(["sed -i -e 's/<var_author>/" + var_author +
                     "/g' $(find " + mod_name + "/ -type f)"], shell=True)

if __name__ == "__main__":
    main(sys.argv[1:])
