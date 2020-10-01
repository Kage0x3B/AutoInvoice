import json
import ntpath
import argparse
import ics

import invoice
import time_entry
from debitoor_client import DebitoorClient


class AutoInvoice:
    def __init__(self):
        self.auth_success = False
        self.auth_status = None
        self.auth_button = None
        self.file_info = None
        self.loaded_filename = None
        self.time_entries = []

        self.api_config = {
            "clientId": "",
            "clientSecret": ""
        }
        self.settings = {
            "accessToken": "",
            "serviceName": "Dienstleistung Entwicklung",
            "customerId": "5e97dcd2c223eb0023c58ada",
            "entriesPerInvoice": 10,
            "hourlyRate": 30.0
        }

        self.load_config()

        self.api_client = DebitoorClient(
            self.api_config["clientId"], self.api_config["clientSecret"])

        if self.settings["accessToken"]:
            try:
                self.api_client.use_access_token(self.settings["accessToken"])
                self.auth_success = True
                print("[+] You are authenticated")
            except:
                print("[-] You are not authenticated")
                pass

    def load_config(self):
        with open("api.json", "r") as f:
            self.api_config = json.load(f)

        with open("settings.json", "r") as f:
            self.settings = json.load(f)

    def save_settings(self):
        with open("settings.json", "w") as settings_file:
            settings_file.write(json.dumps(self.settings))

    def retrieve_access_token(self, parent):
        access_token = self.api_client.request_access_token(oauth_code)

        if access_token:
            self.settings["accessToken"] = access_token
            self.save_settings()

            self.auth_success = True
            self.auth_status.set("Authorized")

    def create_debitoor_auth(self, parent):

        def on_authorize_click():
            self.retrieve_access_token(parent)

        if self.auth_success:
            self.auth_status.set("Authorized")

    def read_file(self, filename, hourly_rate):
            if filename:
                with open(filename, "r") as ics_file:
                    c = ics.Calendar(ics_file.read())
                    print(c.todos)
                    print(ics_file)

                    name = "time list"

                    for extra in c.extra:
                        if str(extra).startswith("X-WR-CALNAME:"):
                            name = str(extra)[13:]

                    self.time_entries += time_entry.parse_work_times(c.todos, hourly_rate)

    def create(self):
        if len(self.time_entries) < 1:
                        return

        invoices=invoice.create_invoices(self.time_entries, self.settings)

        for inv in invoices:
            self.api_client.create_invoice_draft(inv)
            

if __name__ == '__main__':
    parser=argparse.ArgumentParser(description = 'Auto create invoices')
    parser.add_argument('-f','--file', action='append', help='<Required> Set flag', required=True)
    parser.add_argument('-r','--rate', action='append', help='<Required> Set flag', required=True)


    args=parser.parse_args()

    if (len(args.file) != len(args.rate)):
        print("Multiple -f tags need the same amount of -r (Rate) tags for each file")
    else:
        auto = AutoInvoice()
        for file,rate in zip(args.file, args.rate):
            auto.read_file(file, float(rate))

        auto.create()
            
