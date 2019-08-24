from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import threading
import os
import time

class geoLocator:
  def __init__(self, ip_addr):
    try:
      self.scraper_capability = True
      self.currentDatabase = {}
      self.ip_addr = ip_addr
      self.chrome_options = webdriver.ChromeOptions()
      self.chrome_options.add_argument('headless')
    except:
      self.scraper_capability = False
      print('Unable to initialize geolocator.')
    self.main()

  def usable(self):
    return self.scraper_capability

  def busyWait(self):
    pass

  def goTo(self, url = 'https://whatismyipadress.com'):
    try:
      self.wd.get(url)
      self.busyWait()
      return 0
    except:
      print('Unable to go to', url)
      return -1

  def exit(self):
    try:
      self.wd.close()
      self.wd.quit()
      return 0
    except:
      print('Unable to quit webdriver properly')
      return -1

  def main(self):
    if (self.usable()):
      self.wd = webdriver.Chrome(chrome_options=self.chrome_options)
      if (self.goTo('https://whatismyipaddress.com') is -1):
        pass
      else:
        print('Went to url...')
      return exit()
    else:
      return -1