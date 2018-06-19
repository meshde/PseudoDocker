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
