from fabric import api as fab
from fabric.contrib import files as ffiles
from path import path
import uuid
default_mirrors = ['.*gatech.*',
                   '.*supsec.*',
                   '.*kernel.*']


def cond_mkdir(path):
    if not ffiles.exists(path):
        fab.run("mkdir %s" %path)

# revist this with aurbuild or some other helper
## def aur(url):
##     tarball = path(path(urlparse(url).path).basename())
##     fab.run('wget -O /tmp/%s %s' %(tarball, url))
##     with fab.cd('/tmp'):
##         fab.run('tar -xvzf /tmp/%s' %tarball)
##         newdir = path('/tmp') / path(tarball.namebase).namebase
##     with fab.cd(newdir):
##         out = fab.run('makepkg -s --asroot')
##         import pdb;pdb.set_trace()
    
##     fab.run("pacman -U /tmp/%s" %tarball)


def keys():
    entropy = int(fab.run('cat /proc/sys/kernel/random/entropy_avail'))
    if entropy < 200:
        # hexes = (uuid.uuid4().hex for x in range(1000))
        # cmd1 = ";".join("echo %s >> /dev/random" for x in hexes)
        # fab.run(cmd1)
        fab.run('pacman-key --populate archlinux')
        fab.run('pacman --no-confirm -S haveged')
        fab.run('rc.d start haveged')
        fab.run('pacman-key  --init')
        fab.run('pacman-key --populate archlinux')
        return fab.run("rc.d stop haveged")
    return fab.run('pacman-key  --init')


def update_mirrors(mirrors=default_mirrors,
                   url='https://www.archlinux.org/mirrorlist/all/', pacv='4.0.3'):
    """
    updates mirrors and pacman to latest version if pacv is higher
    than installed.
    """
    pmm = path('/etc/pacman.d/mirrorlist')
    fab.run('wget -O {0} {1}'.format(pmm, url))
    for mirror in default_mirrors:
        ffiles.uncomment(pmm, mirror)
    fab.run('pacman -Syy')

    with fab.settings(warn_only=True):
        # for some reason this call has returncode 2
        vinfo = fab.run('pacman -V')

    if not pacv in vinfo: # parse this better
        fab.run('pacman -S --noconfirm pacman')
        fab.run("curl https://www.archlinux.org/{developers,trustedusers}/ | awk -F\" '(/pgp.mit.edu/) {sub(/.*search=0x/,"");print $1}' | xargs pacman-key --recv-keys")
        keys()

    fab.run('pacman --noconfirm -Sf pacman-mirrorlist')
    fab.run('pacman --noconfirm -Syu')


# Edit pacman.conf and uncomment 'SigLevel = Optional TrustAll' and run 'pacman-key --init'.


