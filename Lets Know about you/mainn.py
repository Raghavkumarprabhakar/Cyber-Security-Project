import socket
import whois
import dns.resolver
import requests
import re
import json
from bs4 import BeautifulSoup
from ipwhois import IPWhois
import pyfiglet

# Function to perform DNS lookup
def dns_lookup(domain):
    try:
        result = socket.gethostbyname(domain)
        return result
    except socket.gaierror:
        return "DNS lookup failed"

# Function to perform WHOIS lookup
def whois_lookup(domain):
    try:
        result = whois.whois(domain)
        return result
    except Exception as e:
        return str(e)

# Function to perform reverse DNS lookup
def reverse_dns_lookup(ip):
    try:
        result = socket.gethostbyaddr(ip)
        return result
    except socket.herror:
        return "Reverse DNS lookup failed"

# Function to find subdomains
def find_subdomains(domain):
    subdomains = ['www', 'mail', 'ftp', 'test']
    found_subdomains = []
    for subdomain in subdomains:
        subdomain_url = f"{subdomain}.{domain}"
        try:
            result = socket.gethostbyname(subdomain_url)
            found_subdomains.append(subdomain_url)
        except socket.gaierror:
            continue
    return found_subdomains

# Function to perform port scanning
def port_scan(domain):
    ports = [21, 22, 23, 25, 53, 80, 110, 443, 8080]
    open_ports = []
    for port in ports:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        socket.setdefaulttimeout(1)
        result = sock.connect_ex((domain, port))
        if result == 0:
            open_ports.append(port)
        sock.close()
    return open_ports

# Function to perform IP WHOIS lookup
def ip_whois_lookup(ip):
    try:
        obj = IPWhois(ip)
        result = obj.lookup_rdap()
        return result
    except Exception as e:
        return str(e)

# Function to scrape web pages for emails
def scrape_emails(domain):
    url = f"http://{domain}"
    try:
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')
        emails = set(re.findall(r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}", response.text))
        return emails
    except Exception as e:
        return str(e)

# Function to find social media accounts
def find_social_media(domain):
    social_media_sites = ['facebook.com', 'twitter.com', 'linkedin.com', 'instagram.com']
    social_media_accounts = {}
    for site in social_media_sites:
        url = f"http://{site}/search?q={domain}"
        try:
            response = requests.get(url)
            if response.status_code == 200:
                social_media_accounts[site] = url
        except requests.exceptions.RequestException:
            continue
    return social_media_accounts

# Function to get detailed IP address information
def get_ip_details(ip):
    try:
        # Using ip-api for IP details
        url_ip_api = f"http://ip-api.com/json/{ip}"
        response_ip_api = requests.get(url_ip_api).json()

        # Using ipstack for additional IP details
        api_key = 'fd0c1eae3c2d27ee676af0db2b864b0e'  # Replace with your ipstack API key
        url_ipstack = f"http://api.ipstack.com/{ip}?access_key={api_key}"
        response_ipstack = requests.get(url_ipstack).json()

        if response_ip_api['status'] == 'success':
            location_info = {
                "IP": response_ipstack.get('ip', 'N/A'),
                "IP Type": response_ipstack.get('type', 'N/A'),
                "Continent Name": response_ipstack.get('continent_name', 'N/A'),
                "Continent Code": response_ipstack.get('continent_code', 'N/A'),
                "Country": response_ipstack.get('country_name', 'N/A'),
                "Country Code": response_ip_api.get('countryCode', 'N/A'),
                "Region Name": response_ipstack.get('region_name', 'N/A'),
                "Region Code": response_ipstack.get('region_code', 'N/A'),
                "City": response_ipstack.get('city', 'N/A'),
                "Zip": response_ipstack.get('zip', 'N/A'),
                "TimeZone": response_ip_api.get('timezone', 'N/A'),
                "ISP": response_ip_api.get('isp', 'N/A'),
                "Latitude": response_ipstack.get('latitude', 'N/A'),
                "Longitude": response_ipstack.get('longitude', 'N/A')
            }
            return location_info
        else:
            return {"Error": "Unable to retrieve location info"}
    except Exception as e:
        return {"Error": str(e)}

# Function to get details from Gmail address using Hunter.io API
def get_email_details(email):
    try:
        hunter_api_key = 'YOUR_HUNTER_API_KEY'  # Replace with your Hunter.io API key
        url = f"https://api.hunter.io/v2/email-verifier?email={email}&api_key={hunter_api_key}"
        response = requests.get(url).json()

        if response.get('data'):
            email_info = {
                "Email": email,
                "Result": response['data'].get('result', 'N/A'),
                "Score": response['data'].get('score', 'N/A'),
                "Domain": response['data'].get('domain', 'N/A'),
                "Disposable": response['data'].get('disposable', 'N/A'),
                "Webmail": response['data'].get('webmail', 'N/A'),
                "SMTP Check": response['data'].get('smtp_check', 'N/A'),
                "Accept All": response['data'].get('accept_all', 'N/A'),
                "Block": response['data'].get('block', 'N/A'),
                "Sources": response['data'].get('sources', [])
            }
            return email_info
        else:
            return {"Error": "Unable to retrieve email details"}
    except Exception as e:
        return {"Error": str(e)}

# Main function to gather all information
def footprinting(domain, email=None):
    print(f"Footprinting results for: {domain}")

    # DNS Lookup
    dns_result = dns_lookup(domain)
    print(f"DNS Lookup: {dns_result}")

    # WHOIS Lookup
    whois_result = whois_lookup(domain)
    print(f"WHOIS Lookup:\n{whois_result}")

    # Reverse DNS Lookup
    reverse_dns_result = reverse_dns_lookup(dns_result)
    print(f"Reverse DNS Lookup: {reverse_dns_result}")

    # Subdomain Finding
    subdomains_result = find_subdomains(domain)
    print(f"Subdomains: {', '.join(subdomains_result)}")

    # Port Scanning
    ports_result = port_scan(domain)
    print(f"Open Ports: {', '.join(map(str, ports_result))}")

    # IP WHOIS Lookup
    ip_whois_result = ip_whois_lookup(dns_result)
    print(f"IP WHOIS Lookup:\n{ip_whois_result}")

    # Scrape Emails
    emails = scrape_emails(domain)
    print(f"Emails: {', '.join(emails)}")

    # Find Social Media Accounts
    social_media_accounts = find_social_media(domain)
    print("Social Media Accounts:")
    for site, url in social_media_accounts.items():
        print(f"{site}: {url}")

    # Get detailed IP address information
    ip_details = get_ip_details(dns_result)
    print("\033[1;33m==================================================================================================\033[1;33m")
    print("\n\033[1;33mIP: \033[1;33m" + dns_result)
    if "Error" in ip_details:
        print(f"Error: {ip_details['Error']}")
    else:
        for key, value in ip_details.items():
            print(f"{key}: {value}")

    # Get email details if provided
    if email:
        email_details = get_email_details(email)
        print("\033[1;33m==================================================================================================\033[1;33m")
        print("\n\033[1;33mEmail: \033[1;33m" + email)
        if "Error" in email_details:
            print(f"Error: {email_details['Error']}")
        else:
            for key, value in email_details.items():
                print(f"{key}: {value}")

if __name__ == "__main__":
    ascii_banner = pyfiglet.figlet_format("Lets Find You!!")
    print(ascii_banner)
    target_domain = input("Enter the domain to footprint: ")
    footprinting(target_domain)
