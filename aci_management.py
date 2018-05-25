#!/usr/bin/env python

"""aci_management.py: Manage Cisco ACI."""

import argparse
import json
import requests
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

__author__ = "Larry Smith Jr."
__email___ = "mrlesmithjr@gmail.com"
__maintainer__ = "Larry Smith Jr."
__status__ = "Development"
# http://everythingshouldbevirtual.com
# @mrlesmithjr


def create_credentials(apic_user, apic_password):
    """Create credentials structure."""
    creds_structure = {"aaaUser": {"attributes": {
        "name": apic_user, "pwd": apic_password}}}
    return json.dumps(creds_structure)


def decide_action(apic_url, session, args):
    """Decide action to take."""
    if args.action == "get_tenants":
        get_tenants(apic_url, session)
    if args.action == "get_tenants_complete_info":
        get_tenants_complete_info(apic_url, session)


def get_tenants_complete_info(apic_url, session):
    """Get tenants."""
    get_response = session.get(
        apic_url + "class/fvTenant.json?query-target=subtree", verify=False)
    tenants = json.loads(get_response.text)
    print(json.dumps(tenants, indent=4))


def get_tenants(apic_url, session):
    """Get tenants."""
    get_response = session.get(apic_url + "class/fvTenant.json", verify=False)
    tenants = json.loads(get_response.text)
    print(json.dumps(tenants, indent=4))


def login(apic_url, session, json_credentials):
    """Login to APIC."""
    login_url = apic_url + "aaaLogin.json"
    post_response = session.post(
        login_url, data=json_credentials, verify=False)
    return session, post_response


def main():
    """Main function."""
    args = parse_args()
    apic_url = args.apicUrl + "/api/"
    apic_user = args.apicUser
    apic_password = args.apicPassword
    session = requests.Session()
    credentials = create_credentials(apic_user, apic_password)
    session, response = login(apic_url, session, credentials)
    if response.status_code == 200:
        decide_action(apic_url, session, args)


def parse_args():
    """Parse CLI arguments."""
    parser = argparse.ArgumentParser(description="Manage Cisco ACI.")
    parser.add_argument("action", help="Define action to take", choices=[
        "get_tenants_complete_info", "get_tenants"])
    parser.add_argument(
        "--apicPassword", help="APIC Password", default="ciscopsdt")
    parser.add_argument("--apicUrl", help="APIC Url",
                        default="https://sandboxapicdc.cisco.com")
    parser.add_argument("--apicUser", help="APIC User", default="admin")
    args = parser.parse_args()
    return args


if __name__ == "__main__":
    main()
