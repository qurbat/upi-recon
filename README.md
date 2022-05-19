# upi-recon
![screenshot of upi-recon](https://i.imgur.com/GexQjBq.gif)

upi-recon is a command line tool for UPI payment address discovery and reconnaissance. The project was primarily created for demonstrating the range of correlated information that can be extracted from and along with Unified Payments Interface ("UPI") Virtual Payment Addresses.

The tool has support for several input types which can be used to obtain (and otherwise extrapolate) information associated with UPI virtual payment addresses.

## Requirements
`pip install -r requirements.txt`

## Usage
### Query all possible UPI addresses for the provided phone number
`upi-recon.py -p <phone_number>`
### Query all possible UPI addresses for the provided phone number using a specified number of threads
`upi-recon.py -p <phone_number> -t 5`
### Query a single UPI address for the provided VPA
`upi-recon.py -v <single_vpa>`
### Query all possible UPI addresses for the provided Gmail address
`upi-recon.py -g <gmail_username>`
### Query all possible FASTag addresses for a vehicle registration number
`upi-recon.py -f <vehicle_number>`
### Query all possible UPI addresses for a given term
`upi-recon.py -w <word>`

## Contributions
Contributions are welcome. Feature wishlist:
- [ ] Introduce support for more API providers
- [ ] Introduce support for wordlist based address discovery
- [ ] Refactor for release as Python module

## Acknowledgements

- Srikanth L (added FASTag and Google support)
- Anant Shrivastava (QoL improvements)

## Disclaimer

Note: Unified Payment Interface ("UPI") Virtual Payment Addresses ("VPAs") do not carry a data security classification by virtue of their usage in practice, and should as such be considered to be public information, similar to how email addresses may be considered to be public information.

This tool allows users to **1)** check the existence of UPI payment addresses, and **2)** fetch associated information about the account holder, in an automated manner based on provided input. This functionality is already available (however, not in an automated fashion) through most UPI payment applications available on the Android and/or iOS platforms. 

This tool is provided "AS IS" without any warranty of any kind, either expressed, implied, or statutory, to the extent permitted by applicable law.
