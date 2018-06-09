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

def test_clone_args():
    import linux
    import ctypes

    def callback(val):
        # phrase = ctypes.c_char_p.from_buffer(val)
        print('Hello')
        print(val)
        valu = ctypes.cast(val, ctypes.py_object)
        print('Value is:', valu.value)
        print('Types is:', type(valu))
        return 0

    pid = linux.clone(callback, args=['Mehmood'])
    status = linux.waitpid(pid)
    print('{} exited with status {}'.format(pid, status))
    return
