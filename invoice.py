import time_entry


class Invoice:
    def __init__(self, customer_id, entries):
        self.customer_id = customer_id
        self.entries = entries

    def data(self):
        lines = []

        for entry in self.entries:
            lines.append(entry.data())

        return {
            "customerId": self.customer_id,
            "lines": lines
        }


class InvoiceEntry:
    def __init__(self, name, date, hours, hourly_rate):
        self.name = name
        self.date = date
        self.hours = hours
        self.hourly_rate = hourly_rate
        self.unit_type = 1  # 1 for hours

    def data(self):
        return {
            "productName": self.name,
            "description": self.date.format("DD.MM.YYYY"),
            "quantity": float("{:10.2f}".format(self.hours)),
            #"unitGrossPrice": float("{:10.2f}".format(self.hourly_rate)),
            "unitNetPrice": float("{:10.2f}".format(self.hourly_rate)),
            "unitId": self.unit_type,
            "taxEnabled": True,
            "taxRate": 16
        }


def create_invoice(time_entries, settings):
    invoice_entries = []

    for entry in time_entries:
        invoice_entries.append(
            InvoiceEntry(settings["serviceName"], entry.date, entry.duration, entry.hourly_rate))

    return Invoice(settings["customerId"], invoice_entries)


def create_invoices(time_entries, settings):
    sorted_time_entries = {}

    for entry in time_entries:
        month = entry.date.month

        if month not in sorted_time_entries:
            sorted_time_entries.update({month: []})

        sorted_time_entries[month].append(entry)

    invoices = []

    def sort_time_entries(value):
        return value.date

    for month_key in sorted_time_entries:
        sorted_time_entries[month_key].sort(key=sort_time_entries)
        invoices.append(create_invoice(sorted_time_entries[month_key], settings))

    for inv in invoices:
        print(inv.data())

    return invoices
