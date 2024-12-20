class Event:
    def __init__(self, name, payload):
        self.name = name
        self.payload = payload

class EmbassyAppointmentRequestEvent(Event):
    def __init__(self, passport_number, date):
        super().__init__("embassy_appointment_request", {"passport_number": passport_number, "date": date})

class AppointmentConfirmationEvent(Event):
    def __init__(self, passport_number, is_confirmed):
        super().__init__("appointment_confirmation", {"passport_number": passport_number, "is_confirmed": is_confirmed})

class VisaRequestEvent(Event):
    def __init__(self, student_details, period):
        super().__init__("visa_request", {"student_details": student_details, "period": period})

# Event queue
event_queue = []

class Student:
    def __init__(self, first_name, last_name, day_of_birth, address, phone_number, passport_number):
        self.first_name = first_name
        self.last_name = last_name
        self.day_birth = day_of_birth
        self.address = address
        self.phone_number = phone_number
        self.passport_number = passport_number

    def ask_for_embassy_appointment(self, date):
        event = EmbassyAppointmentRequestEvent(self.passport_number, date)
        event_queue.append(event)
        print('Event', event.name, 'emitted!')

    def submit_visa_request(self, period):
        student_details = {
            "first_name": self.first_name,
            "last_name": self.last_name,
            "day_of_birth": self.day_birth,
            "address": self.address,
            "phone_number": self.phone_number,
            "passport_number": self.passport_number
        }
        event = VisaRequestEvent(student_details, period)
        event_queue.append(event)
        print('Event', event.name, 'emitted!')

class Embassy:
    def __init__(self, name, address, phone_number, email):
        self.name = name
        self.address = address
        self.phone_number = phone_number
        self.email = email

    def handle_appointment_request(self, event):
        print(f"Received appointment request for Passport: {event.payload['passport_number']} on {event.payload['date']}")
        confirmation_event = AppointmentConfirmationEvent(event.payload["passport_number"], is_confirmed=True)
        event_queue.append(confirmation_event)
        print('Event', confirmation_event.name, 'emitted!')

    def handle_visa_request(self, event):
        student_details = event.payload['student_details']
        period = event.payload['period']
        print(f"Received visa request for {student_details['first_name']} {student_details['last_name']} \n"
              f"Passport: {student_details['passport_number']} \n"
              f"Period: {period}")

# Event loop
def event_loop():
    while event_queue:
        current_event = event_queue.pop(0)
        
        if isinstance(current_event, EmbassyAppointmentRequestEvent):
            polish_embassy.handle_appointment_request(current_event)
        elif isinstance(current_event, AppointmentConfirmationEvent):
            print(f"Confirmation for Passport: {current_event.payload['passport_number']} - Confirmed: {current_event.payload['is_confirmed']}")
        elif isinstance(current_event, VisaRequestEvent):
            polish_embassy.handle_visa_request(current_event)

# Example Usage
peter1 = Student("Piotr1", "Brudny", '1.02.1984', 'Ankara', '5435345345', 'ED4234323')
peter2 = Student("Piotr2", "Brudny", '2.02.1994', 'Ankara', '5435345345', 'ED41423')
peter3 = Student("Piotr3", "Brudny", '4.02.1984', 'Ankara', '54353fds45345', 'ED42723')

peter1.ask_for_embassy_appointment('10.12.2024')
peter2.ask_for_embassy_appointment('11.12.2024')
peter3.ask_for_embassy_appointment('10.12.2024')

peter1.submit_visa_request('6 months')
peter2.submit_visa_request('1 year')
peter3.submit_visa_request('3 months')

polish_embassy = Embassy('Polish Embassy', 'Ankara, Harika 10', '343242344', 'polishembassy@gov.tr')

event_loop()
