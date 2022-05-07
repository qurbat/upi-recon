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
### Query all possible FASTag addresses for a vehicle registration number
`upi-recon.py -f <vehicle_number>`
### Query all possible UPI addresses for a given term
`upi-recon.py -w <word>`

## Disclaimer / Warranty

- An UPI Virtual Payment Address does not have data security classification and by virtue of its usage and practice, considered a public information, just as how email address of a person is publicly available information.
- The tool lets one verify the name of account holder for a specific set of payment addresses. The same is possible manually by opening any UPI app and querying in the "Make payment to a contact / VPA" screen in most apps.
- VPAs are virtual and can be dynamically linked to any bank account that is linked to the same mobile number and hence the underlying owner of the account can differ at different points of time, should the owner of VPA changes the destination of the VPA to a different bank account.
- Use of this tool comes with no warranties.

## Contributions
Contributions are welcome. Feature wishlist:
- [x] Introduce support for Google Pay addresses
- [x] Improve argument parsing code
- [ ] Introduce support for more API providers
- [ ] Introduce support for wordlist based address discovery
- [ ] Refactor for release as Python module
