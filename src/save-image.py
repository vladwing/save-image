#!/usr/bin/env python
# vim: tabstop=4 expandtab shiftwidth=4 softtabstop=4
from __future__ import print_function
from time import sleep
import os.path
import logging

interval = 300
MAX_RETRY_COUNT=20

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(os.path.basename(__file__))

def save_image(driver, filename):
    driver.implicitly_wait(10)
    driver.get_screenshot_as_file(filename)


def init_driver(remote_ip, width, height):
    from selenium import webdriver
    from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
    import signal
    import sys

    if remote_ip is None:
        logger.warning("You didn't specify a Selenium remote")
        remote_ip = '127.0.0.1:4444'
    url =  'http://' + remote_ip + '/wd/hub'
    logger.info("Using '"+url+"' as remote Selenium")
    driver = None
    retry_count = 0
    while not driver and retry_count < MAX_RETRY_COUNT:
        try:
            driver = webdriver.Remote(command_executor=url, desired_capabilities=DesiredCapabilities.CHROME)
        except Exception as e:
            retry_count += 1
        sleep(1)
        logger.info("Waiting for the Selenium driver to come up")
    driver.set_window_size(width, height)
    def intercept_sigint(signal, frame):
        logger.info("Ctrl+C pressed")
        driver.quit()
        sys.exit(0)
    signal.signal(signal.SIGINT, intercept_sigint)
    return driver


def arguments():
    import argparse

    parser = argparse.ArgumentParser(description="Save image using selenium driver", prog=os.path.basename(__file__))
    parser.add_argument("--driver-ip", dest="remote_ip")
    parser.add_argument("--width", dest="width", type=int, default="1280")
    parser.add_argument("--height", dest="height", type=int, default="720")
    parser.add_argument("-o", "--output", dest="filename")
    parser.add_argument("-l", "--loop", dest="loop", action='store_true', default=False)
    parser.add_argument("address")
    return parser.parse_args()


def main():
    import sys
    logger.warn(sys.argv)
    args = arguments()
    logger.warn(args)
    driver = init_driver(args.remote_ip, args.width, args.height)
    while True:
        driver.get(args.address)
        sleep(3)
        save_image(driver, args.filename)
        if not args.loop:
            break
        logger.info("Waiting " + str(interval) + "seconds ...")
        sleep(interval)
    driver.quit()

if __name__ == "__main__":
    main()
