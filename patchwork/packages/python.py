from fabric import api as fab
from path import path
from .. import files


def pipinstall(spec, index=None, upgrade=True, venvs=None):
    """
    Very basic pip install that will install to multiple targets
    """
    targets = venvs and venvs or './' 
    if isinstance(venvs, basestring):
        targets = [venvs]
        
    base = "pip install {0} %s"

    optional = []

    if not index is None:
        optional.extend(['-i', index])

    if upgrade is True:
        optional.append('--upgrade')

    cmd = base.format(" ".join(optional))
    for target in targets:
        with fab.prefix(". %s/bin/activate" %target):
            fab.sudo(cmd % spec)


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
    
