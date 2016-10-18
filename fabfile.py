import os
from fabric.api import local, run, env, task
from fabric.context_managers import cd, lcd
from fabric.operations import put, get
from fabric.decorators import parallel

# Change to fabfile directory, to make relative paths work
DIR_SCRIPT = os.path.dirname(os.path.realpath(__file__))
os.chdir(os.path.join(DIR_SCRIPT, ".."))

# LOGFILE = "/var/log/mirapi/mirapi.log"
DIR_REMOTE = "/server/mouseplayer"
SERVICE_NAME = "mirapi"

env.use_ssh_config = True
if not env.hosts:
    # Set default host to something
    env.hosts = ["usblooper@mirapi.local"]


@task
def hd_ro():
    """ Remount / as read-only """
    run("sudo mount -o remount,ro /")


@task
def hd_rw():
    """ Remount / as read-write """
    run("sudo mount -o remount,rw /")


@task
def reboot():
    """ Reboot the Raspberry Pi """
    run("sudo reboot")


@task
def restart():
    """ Restart the software service on the pi """
    run("sudo systemctl restart %s" % SERVICE_NAME)


@task
@parallel
def upload():
    """ Upload sources to a Raspberry """

    run("sudo rsync -avzh src %s" % DIR_REMOTE)
    # run("sudo rm -rf %s" % DIR_REMOTE)
    # run("sudo mkdir -p %s" % DIR_REMOTE)
    run("sudo chown usblooper:usblooper %s -R" % DIR_REMOTE)

    # # Upload source
    # put("src/*", DIR_REMOTE, mirror_local_mode=True)


@task
@parallel
def uploadx():
    """ Upload sources to a Raspberry """
    put("src/gpiothread.py", DIR_REMOTE, mirror_local_mode=True)


# @task
# @parallel
# def get_logs():
#     """ Download logs """
#     get(LOGFILE, "logs/%s.log" % env.host_string)
#     # print env.host_string

# @task
# @parallel
# def clear_logs():
#     """ Clear log file """
#     run("rm -f %s" % LOGFILE)
