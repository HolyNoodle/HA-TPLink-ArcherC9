import logging
import requests
import voluptuous as vol

from homeassistant.components.device_tracker import (
    DOMAIN, PLATFORM_SCHEMA, DeviceScanner)
from homeassistant.const import (
    CONF_HOST, CONF_PASSWORD, CONF_USERNAME, HTTP_HEADER_X_REQUESTED_WITH)
import homeassistant.helpers.config_validation as cv

import re

PLATFORM_SCHEMA = PLATFORM_SCHEMA.extend({
    vol.Required(CONF_HOST): cv.string,
    vol.Required(CONF_PASSWORD): cv.string
})

api_endpoints = {
    "login": 'login?form=login',
    "getDevices": 'admin/status?form=all',
    "logout": 'admin/system?form=logout'
}

def get_scanner(hass, config):
    """Validate the configuration and return a TPLinkArcherC9 scanner."""
    scanner = TPLinkArcherC9Scanner(config[DOMAIN])

    return scanner if scanner.success_init else None


class TPLinkArcherC9Scanner(DeviceScanner):
    """This class queries a Archer C9 Access Point for connected devices."""

    def __init__(self, config):
        """Initialize the scanner."""
        self.host = config[CONF_HOST]
        self.password = config[CONF_PASSWORD]

        self.last_results = {}

        # Test the router is accessible.
        data = self.get_archer_c9_data()
        self.success_init = data is not None

    def scan_devices(self):
        """Scan for new devices and return a list with found device IDs."""
        self._update_info()
        return [client['mac'] for client in self.last_results]

    def get_device_name(self, device):
        """Return the name of the given device or None if we don't know."""
        if not self.last_results:
            return None
        for client in self.last_results:
            if client['mac'] == device:
                return client['name']
        return None

    def _update_info(self):
        """Ensure the information from the Aruba Access Point is up to date.

        Return boolean if scanning successful.
        """
        if not self.success_init:
            return False

        data = self.get_archer_c9_data()
        if not data:
            return False

        self.last_results = data.values()
        return True
    
    def getAPIUrl(self, host, token, endpoint):
        return "http://{}/cgi-bin/luci/;stok={}/{}".format(host, token, endpoint)
    
    def get_archer_c9_data(self):
        session = requests.session()
        token = ''

        devices = {}

        response = session.post(self.getAPIUrl(self.host, token, api_endpoints['login']), data={
            "operation": "login",
            "password": self.password
        }, headers={
            "Host": self.host,
            "Origin": "http://{}".format(self.host)
        })
        responseJson = response.json()

        if responseJson['success'] == True:
            token = responseJson['data']['stok']
            print(self.getAPIUrl(self.host, token, api_endpoints['getDevices']))
            response = session.get(self.getAPIUrl(self.host, token, api_endpoints['getDevices']), headers={
                "Host": self.host,
                "Origin": "http://{}".format(self.host)
            })
            responseJson = response.json()

            print(self.getAPIUrl(self.host, token, api_endpoints['logout']))
            response = session.post(self.getAPIUrl(self.host, token, api_endpoints['logout']), headers={
                "Host": self.host,
                "Origin": "http://{}".format(self.host)
            })

            [print(device) for device in responseJson['data']['access_devices_wireless_host']]
            [print(device) for device in responseJson['data']['access_devices_wired']]

            for device in responseJson['data']['access_devices_wireless_host']:
                devices[device['ipaddr']] = {
                    'ip': device['ipaddr'],
                    'mac': device['macaddr'].upper(),
                    'name': device['hostname']
                }

        return devices