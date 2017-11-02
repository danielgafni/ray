from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import os
import sys
# Add the directory containing pyarrow to the Python path so that we find the
# pyarrow version packaged with ray and not a pre-existing pyarrow.
pyarrow_path = os.path.join(os.path.abspath(os.path.dirname(__file__)),
                            "pyarrow_files")
sys.path.insert(0, pyarrow_path)

# See https://github.com/ray-project/ray/issues/131.
helpful_message = """

If you are using Anaconda, try fixing this problem by running:

    conda install libgcc
"""

try:
    import pyarrow  # noqa: F401
except ImportError as e:
    if ((hasattr(e, "msg") and isinstance(e.msg, str) and
            ("libstdc++" in e.msg or "CXX" in e.msg))):
        # This code path should be taken with Python 3.
        e.msg += helpful_message
    elif (hasattr(e, "message") and isinstance(e.message, str) and
          ("libstdc++" in e.message or "CXX" in e.message)):
        # This code path should be taken with Python 2.
        condition = (hasattr(e, "args") and isinstance(e.args, tuple) and
                     len(e.args) == 1 and isinstance(e.args[0], str))
        if condition:
            e.args = (e.args[0] + helpful_message,)
        else:
            if not hasattr(e, "args"):
                e.args = ()
            elif not isinstance(e.args, tuple):
                e.args = (e.args,)
            e.args += (helpful_message,)
    raise

from ray.worker import (error_info, init, connect, disconnect,
                        get, put, wait, remote, log_event, log_span,
                        flush_log, get_gpu_ids, get_webui_url,
                        register_custom_serializer)  # noqa: E402
from ray.worker import (SCRIPT_MODE, WORKER_MODE, PYTHON_MODE,
                        SILENT_MODE)  # noqa: E402
from ray.worker import global_state  # noqa: E402
# We import ray.actor because some code is run in actor.py which initializes
# some functions in the worker.
import ray.actor  # noqa: F401

# Ray version string. TODO(rkn): This is also defined separately in setup.py.
# Fix this.
__version__ = "0.2.2"

__all__ = ["error_info", "init", "connect", "disconnect", "get", "put", "wait",
           "remote", "log_event", "log_span", "flush_log", "actor",
           "get_gpu_ids", "get_webui_url", "register_custom_serializer",
           "SCRIPT_MODE", "WORKER_MODE", "PYTHON_MODE", "SILENT_MODE",
           "global_state", "__version__"]

import ctypes  # noqa: E402
# Windows only
if hasattr(ctypes, "windll"):
    # Makes sure that all child processes die when we die. Also makes sure that
    # fatal crashes result in process termination rather than an error dialog
    # (the latter is annoying since we have a lot of processes). This is done
    # by associating all child processes with a "job" object that imposes this
    # behavior.
    (lambda kernel32: (lambda job: (lambda n: kernel32.SetInformationJobObject(job, 9, "\0" * 17 + chr(0x8 | 0x4 | 0x20) + "\0" * (n - 18), n))(0x90 if ctypes.sizeof(ctypes.c_void_p) > ctypes.sizeof(ctypes.c_int) else 0x70) and kernel32.AssignProcessToJobObject(job, ctypes.c_void_p(kernel32.GetCurrentProcess())))(ctypes.c_void_p(kernel32.CreateJobObjectW(None, None))) if kernel32 is not None else None)(ctypes.windll.kernel32)  # noqa: E501
