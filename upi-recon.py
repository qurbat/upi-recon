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
                    upi-recon.py <phone_number> -s <suffix> (query a single UPI address with a specific suffix)
                    upi-recon.py -g <gmail_address> (query common Google Pay UPI addresses for specified google account)
"""

upi_suffix_dict = ['airtel', 'airtelpaymentsbank', 'apl', 'abfspay', 'allbank', 'andb', 'aubank', 'axis', 'albk', 'allahabadbank', 'apb', 'axisb', 'axisbank', 'axisgo', 'barodampay', 'barodapay', 'bandhan', 'birla', 'boi', 'cbin', 'cboi', 'centralbank', 'cnrb', 'dlb', 'eazypay', 'ezeepay', 'fbl', 'federal', 'freecharge', 'cmsidfc', 'csbcash', 'csbpay', 'cub', 'dbs', 'dcb', 'denabank', 'equitas', 'finobank', 'hdfcbank', 'hdfcbankjd', 'hsbc', 'ibl', 'icici', 'idbi', 'idbibank', 'idfcbank', 'icicibank', 'idfc', 'idfcnetc', 'ikwik', 'imobile', 'indianbank', 'indus', 'jkb', 'karurvysyabank', 'kaypay', 'kbl', 'kmb', 'kmbl', 'kotak', 'kvb', 'kvbank', 'lime', 'mahb', 'myicici', 'obc', 'okaxis', 'okhdfcbank', 'okicici', 'oksbi', 'paytm', 'payzapp', 'pingpay', 'pnb', 'pockets', 'rajgovhdfcbank', 'rbl', 'rmhdfcbank', 'sbi', 'sib', 'ubi', 'uboi', 'uco', 'unionbank', 'unionbankofindia', 'united', 'upi', 'utbi', 'ybl', 'yesbank', 'yesbankltd', 'indbank', 'indianbk', 'iob', 'jsbp', 'karb', 'lvb', 'lvbank', 'psb', 'purz', 'sc', 'scb', 'scbl', 'scmobile', 'srcb', 'synd', 'syndbank', 'syndicate', 'tjsb', 'vijayabank', 'vijb', 'vjb'] 

gpay_suffix_dict = ['okicici', 'oksbi', 'okaxis', 'okhdfcbank']

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
    parser.add_argument('-t', '--threads', type=int, default=None, help='number of threads to use for parallel address discovery')
    parser.add_argument('-q', '--quiet', default=False, action='store_true', help='suppress banner')
    #  group arguments
    group_1 = parser.add_mutually_exclusive_group()
    group_1.add_argument('--api_key_id', type=str, help='add api_key_id to config.ini')
    group_2 = parser.add_mutually_exclusive_group()
    group_2.add_argument('-a', '--all', default=True, action='store_true', help='query all suffixes')
    group_2.add_argument('-s', '--suffix', type=str, help='query a specific suffix')
    group_3 = parser.add_mutually_exclusive_group()
    group_3.add_argument('phone', type=str, nargs='?', help='phone number to query UPI addresses for')
    group_3.add_argument('-g', '--gpay', type=str, nargs='?', help='enter gmail address to query Google Pay UPI addresses for')
    group_4 = parser.add_mutually_exclusive_group()
    group_4.add_argument('-v', '--vpa', type=str, nargs='?', help='enter a UPI VPA')
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
    if not arguments.gpay and not arguments.phone and not arguments.vpa:
        print('[!] please enter a phone number or gmail address or vpa')
        exit(1)
    if arguments.gpay and not arguments.phone:
        email = arguments.gpay[:-10] if arguments.gpay.endswith('@gmail.com') else arguments.gpay
        phone = '8888888888'
    elif arguments.vpa and not arguments.phone:
        if arguments.vpa.split('@')[1] in upi_suffix_dict:
            vpa = arguments.vpa
        else:
            print('[!] please enter a valid vpa')
            exit(1)
        phone = '8888888888'
    elif arguments.phone and arguments.gpay:
        print('[!] please enter either a phone number or a gmail address')
        exit(1)
    elif arguments.phone:
        phone = arguments.phone[2:] if arguments.phone[0:2] == '91' and len(arguments.phone) > 10 else arguments.phone
        if len(phone) != 10:
            print('[!] please enter a valid 10 digit phone number')
            exit(1)
    # check if api_key_id is correct
    if api_key_id and not api_key_id[0:3] == 'rzp':
        quit('[!] invalid api_key_id')
    if not phone.isdigit():
        quit('[!] phone number must be numeric. use -g to query Google Pay addresses')
    #  informational header
    print('[i] starting at ' + datetime.now().strftime("%d/%m/%Y %H:%M:%S"))

    #  do the thing
    if arguments.suffix and arguments.gpay:
        print('[!] cannot use suffix and gpay at the same time. please specify only one.')
        exit(1)

    elif arguments.suffix:
        arguments.all = False
        suffix = arguments.suffix[1:] if arguments.suffix[0] == '@' else arguments.suffix
        print('[i] querying UPI addresses for phone number ' + phone)
        address_discovery(phone + '@' + suffix, API_URL + api_key_id)
        print('[i] finished at ' + datetime.now().strftime("%d/%m/%Y %H:%M:%S"))
        exit(1)
    
    elif arguments.gpay:
        if arguments.threads:
            print('[i] querying Google Pay UPI addresses for ' + email + '@gmail.com with ' + str(arguments.threads) + ' threads')
            with concurrent.futures.ThreadPoolExecutor(max_workers=arguments.threads) as executor:
                for suffix in gpay_suffix_dict:
                    try:
                        executor.submit(address_discovery, email + '@' + suffix, API_URL + api_key_id)
                        sleep(rand(0.1, 0.2))
                    except KeyboardInterrupt as e:
                        print('\n[!] interrupted! stopping threads...')
                        exit(1)
            print ('[i] finished at ' + datetime.now().strftime("%d/%m/%Y %H:%M:%S"))
            exit(1)
        else:
            print('[i] querying Google Pay UPI addresses for ' + email + '@gmail.com')
            for suffix in track(gpay_suffix_dict):
                address_discovery(email + '@' + suffix, API_URL + api_key_id)
            print('[i] finished at ' + datetime.now().strftime("%d/%m/%Y %H:%M:%S"))
            exit(1)
    
    elif arguments.vpa:
        print('[i] querying ' + vpa)
        address_discovery(vpa, API_URL + api_key_id)
        print('[i] finished at ' + datetime.now().strftime("%d/%m/%Y %H:%M:%S"))
        exit(1)

    elif arguments.all and not arguments.threads: #  query all with no concurrency
        print('[i] querying UPI addresses for phone number ' + phone)
        for suffix in track(upi_suffix_dict):
            address_discovery(phone + '@' + suffix, API_URL + api_key_id)
        print('[i] finished at ' + datetime.now().strftime("%d/%m/%Y %H:%M:%S"))
        exit(1)

    elif arguments.threads and not arguments.gpay: #  query all with threading
        print('[i] querying UPI addresses for phone number ' + phone + ' with ' + str(arguments.threads) + ' threads')
        with concurrent.futures.ThreadPoolExecutor(max_workers=arguments.threads) as executor:
            for suffix in upi_suffix_dict:
                try:
                    executor.submit(address_discovery, phone + '@' + suffix, API_URL + api_key_id)
                    sleep(rand(0.1, 0.2))
                except KeyboardInterrupt:
                    print('\n[!] interrupted! stopping threads...')
                    exit(1)
                finally:
                    print('[i] finished at ' + datetime.now().strftime("%d/%m/%Y %H:%M:%S"))
                    exit(1)
        exit(1)
