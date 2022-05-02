# upi-recon
![screenshot of upi-recon](https://i.imgur.com/GexQjBq.gif)

A command line tool for UPI payment address discovery and reconaissance.
## Requirements
`pip install -r requirements.txt`

## Configuration
You can use the following command to add an API key ID to the configuration file. Please [refer to the documentation](https://razorpay.com/docs/payments/dashboard/settings/api-keys/) provided by Razorpay in order to generate valid API credentials.

`upi-recon.py <phone_number> --api_key_id <api_key_id>`

**Note:** Razorpay does not consider an API key ID as sensitive information. While the process of arbitrarily discovering a valid API key ID for any given Razorpay merchant is fairly straightforward, it is beyond the scope of the repository and will thus not be covered. In any case, it is suggested that you generate your own Razorpay API credentials for use with upi-recon.

## Usage
### Query all possible UPI addresses for the provided phone number
`upi-recon.py <phone_number>`
### Query all possible UPI addresses for the provided phone number using a specified number of threads
`upi-recon.py <phone_number> -t 5`
### Query a single UPI address for the provided phone number using a provided suffix
`upi-recon.py <phone_number> -s <suffix>`

## Contributions
Contributions are welcome. Feature wishlist:
- Introduce support for more API providers [] 
- Improve argument parsing section []
- Refactor code to publish as a Python module []