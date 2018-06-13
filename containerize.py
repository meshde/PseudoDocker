import os
from pyLinux import linux
from pyLinux.cgroups import Cgroup
import tarfile
import uuid

CONTAINER_DIR = 'containers/'

def isolate_resources():
    cgroup = Cgroup('container')
    resources  = [
        ('cpu', 'cpu.shares', 256),
        ('memory', 'memory.limit_in_bytes', 1073741824),
    ]
    for resource, attribute, value in resources:
        cgroup.set(resource, attribute, value)
    return

def get_container_root():
    container_id = str(uuid.uuid4())
    container_root = os.path.join(CONTAINER_DIR, container_id)
    os.makedirs(container_root)

    print('--> Extracting File to Root...')
    with tarfile.open('ubuntu.tar') as t:
        members  = [m for m in t.getmembers() if m.type not in
                    (tarfile.CHRTYPE, tarfile.BLKTYPE)]
        t.extractall(container_root, members=members)
    return container_root

def mount_files(root):
    sources = ['proc', 'sysfs', 'udev']
    targets = ['proc', 'sys', 'dev']
    fstypes = ['proc', 'sysfs', 'devtmpfs']

    destinations = [os.path.join(root, target) for target in targets]
    for destination in destinations:
        os.makedirs(destination)

    for i in range(3):
        linux.mount(
            sources[i], destinations[i], fstypes[i],
        )

    return

def isolate_filesystem():
    print('--> Creating Root...')
    new_root = get_container_root()
    print('--> Mounting Filesystems...')
    mount_files(new_root)

    print('--> Chrooting...')
    os.chroot(new_root)
    os.chdir('/')
    return

def contain(cmd):
    print('Isolating Resources...')
    isolate_resources()
    print('Isolating Filesystem...')
    isolate_filesystem()
    cmd = utils.get_object_from_pointer(cmd)
    cmd = cmd.split()
    print('Executing Command...')
    os.execv(cmd[0], cmd)
    return

def run():
    COMMAND = '/bin/sh'
    pid = linux.clone(contain, args=COMMAND)
    status = linux.waitpid(pid)
    print('{0} exited with status {1}'.format(pid, status))

if __name__ == '__main__':
    run()
