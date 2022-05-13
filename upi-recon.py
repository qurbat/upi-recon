#!/usr/bin/env python
#  -*- coding: utf-8 -*-

import argparse
from audioop import add
import os
import requests
import concurrent.futures

from time import sleep
from sys import exit
from random import uniform as rand
from datetime import datetime
from configparser import ConfigParser
from rich.progress import track

banner = """
              _                          
             (_)                         
  _   _ _ __  _ _ __ ___  ___ ___  _ __  
 | | | | '_ \| | '__/ _ \/ __/ _ \| '_ \ 
 | |_| | |_) | | | |  __/ (_| (_) | | | |
  \__,_| .__/|_|_|  \___|\___\___/|_| |_|
       | |                               
       |_|                               

	#  Author: Karan Saini (@squeal)
	#  URL: https://github.com/qurbat/upi-recon
        #  Usage:    upi-recon.py <e.g., 9999999999> (query all suffixes for phone number)
                     upi-recon.py -g <e.g., example@gmail.com> (query known gpay suffixes for google account)
                     upi-recon.py -v <e.g., address@psp> (query a single UPI VPA)
                     upi-recon.py -i <e.g., identifier> (query all suffixes for an arbitrary alphanumeric identifier)
                     upi-recon.py -f <e.g., MH01AA1234> (query known FASTag suffixes for vehicle registration number)
"""

#  opting to load lists from a file instead of hardcoding them
#  as this would be more flexible, allow for easier updates,
#  and allow others to make use of the lists provided
with open("data/general_suffixes.txt", "r") as suffix_file:
    upi_suffix_dict = suffix_file.read().splitlines() #  read all suffixes into a list

with open("data/mobile_suffixes.txt", "r") as mobile_suffix_file:
    mobile_suffix_dict = mobile_suffix_file.read().splitlines()

with open("data/fastag_suffixes.txt", "r") as fastag_suffix_file:
    fastag_suffix_dict = fastag_suffix_file.read().splitlines()

with open("data/gpay_suffixes.txt", "r") as gpay_suffix_file:
    gpay_suffix_dict = gpay_suffix_file.read().splitlines()

def searchvpa(searchtext, vpa_dict, threadcount):
    if(threadcount == 0):
        for suffix in track(vpa_dict, description="querying . . . "):
            try:
                address_discovery(searchtext + '@' + suffix, API_URL + api_key_id)
            except KeyboardInterrupt:
                print('[!] execution interrupted. quitting...')
                exit(0)
    else:
        threadcount = 10 if threadcount > 10 else threadcount
        with concurrent.futures.ThreadPoolExecutor(max_workers=threadcount) as executor:
            try:
                for suffix in vpa_dict:
                    executor.submit(address_discovery, searchtext + '@' + suffix, API_URL + api_key_id)
                    sleep(rand(0.1, 0.2))
            except KeyboardInterrupt:
                #  quit ungracefully on keyboard interrupt:
                #  considering the bandwidth consumed for requests,
                #  there is no reason to wait for the threads to finish
                #  sorry for the inconvenience
                executor._threads.clear()
                concurrent.futures.thread._threads_queues.clear()
                print('\n[!] execution interrupted. quitting...')
    print('[i] finished at ' + datetime.now().strftime("%d/%m/%Y %H:%M:%S"))
    exit(1)

def address_discovery(vpa, api_url):
    
    r = requests.post(api_url, data={'entity':'vpa','value':vpa}, headers={'Connection':'close'})
    if r.status_code == 200 and r.json()['success'] is True:
        print('[+] ' + vpa + ' is a valid UPI payment address registered to ' + r.json()['customer_name']) if r.json()['customer_name'] else print('[!] The name associated with the UPI payment address could not be determined')
#       if r.status_code == 200 and r.json()['success'] == False:
#            print('[-] ' + vpa + ' not a valid UPI address')
#  todo:      store in dict by default and print if verbosity is set
    if r.status_code == 400 and "Please enter a valid Virtual Payment Address" in r.text:
        print('[-] query failed for ' + vpa)
        print('[!] "' + vpa + '" may not be a valid address')


