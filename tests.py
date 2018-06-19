def test_extract2(tmpdir):
    import os
    from containerize import extract2
    tmp = tmpdir.mkdir('tmp')
    extract2('ubuntu.tar', str(tmp))
    assert os.listdir(str(tmp)) == os.listdir(os.path.abspath('tmp'))
    return

def test_extract(tmpdir):
    import os
    from containerize import extract
    tmp = tmpdir.mkdir('tmp')
    extract('ubuntu.tar', str(tmp))
    assert os.listdir(str(tmp)) == os.listdir(os.path.abspath('tmp'))
    return

def test_get_container_root():
    from containerize import get_container_root
    root = get_container_root()
    import os
    assert os.listdir(root) == os.listdir(os.path.abspath('tmp'))

def chroot_test():
    import py
    tmpdir = py.path.local('/home/ubuntu/docker')
    try:
        tmp = tmpdir.mkdir('meshde')
    except:
        tmp = tmpdir.join('meshde')
    f = tmp.join('meshde.txt')
    f.write('Hello moto')

    from containerize import chroot
    print(str(tmp))
    # assert False
    chroot(str(tmp))
    # assert False

    import os
    assert os.getcwd() == '/'
    assert os.path.exists('/meshde.txt')
    return

def memory_limit_stress_test(byte):
    with open('/dev/urandom', 'r') as f:
        f.read(byte)
    return

def test_isolate_resources():
    from containerize import isolate_resources
    import os

    pid = os.fork()

    if pid == 0:
        memory_limit = 10000000
        resources = [
            ('memory', 'memory.limit_in_bytes', memory_limit),
        ]
        cgroup = isolate_resources()
        memory_limit_stress_test(memory_limit + 1)
        assert cgroup.assigned('memory')
        cgroup_dir = cgroup.get_cgroup_dir('memory')
        memory_limit_path = os.path.join(cgroup_dir, 'memory.limit_in_bytes')
        with open(memory_limit_path, 'r') as f:
            lines = f.readlines()
            assert isinstance(lines, list) and len(lines) == 1
            assert int(lines[0].strip()) == memory_limit

    else:
        _, status = os.waitpid(pid, 0)
        assert status == 9
