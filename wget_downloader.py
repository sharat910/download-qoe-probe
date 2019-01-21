import time
import subprocess

class WGETDownloader(object):
    """docstring for Webpage"""
    def __init__(self, logger):
        self.logger = logger

    def download(self,url, max_time):
        command = "wget %s -O /dev/null --progress=dot:mega" % url
        self.process = subprocess.Popen(command.split(),stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        time.sleep(max_time)
        # If alive after max_time
        if self.process_alive():
            self.process.kill()
            time.sleep(1)
            assert self.process_alive() == False

    def process_alive(self):
        if self.process.poll() is None:
            return True
        else:
            return False