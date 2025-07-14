#!/usr/bin/python

########################################
#                                      #
#  Used to control Nessus through      #
#  scripting.                          #
#                                      #
#  Requires Python 2.x and requests    #
#  module                              #
#                                      #
#  Copyright (C) 2016 Matt Grandy      #
#  Email: grandy[at]redteamsecure.com  #
#                                      #
########################################

try:
    import requests
except ImportError:
    print('Need to install the Requests module before execution')
    exit()

import json
import sys
import argparse
import time
import os
from pathlib import Path

# Load environment variables from .env if present
try:
    from dotenv import load_dotenv
    env_path = Path(__file__).parent / '.env'
    if env_path.exists():
        load_dotenv(dotenv_path=env_path)
except ImportError:
    pass


# Check to make sure the user has version 3.x of python, if not, exit.
current_maj_version = sys.version_info.major
if current_maj_version < 3:
    print('This script must be run with Python version 3.x or higher')
    exit()

# Disable Warning when not verifying SSL certs.
requests.packages.urllib3.disable_warnings()

# Create options and help menu
parser = argparse.ArgumentParser(description='Control Nessus with this script')
group = parser.add_mutually_exclusive_group()
group.add_argument('-l', '--list', dest='scan_list', action='store_true', help='List current scans and IDs')
group.add_argument('-p', '--policies', dest='policy_list', action='store_true', help='List current policies')
group.add_argument('-sS', '--start', dest='start_scan_id', type=str, help='Start a specified scan using scan id')
group.add_argument('-sR', '--resume', dest='resume_scan_id', type=str, help='Resume a specified scan using scan id')
group.add_argument('-pS', '--pause', dest='pause_scan_id', type=str, help='Pause a specified scan using scan id')
group.add_argument('-sP', '--stop', dest='stop_scan_id', type=str, help='Stop a specified scan using scan id')

args = parser.parse_args()

if not len(sys.argv) > 1:
    parser.print_help()
    print()
    exit()


# Specify credentials for Nessus and initialize vars
url = 'https://localhost:8834'
verify = False
token = ''
username = os.environ.get('NESSUS_USERNAME', 'xxxxx')
password = os.environ.get('NESSUS_PASSWORD', 'xxxxx')

class create_menu:
    '''This is used to build an instance of the menu object
       and can be called from the main program to instantiate the menu
       with passed variables.'''
    def __init__(self, menu, text, other):
        self.text = text
        self.menu = menu
        self.other = other

        # Build the menu
        option_length_menu = len(str(menu))
        option_length_text = len(str(text))
        if self.other != 'Null':
            print('{:<20}  :    {:<15}  :    {}'.format(menu, text, other))
        else:
            print('{:<15}  :  {}'.format(menu, text))
        return

def build_url(resource):
    return '{0}{1}'.format(url, resource)


def connect(method, resource, data=None, params=None):
    """
    Send a request
    Send a request to Nessus based on the specified data. If the session token
    is available add it to the request. Specify the content type as JSON and
    convert the data to JSON format.
    """
    headers = {'X-Cookie': 'token={0}'.format(token),
               'content-type': 'application/json'}

    if data is not None:
        data = json.dumps(data)

    if method == 'POST':
        r = requests.post(build_url(resource), data=data, headers=headers, verify=verify)
    elif method == 'PUT':
        r = requests.put(build_url(resource), data=data, headers=headers, verify=verify)
    elif method == 'DELETE':
        r = requests.delete(build_url(resource), data=data, headers=headers, verify=verify)
    else:
        r = requests.get(build_url(resource), params=params, headers=headers, verify=verify)

    # Exit if there is an error.
    if r.status_code != 200:
        try:
            e = r.json()
            print(e['error'])
        except Exception:
            print('HTTP Error:', r.status_code)
        sys.exit()

    # When downloading a scan we need the raw contents not the JSON data.
    if 'download' in resource:
        return r.content

    # All other responses should be JSON data. Return raw content if they are
    # not.
    try:
        return r.json()
    except ValueError:
        return r.content


def login(usr, pwd):
    # Login to Nessus.

    login = {'username': usr, 'password': pwd}
    data = connect('POST', '/session', data=login)
    return data['token']


def get_policies():
    """
    Get scan policies
    Get all of the scan policies but return only the title and the uuid of
    each policy.
    """
    data = connect('GET', '/editor/policy/templates')
    return {p['title']: p['uuid'] for p in data['templates']}


def get_scans():
    """
    Get history ids
    Create a dictionary of scans and uuids
    """

    status_dict = {}
    name_dict = {}
    data = connect('GET', '/scans/')
    for p in data['scans']:
        status_dict[p['id']] = p['status']
        name_dict[p['id']] = p['name']
    return status_dict, name_dict


def get_history_ids(sid):
    """
    Get history ids
    Create a dictionary of scan uuids and history ids so we can lookup the
    history id by uuid.
    """
    data = connect('GET', '/scans/{0}'.format(sid))
    temp_hist_dict = {h['history_id']: h['status'] for h in data['history']}
    temp_hist_dict_rev = {a: b for b, a in temp_hist_dict.items()}
    try:
        for key, value in temp_hist_dict_rev.items():
            print(key)
            print(value)
    except Exception:
        pass


def get_scan_history(sid, hid):
    """
    Scan history details
    Get the details of a particular run of a scan.
    """
    params = {'history_id': hid}
    data = connect('GET', '/scans/{0}'.format(sid), params)
    return data['info']


