# upi-recon
![screenshot of upi-recon](https://i.imgur.com/GexQjBq.gif)

This project was primarily created for demonstrating the range of correlated information that can be extracted from and along with Unified Payments Interface ("UPI") Virtual Payment Addresses. upi-recon has support for several types of queries that can be used to obtain personal information associated with UPI payment addresses.

## Requirements
`pip install -r requirements.txt`

## Configuration
You can use the following command to add an API key ID to the configuration file.

`upi-recon.py <phone_number> --api_key_id <api_key_id>`

Please [refer to the documentation](https://razorpay.com/docs/payments/dashboard/settings/api-keys/) provided by Razorpay in order to generate valid `live` API credentials.

**Note:** `test` credentials will not work.

**Note:** Razorpay does not seem to consider an API key ID as being sensitive information. Further, while the process of arbitrarily discovering the API key ID for a Razorpay merchant is fairly straightforward, it is beyond the scope of the repository and will thus not be covered. It is suggested that you generate your own Razorpay API credentials for use with upi-recon.

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
- [x] Introduce support for FASTag addresses
- [x] Introduce support for Google Pay addresses
- [x] Improve argument parsing code

## Disclaimer

Note: Unified Payment Interface ("UPI") Virtual Payment Addresses ("VPAs") do not carry a data security classification by virtue of their usage in practice, and should as such be considered to be public information, similar to how email addresses may be considered to be public information.

This tool allows users to **1)** check the existence of UPI payment addresses, and **2)** fetch associated information about the account holder, in an automated manner based on provided input. This functionality is already available (however, not in an automated fashion) through most UPI payment applications available on the Android and/or iOS platforms. 

This tool is provided "AS IS" without any warranty of any kind, either expressed, implied, or statutory, to the extent permitted by applicable law.
