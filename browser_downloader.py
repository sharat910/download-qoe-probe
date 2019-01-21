import os
import time
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.common.exceptions import TimeoutException

class ChromeDownloader(object):
    """docstring for Webpage"""
    def __init__(self, config, logger):
        self.config = config
        self.logger = logger

    def download(self,url, max_time):
        self.logger.info("Downloading on chrome from %s..." % url)
        driver = self.get_driver()
        driver.get(url)
        time.sleep(max_time)
        driver.close()
        self.logger.info("Done!")

    def get_driver(self):
        if self.config['type'] == 'local':
            driver = webdriver.Chrome()
        elif self.config['type'] == 'remote':
            driver = webdriver.Remote(command_executor=self.config['chrome_remote_url'],
            desired_capabilities = DesiredCapabilities.CHROME)
        return driver

class FirefoxDownloader(object):
    def __init__(self, config, logger):
        self.config = config
        self.logger = logger

    def download(self,url, max_time):
        driver = self.get_driver()
        driver.set_page_load_timeout(max_time)
        try:
            self.logger.info("Downloading on firefox from %s..." % url)
            driver.get(url)
        except TimeoutException:
            driver.close()
            self.logger.info("Done")
        except Exception as e:
            self.logger.error(e)

    def get_driver(self):
        fp = webdriver.FirefoxProfile()
        fp.set_preference("browser.download.folderList",2)
        fp.set_preference("browser.download.manager.showWhenStarting",False)
        fp.set_preference("browser.download.dir",os.getcwd())
        fp.set_preference("browser.helperApps.neverAsk.saveToDisk","application/x-iso9660-image")
        fp.set_preference("browser.helperApps.neverAsk.saveToDisk","application/zip")
        fp.set_preference("browser.helperApps.neverAsk.saveToDisk","application/octet-stream")
        
        if self.config['type'] == 'local':
            driver = webdriver.Firefox(firefox_profile=fp)
        elif self.config['type'] == 'remote':
            driver = webdriver.Remote(
                command_executor=self.config['firefox_remote_url'],
                desired_capabilities = DesiredCapabilities.FIREFOX,
                browser_profile=fp
            )
        return driver
