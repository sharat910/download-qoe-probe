import requests

class FlowFetch(object):

    def __init__(self,config):
        self.config = config
        self.started = False

    def start(self, data):
        if self.config['enable']:
            r = requests.post(self.config['start_url'],json=data)
            assert r.status_code == 200
            self.started = True
        else:
            print("Flowfetch: Start request | Data:", data)

    def stop(self, success):
        if self.config['enable']:
            if self.started:
                r = requests.post(self.config['stop_url'],json={'success':success})
                assert r.status_code == 200
            else:
                print("Request to stop flowfetch before starting!")
        else:
            print("Flowfetch: Stop request | Success:", success)