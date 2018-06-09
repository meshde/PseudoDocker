import ctypes
import utils

"""
Following Flags were obtained from /ur/include/linux/sched.h
"""
CSIGNAL = 0x000000ff	# signal mask to be sent at exit 
CLONE_VM = 0x00000100	# set if VM shared between processes 
CLONE_FS = 0x00000200	# set if fs info shared between processes 
CLONE_FILES = 0x00000400	# set if open files shared between processes 
CLONE_SIGHAND = 0x00000800	# set if signal handlers and blocked signals shared 
CLONE_PTRACE = 0x00002000	# set if we want to let tracing continue on the child too 
CLONE_VFORK = 0x00004000	# set if the parent wants the child to wake it up on mm_release 
CLONE_PARENT = 0x00008000	# set if we want to have the same parent as the cloner 
CLONE_THREAD = 0x00010000	# Same thread group? 
CLONE_NEWNS = 0x00020000	# New mount namespace group 
CLONE_SYSVSEM = 0x00040000	# share system V SEM_UNDO semantics 
CLONE_SETTLS = 0x00080000	# create a new TLS for the child 
CLONE_PARENT_SETTID = 0x00100000	# set the TID in the parent 
CLONE_CHILD_CLEARTID = 0x00200000	# clear the TID in the child 
CLONE_DETACHED = 0x00400000	# Unused, ignored 
CLONE_UNTRACED = 0x00800000	# set if the tracing process can't force CLONE_PTRACE on this clone 
CLONE_CHILD_SETTID = 0x01000000	# set the TID in the child 
CLONE_NEWCGROUP = 0x02000000	# New cgroup namespace 
CLONE_NEWUTS = 0x04000000	# New utsname namespace 
CLONE_NEWIPC = 0x08000000	# New ipc namespace 
CLONE_NEWUSER = 0x10000000	# New user namespace 
CLONE_NEWPID = 0x20000000	# New pid namespace 
CLONE_NEWNET = 0x40000000	# New network namespace 
CLONE_IO = 0x80000000	# Clone io context 

"""
Following flags were obtained from /usr/include/linux/fs.h
"""
MS_RDONLY = 1	# Mount read-only
MS_NOSUID = 2	# Ignore suid and sgid bits
MS_NODEV = 4	# Disallow access to device special files
MS_NOEXEC = 8	# Disallow program execution
MS_SYNCHRONOUS = 16	# Writes are synced at once
MS_REMOUNT = 32	# Alter flags of a mounted FS
MS_MANDLOCK = 64	# Allow mandatory locks on an FS
MS_DIRSYNC = 128	# Directory modifications are synchronous
MS_NOATIME = 1024	# Do not update access times.
MS_NODIRATIME = 2048	# Do not update directory access times
MS_BIND = 4096
MS_MOVE = 8192
MS_REC = 16384
MS_VERBOSE = 32768	# War is peace. Verbosity is silence.
                    # MS_VERBOSE is deprecated.
MS_SILENT = 32768
MS_POSIXACL = (1<<16)	# VFS does not apply the umask
MS_UNBINDABLE = (1<<17)	# change to unbindable
MS_PRIVATE = (1<<18)	# change to private
MS_SLAVE = (1<<19)	# change to slave
MS_SHARED = (1<<20)	# change to shared
MS_RELATIME = (1<<21)	# Update atime relative to mtime/ctime.
MS_KERNMOUNT = (1<<22)	# this is a kern_mount call
MS_I_VERSION = (1<<23)	# Update inode I_version field
MS_STRICTATIME = (1<<24)	# Always perform atime updates
MS_LAZYTIME = (1<<25)	# Update the on-disk [acm]times lazily


libc = ctypes.CDLL('libc.so.6')

def clone(callback, flags=0, args=None):
    stack = ctypes.c_char_p(" " * 8096)
    stack = ctypes.cast(stack, ctypes.c_void_p)

    # Done to prevent Fatal Erorr: Inconsistent Stringed State.
    # No clue why it happens or how the following line prevents it.
    stack = ctypes.c_void_p(stack.value + 8096)

    if args:
        CFUNC = ctypes.CFUNCTYPE(ctypes.c_int, ctypes.c_void_p)
        callback = CFUNC(callback)
        pointer = ctypes.cast(id(args), ctypes.c_void_p)
        res = libc.clone(callback, stack, flags, pointer)

    else:
        CFUNC = ctypes.CFUNCTYPE(ctypes.c_int)
        callback = CFUNC(callback)
        res = libc.clone(callback, stack, flags)

    return res

def waitpid(pid, options=0):
    status = ctypes.c_int()
    libc.waitpid(pid, ctypes.byref(status), options)
    return status

def get_object_from_pointer(pointer):
    return ctypes.cast(pointer, ctypes.py_object).value

def test():
    print('Just a test bruh!')
    __test()
    return

def __test():
    print('Private Test MOFO!!!')
    return
