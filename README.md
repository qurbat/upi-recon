# upi-recon
![screenshot of upi-recon](https://i.imgur.com/GexQjBq.gif)

A command line tool for UPI payment address discovery and reconnaissance.
## Requirements
`pip install -r requirements.txt`

## Configuration
You can use the following command to add an API key ID to the configuration file.

`upi-recon.py <phone_number> --api_key_id <api_key_id>`

Please [refer to the documentation](https://razorpay.com/docs/payments/dashboard/settings/api-keys/) provided by Razorpay in order to generate valid API credentials.

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
### Query all possible FASTags for a given vehicle number
`upi-recon.py -f <vehicle_number>`
### Query all possible UPI addresses for the provided word
`upi-recon.py -w <word>`


## Contributions
Contributions are welcome. Feature wishlist:
- [x] Introduce support for Google Pay addresses
- [x] Improve argument parsing code
- [ ] Introduce support for more API providers
- [ ] Introduce support for wordlist based address discovery
- [ ] Refactor for release as Python module
