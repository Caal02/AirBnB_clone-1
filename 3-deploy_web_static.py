#!/usr/bin/python3
"""Fabric script that generates a .tgz archive from the contents of the
 web_static folder of your AirBnB Clone repo, using the function do_pack."""

from fabric.api import *
from datetime import datetime
import os

env.hosts = ['34.74.27.162', '54.224.88.154']


def do_pack():
    try:
        formato = "%Y%m%d%H%M%S"
        date_now = datetime.now()
        created_at = date_now.strftime(formato)
        local("mkdir -p versions")
        file_tgz = "versions/web_static_{}.tgz".format(created_at)
        local("tar -cvzf {} web_static".format(file_tgz))
        return file_tgz
    except:
        return None


def do_deploy(archive_path):
    if os.path.isfile(archive_path) is False:
        return False
    try:
        put(archive_path, "/tmp")
        id_file = archive_path.split("_")
        id_final = id_file[2][:-4]
        folder = "/data/web_static/releases/"
        run("mkdir -p {}web_static_{}/".format(folder, id_final))
        run("tar -xzf /tmp/web_static_{}.tgz -C {}web_static_{}/"
            .format(id_final, folder, id_final))
        run("rm /tmp/web_static_{}.tgz".format(id_final))
        run("mv {}web_static_{}/web_static/* {}web_static_{}/"
            .format(folder, id_final, folder, id_final))
        run("rm -rf {}web_static_{}/web_static".format(folder, id_final))
        run("rm -rf /data/web_static/current")
        run("ln -s {}web_static_{}/ /data/web_static/current"
            .format(folder, id_final))
        return True
    except:
        return False


def deploy():
    """
    Fabric script that creates and distributed
    an archive to your web servers, using the function deploy
    """
    archive_path = do_pack()
    if archive_path is None:
        return False
    validate = do_deploy(archive_path)
    return validate
