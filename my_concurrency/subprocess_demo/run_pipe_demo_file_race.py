import subprocess


import tempfile
import time

with tempfile.NamedTemporaryFile() as tf:
    print(tf.name)
    cmd = 'echo hello; sleep .5; echo jackoo; sleep .5'
    ls_process = subprocess.Popen(cmd, stdout=tf, shell=True)
    time.sleep(.1)
    tf.seek(0)
    ls_process.wait()
    print(tf.read())

    print('\n ---- read file again to confirm ---\n')
    with open(tf.name, 'r') as another_f:
        print(another_f.read())