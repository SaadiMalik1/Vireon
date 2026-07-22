# Copyright 2026 VIREON Contributors
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import subprocess
import os
from typing import Optional, List, Any


def run_sandboxed(cmd: List[str], cwd: Optional[str] = None, input_data: Optional[str] = None) -> subprocess.CompletedProcess:
    """
    Executes a command inside a lightweight sandbox using bubblewrap (bwrap) to prevent 
    unauthorized filesystem and network access by the spawned process.
    """
    bwrap_cmd = [
        "bwrap",
        "--unshare-all",          # Unshare all namespaces (network, pid, ipc, etc.)
        "--share-net",            # Allow network if needed for loopback sockets
        "--ro-bind", "/", "/",    # Read-only root filesystem
        "--proc", "/proc",        # Mount proc
        "--dev", "/dev",          # Mount dev
        "--tmpfs", "/tmp",        # Temporary /tmp
        "--bind", cwd if cwd else os.getcwd(), cwd if cwd else os.getcwd(),  # Allow writing only to CWD
    ]
    bwrap_cmd.extend(cmd)
    
    return subprocess.run(
        bwrap_cmd,
        cwd=cwd,
        input=input_data,
        capture_output=True,
        text=True
    )

def popen_sandboxed(cmd: List[str], cwd: Optional[str] = None, stdout: Any = None, stderr: Any = None) -> subprocess.Popen:

    """
    Spawns a process asynchronously inside a lightweight sandbox using bubblewrap.
    """
    bwrap_cmd = [
        "bwrap",
        "--unshare-all",
        "--share-net",            # Need network for QEMU TCP sockets
        "--ro-bind", "/", "/",
        "--proc", "/proc",
        "--dev", "/dev",
        "--tmpfs", "/tmp",
        "--bind", cwd if cwd else os.getcwd(), cwd if cwd else os.getcwd(),
    ]
    bwrap_cmd.extend(cmd)
    
    return subprocess.Popen(
        bwrap_cmd,
        cwd=cwd,
        stdout=stdout,
        stderr=stderr
    )
