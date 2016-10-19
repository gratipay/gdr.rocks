"""Process PyPI artifacts.

The main function is exposed as a console script named `chomp` via setup.py.

"""
from __future__ import absolute_import, division, print_function, unicode_literals

import argparse
import sys
import os
import shutil
import subprocess
from pkg_resources import parse_requirements


def unpack_zip(path, arch_name, dname):
    arch_name = arch_name.rsplit(".", 1)[0] + ".zip"
    shutil.copyfile(path, arch_name)
    cmd = "cd {0} ; unzip {1} >/dev/null 2>&1".format(dname, arch_name)
    subprocess.check_call(cmd, shell=True)
    return set(os.listdir(dname)) - set([os.path.basename(arch_name)])


def unpack_tar_gz(path, arch_name, dname):
    shutil.copyfile(path, arch_name)
    cmd = "cd {0} ; tar -zxvf {1} >/dev/null 2>&1".format(dname, arch_name)
    subprocess.check_call(cmd, shell=True)
    return set(os.listdir(dname)) - set([os.path.basename(arch_name)])


SEEN = set()

def extract():
    # do a docker dance
    # monkeypatch setup.py to hook setup
    # import setup
    # run setup.setup
    # capture relevant info passed to setup.setup
    # return it!
    pass


def possibly_extract(path):

    # make sure the cleanroom is clean
    # unpack the artifact into the cleanroom
    # check the name and version in PKG-INFO (TODO guaranteed?)
    # if already SEEN, return
    # extract the data!
    # serialize the data to SQL
    # return SQL

    print("{:>42} {}".format(path))
    arch_name = os.path.join(dname, os.path.basename(path))
    new_files = []

    if path.endswith('.zip'):
        extract_zip(path, arch_name, dname)
    elif path.endswith('.tar.gz'):
        extract_tgz(path, arch_name, dname)
    import pdb; pdb.set_trace()

    SQL = ''
    return SQL


def download_artifacts():
    try:
        run('cp status status.bak') # store in case we crash
    except IOError as e:

        run('cp status.bak status') # recover from crash
    run('rm -rf web todo')      #
    run('bandersnatch -c conf mirror')  # downloads *all* artifacts for packages which have had
                                        # any change since `status`


def extract_from_artifacts():
    SQL = ''
    for root, dirs, files in os.walk('web/packages'):
        for filename in files:
            path = os.path.join(root, filename)
            SQL += possibly_extract(path)


def update_database(SQL):
    pass


def parse_args(argv):
    p = argparse.ArgumentParser()
    p.add_argument('root', help="path to your bandersnatch root")
    return p.parse_args(argv)


def main(argv=sys.argv):
    os.chdir(parse_args(argv[1:]).root)
    download_artifacts()
    SQL = extract_from_artifacts()
    update_database(SQL)
