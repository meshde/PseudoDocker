import os
import tarfile
import uuid

CONTAINER_DIR = 'containers/'
def get_container_root():
    container_id = str(uuid.uuid4())
    container_root = os.path.join(CONTAINER_DIR, container_id)
    os.makedirs(container_root)

    with tarfile.open('ubuntu.tar') as t:
        members  = [m for m in t.getmembers() if m.type not in (tarfile.CHRTYPE,
                                                             tarfile.BLKTYPE)]
        t.extractall(container_root, members=members)
    return container_root

def isolate_filesystem():
    new_root = get_container_root()

def contain():
    isolate_resources()
    isolate_filesystem()
    return


if __name__ == '__main__':
    isolate_filesystem()
