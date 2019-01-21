from config_parser import get_config
from datetime import datetime
from flowfetch_signal import FlowFetch
from browser_downloader import ChromeDownloader, FirefoxDownloader
from wget_downloader import WGETDownloader
from logger import create_logger
import time 

def build_flowfetch_data(tag, client, url):
    return {
            'tag': tag,
            'agent': client,
            'content_provider': url.split("://")[1].split("/")[0],
            'session_id': str(datetime.now())
        }

if __name__ == "__main__":
    time.sleep(5)
    config = get_config()
    ff = FlowFetch(config['flowfetch'])
    tag = config['downloads']['tag']
    logger =  create_logger("DC",tag)
    for url in config['downloads']['urls']:
        for client in config['downloads']['clients']:
            ff.start(build_flowfetch_data(tag, client, url))
            if client == 'chrome':
                d = ChromeDownloader(config['browser'],logger)
                d.download(url,config["downloads"]["max_time"])
            elif client == 'firefox':
                d = FirefoxDownloader(config['browser'],logger)
                d.download(url,config["downloads"]["max_time"])
            elif client == 'wget':
                d = WGETDownloader(logger)
                d.download(url,config["downloads"]["max_time"])
            else:
                logger.error("Unknown client: %s" % client)
            ff.stop(True)
    

