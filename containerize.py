import gc
import os
from pyLinux import linux
from pyLinux.cgroups import Cgroup
from pyLinux import utils
import time
import tarfile
import traceback
import uuid

CONTAINER_DIR = 'containers/'

def isolate_resources(resources=None):
    cgroup = Cgroup('container')
    if not resources:
        resources  = [
            ('memory', 'memory.limit_in_bytes', 10000000),
        ]
    assert isinstance(resources, list)
    for resource, attribute, value in resources:
        cgroup.set(resource, attribute, value)
    return cgroup

def extract(tarf, root):
    with tarfile.open(tarf) as t:
        members  = [m for m in t.getmembers() if m.type not in
                    (tarfile.CHRTYPE, tarfile.BLKTYPE)]
        t.extractall(root, members=members)
    return

def extract2(tarf, root):
    with tarfile.open(tarf) as t:
        print('Here')
        member = t.next()
        i = 1
        while member:
            print(member.name, member.size, hex(id(member)), member.type)
            if member.type not in (tarfile.CHRTYPE, tarfile.BLKTYPE):
                try:
                    t.extract(member, root)
                    print('Extraction working')
                except OSError:
                    print('This is it mofo')
                    pass
            del member
            print('Delete')
            gc.collect()
            print('Collection')
            member = t.next()
    return

def get_container_root(files='all'):
    container_id = str(uuid.uuid4())
    container_root = os.path.join(CONTAINER_DIR, container_id)
    os.makedirs(container_root)

    print('--> Extracting Files to Root...')
    if files == 'all':
        extract('ubuntu.tar', container_root)
    else:
        extract(files, container_root)
    return container_root

def mount_files(root):
    sources = ['proc', 'sysfs', 'udev']
    targets = ['proc', 'sys', 'dev']
    fstypes = ['proc', 'sysfs', 'devtmpfs']

    destinations = [os.path.join(root, target) for target in targets]
    for destination in destinations:
        if not os.path.exists(destination):
            os.makedirs(destination)

    for i in range(3):
        linux.mount(
            sources[i], destinations[i], fstypes[i],
        )

    return

def create_filesystem():
    print('--> Creating Root...')
    root = get_container_root()
    print('--> Mounting Filesystems...')
    mount_files(root)
    return root

def chroot(root):
    print('--> Chrooting...')
    os.chroot(root)
    os.chdir('/')
    return

def isolate_filesystem():
    root = create_filesystem()
    chroot(root)
    return

def contain_clone(cmd):
    # print('Isolating Resources...')
    # isolate_resources()
    cmd = utils.get_object_from_pointer(cmd)
    cmd = cmd.split()
    print(cmd)
    print('Isolating Filesystem...')
    isolate_filesystem()
    print('Executing Command...')
    os.execv(cmd[0], cmd)
    return

def run_clone():
    COMMAND = '/bin/sh'
    print('OLO')
    pid = linux.clone(contain, stack_size=int(32768), args=COMMAND)
    print('LOLO')
    status = linux.waitpid(pid)
    print('{0} exited with status {1}'.format(pid, status))

def contain_fork(cmd):
    # isolate_namespaces()
    # isolate_resources()
    cmd = cmd.split()
    isolate_filesystem()
    os.execvp(cmd[0], cmd)
    return

def run_fork():
    CMD = '/bin/bash'
    pid = os.fork()
    if pid == 0:
        contain_fork(CMD)
    else:
        time.sleep(5)
        _, status = os.waitpid(pid, 0)
    print('{0} returned with status: {1}'.format(pid, status))

if __name__ == '__main__':
    run_fork()
