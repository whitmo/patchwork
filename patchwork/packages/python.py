from fabric import api as fab
from path import path
from .. import files


class Pip(object):
    def __init__(self, runner=fab.run):
        self.run = runner

    def install(self, spec, index=None, upgrade=False):
        """
        Very basic pip install that will install to multiple targets
        """
        base = "pip install {0} %s"

        optional = []
        if not index is None:
            optional.extend(['-i', index])

        if upgrade:
            optional.append('--upgrade')

        cmd = base.format(" ".join(optional))
        self.run(cmd % spec)


pip = Pip()


def virtualenv(target, python=None, overwrite=True,
               url='https://raw.github.com/pypa/virtualenv/master/virtualenv.py',
               tmp='/tmp/'):
    script = path(tmp) / 'virtualenv.py'
    if not files.exists(script):
        fab.run('curl GET %s > virtualenv.py' %url)

    if not overwrite is True:
        if files.exists(target):
            return False
        
    fab.run("%s %s" %(script, target))
    return True
    
