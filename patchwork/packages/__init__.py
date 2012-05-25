from fabric.api import sudo
from patchwork.info import distro_family


class Package(object):
    # Try to suppress interactive prompts, assume 'yes' to all questions
    # Run from cache vs updating package lists every time; assume 'yes'.
    managers = dict(apt="DEBIAN_FRONTEND=noninteractive apt-get install -y %s",
                    yum="yum install -y %s",
                    pacman='pacman --noconfirm -S %s')
    distro_map = dict(redhat='yum',
                      arch='pacman',
                      debian='apt')

    @classmethod
    def install(cls, *packages):
        fam = distro_family()
        mngr = cls.distro_map.get(fam, None)
        assert mngr, "No manager for linux distro %s" %fam
        manager = cls.managers.get(mngr)
        for package in packages:
            sudo(manager % package)


package = Package.install

def rubygem(gem):
    """
    Install a Rubygem
    """
    return sudo("gem install -b --no-rdoc --no-ri %s" % gem)

