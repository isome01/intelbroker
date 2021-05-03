from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
import asyncio
import time


class Omni:

    def __init__(self, base_url, specs, **attrs):
        try:
            self.scraper_usability = True
            self._driver_path = attrs.get('driver_path', r'C:/Program Files (x86)/chromedriver/chromedriver.exe')
            self._base_url = base_url
            self._specs = specs

            self._initialize_client()

        except Exception as e:
            print(e)
            self.scraper_usability = False
        # from here, algorithm should start
        finally:
            self._exec_ops_from_specs()

    def __del__(self):
        self._exit()

    def _initialize_client(self):
        loop = asyncio.get_event_loop()
        success = loop.run_until_complete(self._await_init_client())
        loop.close()

        return success

    def _exit(self):
        try:
            self._client.quit()
            self._client.close()

        except Exception as e:
            print(e)

    def go_to(self, url=''):
        """ Adhoc 'get' function for our scraper
        :param url:
        :return: bool
        """
        exit_success = True
        try:
            self._client.get(f'{self._base_url}{url}')
            self._busy_wait()
        except Exception as e:
            exit_success = False
            print(e)

        return exit_success

    async def _await_init_client(self):
        success = True
        try:
            options = Options()
            print('Going...')
            self._client = webdriver.Chrome(
                executable_path=self._driver_path,
                options=options
            )
        except Exception as e:
            success = False
            print(f'Error: {e}')
        finally:
            return success

    async def _busy_wait(self):
        exit_success = True
        try:
            while 1:
                state = self._client.execute_script('return document.readyState === "complete"')
                if state:
                    # print('waiting completed.')
                    break
                # print(f'still waiting; current state {state}.')
        except Exception as e:
            print(e)
            exit_success = False

        return exit_success

    def busy_wait(self):
        loop = asyncio.get_event_loop()
        success = loop.run_until_complete(self._busy_wait())
        loop.close()
        return success

    def _search_by(self):
        """
        Adhoc search by name or
        :return:
        """

    def click_on(self, elements):
        success = False
        node = None
        for e in elements:
            if success:
                break
            try:
                e.click()
                success = True
                node = e
            except Exception as e:
                print(e)

        return node

    def _exec_ops_from_specs(self):
        """
        core function for scraper
        :return: bool
        """
        if self.scraper_usability:
            print('Scraper is usable')
            self.go_to(self._base_url)
            self._fill_out_search_fields()
            self._get_links()
        else:
            print('Scraper is NOT usable')

    def _get_links(self):
        print("Getting links...")

    def _fill_out_search_fields(self):
        fields = self._specs['fields']
        
        for key in fields:
            if(fields[key] == 'input'):
                # TODO: Loop through alphabet
                self._client.find_element_by_xpath("//" + fields[key] + "[@name='" + key +"']").send_keys('a')
            else:
                # TODO: will need to loop through options eventually
                self._client.find_element_by_xpath("//" + fields[key] + "[@name='" + key +"']/option[2]").click()

        self._client.find_element_by_xpath("//input[@value='" + self._specs['buttonText'] + "']").click()
        # time.sleep(2)