def get_status(sid):
    # Get the status of a scan by the sid.
    # Print out the scan status

    time.sleep(3) # sleep to allow nessus to process the previous status change
    temp_status_dict, temp_name_dict = get_scans()
    print('\nScan Name           Status  ')
    print('---------------------------------------')
    for key, value in temp_name_dict.items():
        if str(key) == str(sid):
            create_menu(value, temp_status_dict[key], 'Null')


def launch(sid):
    # Launch the scan specified by the sid.

    data = connect('POST', '/scans/{0}/launch'.format(sid))
    return data['scan_uuid']

def pause(sid):
    # Pause the scan specified by the sid.
    connect('POST', '/scans/{0}/pause'.format(sid))
    return

def resume(sid):
    # Resume the scan specified by the sid.
    connect('POST', '/scans/{0}/resume'.format(sid))
    return

def stop(sid):
    # Resume the scan specified by the sid.
    connect('POST', '/scans/{0}/stop'.format(sid))
    return

def logout():
    # Logout of Nessus.
    print('Logging Out...')
    connect('DELETE', '/session')
    print('Logged Out')
    exit()



if __name__ == '__main__':
    print('Script started: ' + time.strftime('%m-%d-%y @ %H:%M:%S'))

    if 'xxxxx' in [username, password]:
        print('Please update the credentials in the .env file')
        print('Set NESSUS_USERNAME and NESSUS_PASSWORD environment variables or edit the .env file')
        exit()

    print('Logging in...')
    try:
        token = login(username, password)
    except Exception:
        print('Unable to login :(')
        exit()
    print('Logged in!\n\n')

    ###### Display all policies  #######
    if args.policy_list:
        # If -p flag is specified, print the policy list and exit
        print("Printing Policies \n\n")
        policy_dict = get_policies()
        print('Policy Name                              UUID')
        print('--------------------------------------------------')
        for title, uuid in policy_dict.items():
            create_menu(title, uuid, 'Null')

    ###### Display all scans  #######
    elif args.scan_list:
        # If -l flag is specified, print the list of scans
        temp_status_dict, temp_name_dict = get_scans()
        print('Scan Name                  Status              ID')
        print('-------------------------------------------------')
        for status_id, status_value in temp_status_dict.items():
            for name_id, name_value in temp_name_dict.items():
                if status_id == name_id:
                    create_menu(name_value, status_value, status_id)

    ###### Start the scan  #######
    if args.start_scan_id:
        # If -sS [scan_id] flag is passed, start the specified scan
        start_id = args.start_scan_id
        temp_status_dict, temp_name_dict = get_scans()
        # Grab the status of the scan and either resume or start based on status
        for key, value in temp_name_dict.items():
            if str(key) == str(start_id):
                if temp_status_dict[key].lower() in ['stopped', 'completed', 'aborted', 'canceled', 'on demand', 'empty']:
                    print('Launching Scan {}'.format(key))
                    launch(start_id)
                elif temp_status_dict[key].lower() in ['running']:
                    print('Scan already running!')
                    logout()
                else:
                    print('Scan already started or paused.')
                    print('If you need to start a previously completed scan, add "completed" to the list on line 269')
                    logout()
        # Re-grab the scans to get the updated status
        get_status(start_id)

    ###### Resume the scan  #######
    if args.resume_scan_id:
        # If -sR [scan_id] flag is passed, start the specified scan
        start_id = args.resume_scan_id
        temp_status_dict, temp_name_dict = get_scans()
        # Grab the status of the scan and either resume or start based on status
        for key, value in temp_name_dict.items():
            if str(key) == str(start_id):
                if temp_status_dict[key].lower() in ['paused']:
                    print('Resuming Scan {}'.format(key))
                    resume(start_id)
                elif temp_status_dict[key].lower() in ['running']:
                    print('Scan already running!')
                    logout()
                else:
                    print('Scan unable to start.')
                    print('If you need to start a previously completed scan, add "completed" to the list on line 269')
                    logout()
        # Re-grab the scans to get the updated status
        get_status(start_id)

    ###### Pause the scan  #######
    elif args.pause_scan_id:
        # If -pS [scan_id] flag is passed, pause the specified scan
        pause_id = args.pause_scan_id
        temp_status_dict, temp_name_dict = get_scans()
        for key, value in temp_name_dict.items():
            if str(key) == str(pause_id):
                if temp_status_dict[key].lower() in ['paused']:
                    print('Scan already paused!')
                    logout()
                elif temp_status_dict[key].lower() in ['running']:
                    print('Pausing Scan {}'.format(key))
                    pause(pause_id)
                else:
                    print('Scan unable to be paused')
                    logout()
        # Re-grab the scans to get the updated status
        get_status(pause_id)

    ###### Stop the scan  #######
    elif args.stop_scan_id:
        # If -sP [scan_id] flag is passed, stop the specified scan
        stop_id = args.stop_scan_id
        temp_status_dict, temp_name_dict = get_scans()
        for key, value in temp_name_dict.items():
            if str(key) == str(stop_id):
                if temp_status_dict[key].lower() in ['paused', 'running']:
                    print('Stopping Scan {}'.format(key))
                    stop(stop_id)
                    logout()
                else:
                    print('Scan cannot be stopped!')
                    logout()
        # Re-grab the scans to get the updated status
        get_status(stop_id)