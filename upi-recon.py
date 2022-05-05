#!/usr/bin/env python
# -*- coding: utf-8 -*-

import argparse
import os
import requests
import concurrent.futures

from time import sleep
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

	# Author: Karan Saini (@squeal)
	# URL: https://github.com/qurbat/upi-recon
        # Usage:    upi-recon.py <phone_number> (query all possible UPI addresses)
                    upi-recon.py <phone_number> -t 5 (query all possible UPI addresses with specified number of threads)
                    upi-recon.py -g <gmail_address> (query common Google Pay UPI addresses for specified google account)
                    upi-recon.py -v <vpa> (query a single UPI VPA)
                    upi-recon.py -w <word> (query a single word)
                    upi-recon.py -f <vehicle_number> (query a vehicle number to check name of owner of the linked FASTag)
"""

with open("vpa_suffixes.txt", "r") as suffix_file:
    upi_suffix_dict = suffix_file.read().splitlines() # read all suffixes into a list

with open("fastag_issuer_suffixes.txt", "r") as fastag_suffix_file:
    fastag_suffix_dict = fastag_suffix_file.read().splitlines()

gpay_suffix_dict = ['okicici', 'oksbi', 'okaxis', 'okhdfcbank']

def searchvpa(searchtext, vpa_dict, threadcount):
    if(threadcount == 0):
        for suffix in track(vpa_dict):
            address_discovery(searchtext + '@' + suffix, API_URL + api_key_id)
    else:
        with concurrent.futures.ThreadPoolExecutor(max_workers=threadcount) as executor:
            for suffix in vpa_dict:
                try:
                    executor.submit(address_discovery, searchtext + '@' + suffix, API_URL + api_key_id)
                    sleep(rand(0.1, 0.2))
                except KeyboardInterrupt as e:
                    print('\n[!] interrupted! stopping threads...')
                    exit(1)
    print('[i] finished at ' + datetime.now().strftime("%d/%m/%Y %H:%M:%S"))
    exit(1)

def address_discovery(vpa, api_url):
    try:
        r = requests.post(api_url, data={'entity':'vpa','value':vpa}, headers={'Connection':'close'})
        if r.status_code == 200 and r.json()['success'] is True:
            print('[+] ' + vpa + ' is a valid UPI payment address registered to ' + r.json()['customer_name']) if r.json()['customer_name'] else print('[!] The name associated with the UPI payment address could not be determined')
#       if r.status_code == 200 and r.json()['success'] == False:
#            print('[-] ' + vpa + ' not a valid UPI address')
#  todo:      store in dict by default and print if verbosity is set
        if r.status_code == 400 and "Please enter a valid Virtual Payment Address" in r.text:
            print('[-] query failed for ' + vpa)
            print('[!] "' + suffix + '" may not be a valid suffix')
    except Exception as e:
        print(e)


if __name__ == '__main__':
    #  argument definition
    parser = argparse.ArgumentParser(description='fetch UPI addresses and associated information for a given phone number')
    #  primary arguments
    parser.add_argument('-t', '--threads', type=int, default=0, help='number of threads to use for parallel address discovery')
    parser.add_argument('-q', '--quiet', default=False, action='store_true', help='suppress banner')
    #  group arguments
    group_1 = parser.add_mutually_exclusive_group()
    group_1.add_argument('--api_key_id', type=str, help='add api_key_id to config.ini')
    group_2 = parser.add_mutually_exclusive_group()
    group_2.add_argument('phone', type=str, nargs='?', help='phone number to query UPI addresses for')
    group_3 = parser.add_mutually_exclusive_group()
    group_3.add_argument('-g', '--gpay', type=str, nargs='?', help='enter gmail address to query Google Pay UPI addresses for')
    group_4 = parser.add_mutually_exclusive_group()
    group_4.add_argument('-v', '--vpa', type=str, nargs='?', help='Enter a VPA to verify')
    group_5 = parser.add_mutually_exclusive_group()
    group_5.add_argument('-w', '--word', type=str, nargs='?', help='Enter a word to search for')
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
    if arguments.api_key_id:  #  write api_key_id to config.ini if provided 
        config.set('main', 'api_key_id', arguments.api_key_id)
        with open(config_file, 'w') as configfile:
            config.write(configfile)
    
    # set variables and normalize input
    API_URL = 'https://api.razorpay.com/v1/payments/validate/account?key_id='
    api_key_id = config.get('main', 'api_key_id')
    # check if api_key_id is correct
    if api_key_id and not api_key_id[0:3] == 'rzp':
        quit('[!] invalid api_key_id')

    #  informational header
    print('[i] starting at ' + datetime.now().strftime("%d/%m/%Y %H:%M:%S"))    
    if arguments.vpa:
        if not arguments.vpa.split('@')[1] in upi_suffix_dict:
            print('[!] please enter a valid vpa')
        else:
            address_discovery(arguments.vpa, API_URL + api_key_id)
        exit(1)
    
    elif arguments.phone:
        searchtext = arguments.phone[2:] if arguments.phone[0:2] == '91' and len(arguments.phone) > 10 else arguments.phone
        if not searchtext.isdigit():
            quit('[!] phone number must be numeric')
        if len(searchtext) != 10:
            print('[!] please enter a valid 10 digit phone number')
            exit(1)
        print('[i] querying UPI addresses for phone number ' + searchtext)
        searchvpa(searchtext,upi_suffix_dict,arguments.threads)

    elif arguments.gpay:
        searchtext = arguments.gpay[:-10] if arguments.gpay.endswith('@gmail.com') else arguments.gpay
        print('[i] querying Google Pay UPI addresses for ' + searchtext + '@gmail.com')
        searchvpa(searchtext,gpay_suffix_dict,arguments.threads)

    elif arguments.fastag:
        searchtext = 'netc.' + arguments.fastag
        print('[i] querying FASTags for vehicle ' + arguments.fastag)
        searchvpa(searchtext,fastag_suffix_dict,arguments.threads)

    elif arguments.word:
        searchtext = arguments.word
        print('[i] querying word ' + searchtext + ' in VPAs')
        searchvpa(searchtext,upi_suffix_dict,arguments.threads)
    else:
        print('[!] please enter a phone number / gmail address / vpa / word / vehicle number')
        exit(1)