def test_clone():
    import linux
    import os
    import time

    def callback():
        print("here")
        print(os.getpid())
        time.sleep(10)
        return 0

    pid = linux.clone(callback)
    # print(pid)
    # print(type(pid))
    # _, status = os.waitpid(pid, 0)
    status = linux.waitpid(pid)
    print('{} exited with status {}'.format(pid, status))
    return
