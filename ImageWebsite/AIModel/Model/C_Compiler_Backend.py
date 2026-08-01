import subprocess
import tempfile
import os
import sys

# Conditionally import resource (it only exists on Linux/Mac)
if sys.platform != 'win32':
    import resource

def set_memory_limit():
    """Limits the subprocess to 50MB of RAM to protect the server."""
    if sys.platform != 'win32':
        megabytes = 50
        bytes_limit = megabytes * 1024 * 1024
        resource.setrlimit(resource.RLIMIT_AS, (bytes_limit, bytes_limit))

def execute_c_code(code):
    with tempfile.TemporaryDirectory() as temp_dir:
        source_path = os.path.join(temp_dir, 'main.c')
        
        # Windows expects .exe, Linux works fine with .out
        exe_extension = 'main.exe' if sys.platform == 'win32' else 'main.out'
        executable_path = os.path.join(temp_dir, exe_extension)

        with open(source_path, 'w') as f:
            f.write(code)

        # 1. Compile
        compile_process = subprocess.run(
            ['gcc', source_path, '-o', executable_path, '-lm'],
            capture_output=True, text=True
        )

        if compile_process.returncode != 0:
            return {"status": "error", "output": f"Compilation Error:\n{compile_process.stderr}"}

        # 2. Execute with strict memory and time limits
        try:
            # Prepare arguments
            run_kwargs = {
                "capture_output": True,
                "text": True,
                "timeout": 3
            }
            
            # Apply memory limits only on Linux/production
            if sys.platform != 'win32':
                run_kwargs["preexec_fn"] = set_memory_limit

            run_process = subprocess.run(
                [executable_path],
                **run_kwargs
            )
            
            if run_process.returncode == 0:
                return {"status": "success", "output": run_process.stdout}
            else:
                return {"status": "error", "output": f"Runtime Error or Memory Limit Exceeded:\n{run_process.stderr}"}
                
        except subprocess.TimeoutExpired:
            return {"status": "error", "output": "Execution timed out (exceeded 3 seconds)."}