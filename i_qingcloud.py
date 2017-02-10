#!/usr/bin/python
import sys
import getopt
import traceback

import base64
import hmac
import urllib
from hashlib import sha256
import httplib


class ArgsException(Exception):
    pass


class ConfigException(Exception):
    pass


class Command(object):
    def __init__(self, args):
        self.configFile = None
        self.printUsage = False
        self.unknownArgs = []

        # auth config
        self.qy_access_key_id = None
        self.qy_secret_access_key = None
        self.zone = None

    def _auth_config_parse(self, filepath):
        with open(filepath) as f:
            for line in f:
                if 'qy_access_key_id' in line:
                    self.qy_access_key_id = line.split()[-1]
                    continue
                elif 'qy_secret_access_key' in line:
                    self.qy_secret_access_key = line.split()[-1]
                    continue
                elif 'zone' in line:
                    self.zone = line.split()[-1]
                    continue
                else:
                    raise ConfigException()

    def __make_url(self, properties):
        return urllib.urlencode(properties)

    def __get_signature(self, string_to_sign):
        h = hmac.new(self.qy_secret_access_key, digestmod=sha256)
        h.update(string_to_sign)
        sign = base64.b64encode(h.digest()).strip()
        signature = urllib.quote_plus(sign)
        return signature

    def __print_properties_util(self, properties):
        for k, v in properties.items():
            print k, v

    def _send_request(self, properties):
        url = self.__make_url(properties)
        string_to_sign = 'GET\n/iaas/\n' + url
        signature = self.__get_signature(string_to_sign)

        properties['signature'] = signature

        self.__print_properties_util(properties)
        url = self.__make_url(properties)
        print 'url = {0}'.format(url)
        headers = {"Content-type": "application/x-www-form-urlencoded",
                   "Accept": "text/plain"}

        conn = httplib.HTTPConnection('api.qingcloud.com')
        conn.request('get', '/iaas', url, headers)
        response = conn.getresponse()
        print response.status
        print response.reason
        print response.read()


class RunInstance(Command):
    def __init__(self, args):
        Command.__init__(self, args)

        # run_instance args
        self.action = 'RunInstances'
        self.signature_method = 'HmacSHA256'
        self.signature_version = 1
        self.version = 1

        self.userPropertyList = [
            'image_id=',
            "instance_type=",
            "instance_name="
        ]
        self.userPropertiesDict = {}

        try:
            self._parse_options(args)
            if self.configFile is not None:
                self._auth_config_parse(self.configFile)
            else:
                raise ConfigException('Should specify config file by -f option.')
        except ConfigException as e:
            print e.message
        except Exception as e:
            print e.message
            print traceback.format_exc()

    def _runInstanceUsage(self):
        print """
usage: qingcloud iaas run-instances --image_id <image_id> --instance_type \
<instance_type> [options] [-f <conf_file>]

        """
    def _parse_options(self,args):
        options, args = getopt.getopt(args, "hf:m:t:N:", self.userPropertyList)

        for o, val in options:
            if o in ('-f'):
                self.configFile = val
            elif o in ("-h"):
                self.printUsage = True
            elif o in ('-m', '--image_id'):
                self.userPropertiesDict['image_id'] = val
            elif o in ('-t', '--instance_type'):
                self.userPropertiesDict['instance_type'] = val
            elif o in ('-N', '--instance_name'):
                self.userPropertiesDict['instance_name'] = val
            else:
                self.unknowArgs.append(o)
        if len(self.unknownArgs) != 0:
            raise ArgsException()

    def _make_request_dict(self):
        properties = {}
        properties['access_key_id'] = self.qy_access_key_id
        properties['action'] = 'RunInstances'
        properties['zone'] = self.zone
        properties['version'] = self.version
        properties['vnets.1'] = 'vnet-0'
        properties['count'] = 1
        properties['signature_version'] = 1
        properties['signature_method'] = "HmacSHA256"

        properties.update(self.userPropertiesDict)

        return properties

    def run(self):
        #pre work

        if self.printUsage is True:
            self._runInstanceUsage()
            return

        # make properties dict
        properties = self._make_request_dict()

        #send
        self._send_request(properties)


def usage():
    print """
usage:
  qingcloud <action> [parameters]

Here are valid action:

  run_instance


optional arguments:
  -h, --help  show this help message and exit
"""



def run_command(args):

    sub_commands = {'run_instance': RunInstance
                    }

    #parse args and create command instance.
    if (len(args)<2):
        usage()
        exit(1)

    try:
        cls = sub_commands.get(args[1])
        print args[2:]
        cmd = cls(args[2:])
        cmd.run()
    except Exception as e:
        print e.message
        print traceback.format_exc()

if __name__ == '__main__':
    run_command(sys.argv)