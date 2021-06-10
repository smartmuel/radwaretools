from ams import *
import requests
from bps_restpy.bps_restpy_v1.bpsRest import BPS

# class for Breaking Point
class BP(object):
    """
    Class for Breaking Point
    """

    test_id = ""

    @staticmethod
    def start(test: str, ip: str, user: str, password: str):
        bps = BPS(ip, user, password)
        # login
        bps.login()
        # showing current port reservation state
        bps.portsState()
        BP.test_id = bps.runTest(modelname=test, group=1)
        bps.logout()

    @staticmethod
    def stop(ip: str, user: str, password: str, csv: bool = False):
        try:
            bps = BPS(ip, user, password)
            # login
            bps.login()
            # stopping test
            bps.stopTest(testid=BP.test_id)
            # logging out
            if csv:
                bps.exportTestReport(BP.test_id, "Test_Report.csv", "Test_Report")
        except:
            print(getframeinfo(currentframe()).lineno, "Unexpected error:", exc_info()[0], exc_info()[1])
        finally:
            try:
                bps.logout()
            except:
                pass  # Silenced


# class for Vision API
class API(object):
    """
    Login/Logout/Get from Vision with REST API
    """
    # flag that indicate the success of the login to vision
    flag = False

    def __init__(self, vision: str, user: str, password: str):
        self.vision = vision
        url = f"https://{self.vision}/mgmt/system/user/login"
        fill_json = {"username": user, "password": password}
        response = requests.post(url, verify=False, data=None, json=fill_json)
        # self.flag = response.status_code
        self.cookie = response.cookies
        self.flag = False if "jsessionid" not in response.text else True

    def get(self, url: str):
        response = requests.get(url, verify=False, data=None, cookies=self.cookie)
        return response.json()

    def logout(self):
        url = f"https://{self.vision}/mgmt/system/user/logout"
        response = requests.post(url, verify=False, cookies=self.cookie)
        # self.flag = response.status_code

