import pandas as pd
from datetime import datetime

# Load existing data from CSVs (for persistence)
rooms_df = pd.read_csv("rooms.csv", dtype=str)
guests_df = pd.read_csv("guests.csv", dtype=str)
reservations_df = pd.read_csv("reservations.csv", dtype=str)

# Room and Guest Management

class Room:
    def __init__(self, room_id, room_type, price, room_demand=0):
        self.room_id = room_id
        self.room_type = room_type
        self.price = price
        self.room_demand = room_demand  # For dynamic pricing

    def save(self):
        global rooms_df
        if self.room_id not in rooms_df['room_id'].values:
            new_room = pd.DataFrame({
                "room_id": [self.room_id],
                "room_type": [self.room_type],
                "price": [self.price],
                "status": ["available"],
                "room_demand": [self.room_demand]
            })
            rooms_df = pd.concat([rooms_df, new_room], ignore_index=True)
            rooms_df.to_csv("rooms.csv", index=False)
        else:
            print(f"Room {self.room_id} already exists in the system.")

    @staticmethod
    def list_rooms():
        global rooms_df
        return rooms_df

    @staticmethod
    def check_availability(room_id, booking_date):
        global rooms_df, reservations_df
        # Check if the room is available for the given date
        room = rooms_df.loc[rooms_df['room_id'] == room_id]
        if room['status'].values[0] != "available":
            return False

        # Check if the room is already booked for the given date
        conflict = reservations_df[reservations_df['room_id'] == room_id]
        if booking_date in conflict['booking_date'].values:
            print(f"Room {room_id} is already booked on {booking_date}.")
            return False
        return True

    @staticmethod
    def dynamic_pricing(room_id):
        global rooms_df
        room = rooms_df.loc[rooms_df['room_id'] == room_id]

        # Convert 'room_demand' to an integer for correct pricing calculation
        room_demand = int(room['room_demand'].values[0])  # Ensure room_demand is treated as an integer
        
        demand_multiplier = 1 + (room_demand * 0.1)  # Increase price by 10% per demand point
        return float(room['price'].values[0]) * demand_multiplier

# New Validation for Booking Date
def validate_booking_date(booking_date):
    try:
        # Check if the booking date is in the future
        booking_date_obj = datetime.strptime(booking_date, "%Y-%m-%d")
        if booking_date_obj < datetime.now():
            print("Error: Booking date cannot be in the past.")
            return False
        return True
    except ValueError:
        print("Error: Invalid date format. Please use YYYY-MM-DD format.")
        return False

class Guest:
    def __init__(self, name, contact_number, email, preferences=None, loyalty_program=False):
        self.name = name
        self.contact_number = contact_number
        self.email = email
        self.preferences = preferences if preferences else {}
        self.loyalty_program = loyalty_program

    def save(self):
        global guests_df
        # Check if email or phone number is already taken
        if self.email in guests_df['email'].values:
            print(f"Error: The email {self.email} is already in use.")
            return False
        if self.contact_number in guests_df['contact_number'].values:
            print(f"Error: The contact number {self.contact_number} is already in use.")
            return False

        new_guest = pd.DataFrame({
            "name": [self.name],
            "contact_number": [self.contact_number],
            "email": [self.email],
            "preferences": [str(self.preferences)],
            "loyalty_program": [self.loyalty_program]
        })
        guests_df = pd.concat([guests_df, new_guest], ignore_index=True)
        guests_df.to_csv("guests.csv", index=False)
        return True

class Reservation:
    def __init__(self, guest, room, booking_date):
        self.guest = guest
        self.room = room
        self.booking_date = booking_date

    def save(self):
        global rooms_df, reservations_df

        # Check if overbooking occurs
        if not Room.check_availability(self.room.room_id, self.booking_date):
            print("Reservation failed due to overbooking conflict.")
            return

        # Save reservation details to the reservations CSV
        reservation_data = pd.DataFrame({
            "guest_name": [self.guest.name],
            "room_id": [self.room.room_id],
            "booking_date": [self.booking_date]
        })
        rooms_df.loc[rooms_df['room_id'] == self.room.room_id, 'status'] = "booked"
        rooms_df.to_csv("rooms.csv", index=False)

        reservations_df = pd.concat([reservations_df, reservation_data], ignore_index=True)
        reservations_df.to_csv("reservations.csv", index=False)

        print(f"Reservation for {self.guest.name} confirmed for room {self.room.room_id} on {self.booking_date}.")

        bill = Billing(reservation=self, payment_method="credit card", amount_paid=self.room.price, advance_payment=True)
        bill.generate_invoice()
        bill.process_payment()

# Billing System
class Billing:
    def __init__(self, reservation, payment_method, amount_paid, advance_payment=False):
        self.reservation = reservation
        self.payment_method = payment_method
        self.amount_paid = amount_paid
        self.advance_payment = advance_payment

    def generate_invoice(self):
        invoice = f"""
        Hotel Invoice
        -------------------------
        Guest: {self.reservation.guest.name}
        Room ID: {self.reservation.room.room_id}
        Booking Date: {self.reservation.booking_date}
        Amount: {self.reservation.room.price}
        Payment Method: {self.payment_method}
        Amount Paid: {self.amount_paid}
        Advance Payment: {self.advance_payment}
        -------------------------
        Thank you for choosing our hotel!
        """
        print(invoice)
        return invoice

    def process_payment(self):
        print(f"Payment of {self.amount_paid} processed using {self.payment_method}.")

# Function to Reserve a Room
def reserve_room():
    # Collect guest information
    name = input("Enter your name: ")
    contact_number = input("Enter your contact number: ")
    email = input("Enter your email address: ")
    preferences = input("Enter any preferences (e.g., king bed, ocean view): ")
    loyalty_program = input("Are you a loyalty program member? (yes/no): ").lower() == 'yes'

    guest = Guest(name=name, contact_number=contact_number, email=email, preferences=preferences, loyalty_program=loyalty_program)
    if not guest.save():
        return  # Stop execution if validation fails

    # List available rooms
    available_rooms = rooms_df[rooms_df['status'] == "available"]
    if available_rooms.empty:
        print("Sorry, no rooms are available.")
        return

    print("\nAvailable Rooms:")
    print(available_rooms[['room_id', 'room_type', 'price']])

    # Choose a room to book
    room_id = input("Enter the room_id you want to book: ")
    booking_date = input("Enter your booking date (YYYY-MM-DD): ")

    # Validate the booking date
    if not validate_booking_date(booking_date):
        return  # Stop execution if date validation fails

    if not Room.check_availability(room_id, booking_date):
        return  # Stop execution if room is not available for the given date

    # Dynamic pricing based on room demand
    room = Room(room_id=room_id, room_type=available_rooms.loc[available_rooms['room_id'] == room_id, 'room_type'].values[0],
                price=available_rooms.loc[available_rooms['room_id'] == room_id, 'price'].values[0])
    room.price = Room.dynamic_pricing(room_id)

    reservation = Reservation(guest=guest, room=room, booking_date=booking_date)
    reservation.save()

# Main System Workflow

def main():
    reserve_room()

if __name__ == "__main__":
    main()
