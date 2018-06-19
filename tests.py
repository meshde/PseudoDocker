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

def stress_test():
    with open('/dev/urandom', 'r') as f:
        f.read(150000000)
    return

def test_isolate_resources():
    from containerize import isolate_resources
    import os

    pid = os.fork()

    if pid == 0:
        cgroup = isolate_resources()
        stress_test()
        assert cgroup.assigned('memory')
        cgroup_dir = cgroup.get_cgroup_dir('memory')
        memory_limit_path = os.path.join(cgroup_dir, 'memory.limit_in_bytes')
        with open(memory_limit_path, 'r') as f:
            lines = f.readlines()
            assert isinstance(lines, list) and len(lines) == 1
            assert int(lines[0].strip()) == 100000000

    else:
        _, status = os.waitpid(pid, 0)
        assert status == 9

def test_stress_test():
    stress_test()
