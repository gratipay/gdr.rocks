#!/usr/bin/env python
from __future__ import absolute_import, division, print_function, unicode_literals

import json
import sys
from subprocess import Popen as Process, PIPE


class ProcessError(RuntimeError):
    pass

class ResolutionError(RuntimeError):
    pass


def run(cmd):
    out, err = Process(cmd.split(), stdout=PIPE, stderr=PIPE).communicate()
    if err:
        raise ProcessError(err)
    return out


def requirements_txt(raw):
    open('requirements.txt', 'w+').write(raw)
    run("virtualenv env")
    run("env/bin/pip install -r requirements.txt")
    packages = run("env/bin/pip freeze")

    for package in packages.splitlines():
        name, version = package.split('==')
        path = 'env/lib/python2.7/site-packages/{}-{}.dist-info/METADATA'.format(name, version)
        license = 'n/a'
        for line in open(path):
            line = line.decode('utf8')
            if line.startswith('License:'):
                license = line.split()[1]
        yield {'name': name, 'version': version, 'license': license}


resolvers = {}
resolvers['requirements.txt'] = requirements_txt


def resolve(filename, content):
    if filename not in resolvers: raise Exception  # sanity check
    proc = Process(['docker', 'run', '-i', 'gdr', filename], stdin=PIPE, stdout=PIPE, stderr=PIPE)
    out, err = proc.communicate(content)
    if err:
        raise ResolutionError(err)
    return json.loads(out)


def main(argv):
    filename = argv[1]
    if filename not in resolvers:
        return 1
    content = sys.stdin.read()
    deps = tuple(resolvers[filename](content))
    json.dump(deps, sys.stdout)
    return 0


if __name__ == '__main__':
    sys.exit(main(sys.argv))
