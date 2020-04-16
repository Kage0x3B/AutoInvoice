class InvoiceEntry:
    def __init__(self, name, date, hours, hourly_rate):
        self.name = name
        self.date = date
        self.hours = hours
        self.hourly_rate = hourly_rate

    def data(self):
        title = self.name + " - " + self.date

        return {
            "productName": title,
            "quantity": self.hours,
            "unitGrossPrice": self.hourly_rate
        }


def create_invoices(time_entries, settings):
    pass
