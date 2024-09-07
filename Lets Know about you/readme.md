# 🌐 Footprinting Tool 📡

Welcome to the Footprinting Tool! This Python script helps gather various types of information about a domain or IP address. Perfect for network security enthusiasts and digital investigators.

![Output 1](https://github.com/Raghavkumarprabhakar/Cyber-Security-Project/blob/main/Lets%20Know%20about%20you/screen%20shot/Screenshot%202024-09-07%20230055.png)
*Explore the details with our powerful tool!*

## Features 🚀

- **DNS Lookup**: 🌍 Get the IP address of a domain.
- **WHOIS Lookup**: 🕵️‍♂️ Retrieve domain registration details.
- **Reverse DNS Lookup**: 🔄 Find the domain associated with an IP address.
- **Subdomain Finder**: 🔍 Identify common subdomains.
- **Port Scanning**: 🔓 Detect open ports on a domain.
- **IP WHOIS Lookup**: 📊 Gather IP address details.
- **Email Scraping**: 📧 Extract emails from a domain's web page.
- **Social Media Finder**: 📱 Locate social media accounts related to a domain.
- **Detailed IP Information**: 🌐 Get comprehensive IP address data.
- **Email Details**: 📨 Verify and analyze email addresses.

## Requirements 📦

- `socket`
- `whois`
- `dns.resolver`
- `requests`
- `re`
- `json`
- `BeautifulSoup` from `bs4`
- `IPWhois` from `ipwhois`
- `pyfiglet`

1. Install required packages using pip:
     ```bash
        pip install whois requests beautifulsoup4 ipwhois pyfiglet

## How to Use 🛠️

1. **Clone the Repository:**

    ```bash
    git clone https://github.com/yourusername/footprinting-tool.git
    cd footprinting-tool
    ```

2. **Run the Script:**

    ```bash
    python footprinting_tool.py
    ```

3. **Enter the Domain or IP Address:**

    The script will prompt you to enter the domain you want to analyze. You can also provide an email address for email details.

## Example Output 📋

### DNS Lookup 🔍

*Example of DNS lookup results.*

### WHOIS Lookup 📄

*Example of WHOIS lookup results.*

     ```plaintext
       Footprinting results for: example.com

       DNS Lookup: 93.184.216.34
       WHOIS Lookup:
    ...

       Subdomains: www.example.com, mail.example.com
       Open Ports: 80, 443
       IP WHOIS Lookup:
    ...

       Emails: contact@example.com
       Social Media Accounts:
       facebook.com: http://facebook.com/search?q=example.com
    ...

       IP: 93.184.216.34
       Country: United States
    ...

       Email: info@example.com

## Notes 📝

- **API Keys:** Remember to replace placeholder API keys with your own for `ipstack` and `Hunter.io` services.
- **Usage:** Ensure you have the necessary permissions to perform footprinting on the domains/IP addresses you are analyzing.

## Contributing 🤝

Feel free to contribute to this project by submitting issues or pull requests.

## 