if __name__ == '__main__':
    #  argument definition
    parser = argparse.ArgumentParser(prog='upi-recon.py')
    #  primary arguments
    parser.add_argument('-t', '--threads', type=int, default=0, help='number of threads to use for parallel address discovery')
    parser.add_argument('-q', '--quiet', default=False, action='store_true', help='suppress banner')
    #  group arguments
    group_1 = parser.add_mutually_exclusive_group()
    group_1.add_argument('--api_key_id', type=str, help='add api_key_id to config/config.ini')
    group_2 = parser.add_mutually_exclusive_group()
    group_2.add_argument('phone', type=str, nargs='?', help='phone number to query UPI addresses for')
    group_3 = parser.add_mutually_exclusive_group()
    group_3.add_argument('-g', '--gpay', type=str, nargs='?', help='enter gmail address to query Google Pay UPI addresses for')
    group_4 = parser.add_mutually_exclusive_group()
    group_4.add_argument('-v', '--vpa', type=str, nargs='?', help='enter a single VPA to query')
    group_5 = parser.add_mutually_exclusive_group()
    group_5.add_argument('-i', '--identifier', type=str, nargs='?', help='enter an address to query against all providers')
    group_6 = parser.add_mutually_exclusive_group()
    group_6.add_argument('-f', '--fastag', type=str, nargs='?', help='Enter a vehicle number to search for')
    
    #  parse arguments
    arguments = parser.parse_args()
    #  check the configuration
    if not os.path.exists('config/config.ini'):
        print('[!] config/config.ini not found! please create the config file\n[!] you may refer to config/config.ini.example for help')
        exit(1)
    config = ConfigParser()
    config_file = 'config/config.ini'
    config.read(config_file)
    #  deal with arguments
    if arguments.quiet is False:
        print(banner)
    if arguments.api_key_id:  #  write api_key_id to config/config.ini if provided 
        config.set('main', 'api_key_id', arguments.api_key_id)
        with open(config_file, 'w') as configfile:
            config.write(configfile)
    
    #  API stuff
    API_URL = 'https://api.razorpay.com/v1/payments/validate/account?key_id='
    api_key_id = config.get('main', 'api_key_id')
    #  check if api_key_id is correct
    if api_key_id and not api_key_id[0:3] == 'rzp':
        exit('[!] invalid api_key_id')
    #  print informational header
    print('[i] starting at ' + datetime.now().strftime("%d/%m/%Y %H:%M:%S"))
    #  query address directly
    #  this may not be the best way to handle this, but it works for now
    if arguments.vpa and '@' in arguments.vpa:
        address_discovery(arguments.vpa, API_URL + api_key_id)
    elif arguments.vpa and '@' not in arguments.vpa:
        print('[!] please enter a full, valid UPI address e.g. <identifier>@<provider>')
        exit(0)

    #  query based on phone number
    elif arguments.phone:
        searchtext = arguments.phone[2:] if arguments.phone[0:2] == '91' and len(arguments.phone) > 10 else arguments.phone
        if not searchtext.isdigit():
            exit('[!] phone number must be numeric')
        if len(searchtext) != 10:
            print('[!] please enter a valid 10 digit phone number')
            exit(1)
        print('[i] querying {} suffixes for phone number '.format(len(mobile_suffix_dict)) + searchtext)
        searchvpa(searchtext, mobile_suffix_dict, arguments.threads)
    #  query based on gpay address
    elif arguments.gpay:
        searchtext = arguments.gpay[:-10] if arguments.gpay.endswith('@gmail.com') else arguments.gpay
        print('[i] querying {} suffixes for '.format(len(gpay_suffix_dict)) + searchtext + '@gmail.com')
        searchvpa(searchtext, gpay_suffix_dict, 4) #  overriding threads to 4 as there are only 4 VPA addresses to check for gpay
    #  query based on fastag vehicle registration number
    elif arguments.fastag:
        searchtext = 'netc.' + arguments.fastag
        print('[i] querying {} suffixes for vehicle '.format(len(fastag_suffix_dict)) + arguments.fastag)
        searchvpa(searchtext, fastag_suffix_dict, arguments.threads)
    #  query alphanumeric identifier across all providers
    elif arguments.identifier:
        searchtext = arguments.identifier if '@' not in arguments.identifier else arguments.identifier.split('@')[0]
        print('[i] querying {} suffixes for identifier '.format(len(upi_suffix_dict)) + searchtext)
        searchvpa(searchtext, upi_suffix_dict, arguments.threads)
    #  print error if no arguments provided
    #  this is a probably a bad way to handle empty arguments, but it works 
    else:
        print('[!] please enter a valid argument')
        print('[!] usage: upi-recon.py -h for help')
        exit(1)