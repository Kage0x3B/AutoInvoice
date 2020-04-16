import json
import ntpath
import tkinter
from tkinter import filedialog, simpledialog
import time_entry

import ics

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
            "serviceName": "Unverpackt Website Entwicklung",
            "entriesPerInvoice": 10
        }

        self.load_config()

        self.api_client = DebitoorClient(self.api_config["clientId"], self.api_config["clientSecret"])

        if self.settings["accessToken"]:
            try:
                self.api_client.use_access_token(self.settings["accessToken"])
                self.auth_success = True
            except:
                pass

        root = tkinter.Tk()

        self.create_debitoor_auth(root)
        self.create_ics_file_select(root)

        root.mainloop()

    def load_config(self):
        with open("api.json", "r") as f:
            self.api_config = json.load(f)

        with open("settings.json", "r") as f:
            self.settings = json.load(f)

    def save_settings(self):
        with open("settings.json", "w") as settings_file:
            settings_file.write(json.dumps(self.settings))

    def retrieve_access_token(self, parent):
        self.api_client.open_oauth_page()
        oauth_code = simpledialog.askstring("Authorize AutoInvoice", "Authentication code: ")
        access_token = self.api_client.request_access_token(oauth_code)

        if access_token:
            self.settings["accessToken"] = access_token
            self.save_settings()

            self.auth_success = True
            self.auth_status.set("Authorized")
            self.auth_button["state"] = tkinter.DISABLED

    def show_ics_file_dialog(self, parent):
        ics_filename = filedialog.askopenfilename(parent=parent, initialdir=".", title="Select exported iCalendar file",
                                                  filetypes=(("iCalendar files", "*.ics"), ("All files", "*.*")))

        if ics_filename:
            with open(ics_filename, "r") as ics_file:
                c = ics.Calendar(ics_file.read())
            print(c.todos)
            print(ics_file)

            name = "time list"

            for extra in c.extra:
                if str(extra).startswith("X-WR-CALNAME:"):
                    name = str(extra)[13:]

            self.loaded_filename.set(ntpath.basename(ics_filename))
            self.file_info.set("Loaded " + name + " with " + str(len(c.todos)) + " entries")

            self.time_entries = time_entry.parse_work_times(c.todos)

    def create_debitoor_auth(self, parent):
        self.auth_status = tkinter.StringVar(parent, "Debitoor access pending...")

        def on_authorize_click():
            self.retrieve_access_token(parent)

        frame = tkinter.Frame(parent)
        frame.pack(fill=tkinter.X, padx=5, pady=5)

        auth_info = tkinter.Label(frame, textvariable=self.auth_status)
        auth_info.pack(side=tkinter.TOP)

        self.auth_button = tkinter.Button(frame, text="Authorize", command=on_authorize_click)

        if self.auth_success:
            self.auth_status.set("Authorized")
            self.auth_button["state"] = tkinter.DISABLED

        self.auth_button.pack(side=tkinter.BOTTOM)

    def create_ics_file_select(self, parent):
        self.file_info = tkinter.StringVar(parent, "No file loaded")
        self.loaded_filename = tkinter.StringVar(parent, "")

        def on_open_click():
            self.show_ics_file_dialog(parent)

        frame = tkinter.Frame(parent)
        frame.pack(fill=tkinter.X, padx=5, pady=5)
        top_frame = tkinter.Frame(frame)
        top_frame.pack(side=tkinter.TOP)

        ics_file_entry = tkinter.Entry(top_frame, state=tkinter.DISABLED, textvariable=self.loaded_filename)
        ics_file_entry.pack(side=tkinter.LEFT, padx=5)
        ics_file_dialog_button = tkinter.Button(top_frame, text="Open file", command=on_open_click)
        ics_file_dialog_button.pack(side=tkinter.RIGHT)
        ics_file_info = tkinter.Label(frame, textvariable=self.file_info)
        ics_file_info.pack(side=tkinter.BOTTOM)


if __name__ == '__main__':
    AutoInvoice()
