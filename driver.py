import os
import time
import json
import sys
from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.firefox.firefox_profile import AddonFormatError

import types
from selenium.webdriver.chrome.remote_connection import ChromeRemoteConnection

def set_bandwidth(driver, mbps):
    driver.set_network_conditions(
        offline=False,
        latency=0,  # additional latency (ms)
        download_throughput=mbps * 1000 * 128,  # maximal throughput
        upload_throughput=mbps * 1000 * 128) 

def fix_timeout(driver):
    try:
        driver.execute_script("window.open('about:blank');")
        driver.close()
        driver.switch_to_window(driver.window_handles[0])
        return True
    except Exception as e:
        print(e)
        print("Unable to about blank!")
        return False
    

def get_browser(config):
    desired_cap = None
    if config['browser'] == 'firefox':
        desired_cap = DesiredCapabilities.FIREFOX
    elif config['browser'] == 'chrome':
        desired_cap = DesiredCapabilities.CHROME
    return desired_cap

def get_local_driver(config):
    driver = None
    if config['browser'] == 'firefox':
        driver = webdriver.Firefox()
    elif config['browser'] == 'chrome':
        driver = webdriver.Chrome()
    else:
        print("Browser type not supported!")

    return driver

def get_remote_driver(config):
    driver = None
    desired_cap = get_browser(config)
    driver = webdriver.Remote(command_executor=config['hub_url'],
    desired_capabilities=desired_cap)
    return driver

def get_driver(config):
    driver_type = config['type']
    if driver_type == 'remote':
        driver = get_remote_driver(config)
    elif driver_type == 'local':
        driver = get_local_driver(config)
    else:
        print("Incorrect driver type in configuration.")
    driver.set_window_position(0, 0)
    driver.set_window_size(config['width'],config['height'])
    driver.set_page_load_timeout(config['page_load_timeout'])
    monkey_patch_bw(driver)
    return driver

# monkey patch: add network conditions support to Remote WebDriver
def monkey_patch_bw(driver):
    driver.command_executor = ChromeRemoteConnection(driver.command_executor._url)
    driver.set_network_conditions = types.MethodType(webdriver.Chrome.set_network_conditions, driver)
    driver.get_network_conditions = types.MethodType(webdriver.Chrome.get_network_conditions, driver)
