import docker
import os
import tempfile
from typing import Dict, Any

class CodeSandbox:
    def __init__(self, image: str = "python:3.11-slim"):
        """Initializes the connection to your running Docker Desktop engine."""
        self.client = docker.from_env()
        self.image = image
        
        try:
            self.client.images.get(self.image)
        except docker.errors.ImageNotFound:
            print(f"Downloading isolated Python environment ({self.image})...")
            self.client.images.pull(self.image)

    def execute(self, code_string: str, timeout_seconds: int = 5) -> Dict[str, Any]:
        """
        Executes an AI's raw code string inside an isolated, secure bubble.
        Blocks networking, limits memory, and tracks errors.
        """
        with tempfile.TemporaryDirectory() as temp_dir:
            host_script_path = os.path.join(temp_dir, "script.py")
            
            with open(host_script_path, "w", encoding="utf-8") as f:
                f.write(code_string)

            container = None
            try:
                container = self.client.containers.create(
                    image=self.image,
                    command=["python", "/workspace/script.py"],
                    volumes={temp_dir: {"bind": "/workspace", "mode": "ro"}},
                    network_disabled=True,  # Keeps the AI from accessing your local network
                    mem_limit="128m",       # Thwarts memory-hog exploits
                    nano_cpus=1000000000,   # Caps usage to 1 CPU core max
                    detach=True
                )

                container.start()

                # Enforce execution timeout limits
                result = container.wait(timeout=timeout_seconds)
                exit_code = result.get("StatusCode", 0)
                logs = container.logs(stdout=True, stderr=True).decode("utf-8")

                return {
                    "success": exit_code == 0,
                    "exit_code": exit_code,
                    "output": logs,
                    "error": None if exit_code == 0 else "Runtime execution error occurred."
                }

            except Exception as e:
                if "timeout" in str(e).lower() or type(e).__name__ == "ReadTimeoutError":
                    if container:
                        try: container.kill()
                        except Exception: pass
                    return {
                        "success": False,
                        "exit_code": 124,
                        "output": "",
                        "error": f"Execution Timed Out! Exceeded maximum threshold of {timeout_seconds}s."
                    }
                return {"success": False, "exit_code": -1, "output": "", "error": str(e)}

            finally:
                if container:
                    try: container.remove(force=True)
                    except Exception: pass

# --- Verification Tests ---
if __name__ == "__main__":
    sandbox = CodeSandbox()

    print("\n--- Test 1: Executing Clean Code ---")
    res1 = sandbox.execute("print([x**2 for x in range(5)])")
    print(f"Success: {res1['success']} | Output: {res1['output'].strip()}")

    print("\n--- Test 2: AI Generates a Syntax Error ---")
    res2 = sandbox.execute("items =\nprint(items)")
    print(f"Success: {res2['success']} | System Logs Captured:\n{res2['output']}")

