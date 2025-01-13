import subprocess
import time

start_time = time.time()

# Run a long-running command
print("Starting subprocess...")
subprocess.run("echo 'hello' | sleep 1 | grep 'hello'", shell=True)
print("Subprocess finished.")

end_time = time.time()
print(f"Time taken: {end_time - start_time:.2f} seconds")