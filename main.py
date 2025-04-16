import pandas as pd

# Load existing data from CSVs (for persistence)
rooms_df = pd.read_csv("rooms.csv", dtype=str)
guests_df = pd.read_csv("guests.csv", dtype=str)
reservations_df = pd.read_csv("reservations.csv", dtype=str)

# Room and Guest Management

class Room:
    def __init__(self, room_id, room_type, price):
        self.room_id = room_id
        self.room_type = room_type
        self.price = price

    def save(self):
        # Declare global for rooms_df
        global rooms_df
        # Save room details to the CSV (avoid duplicates)
        if self.room_id not in rooms_df['room_id'].values:
            new_room = pd.DataFrame({
                "room_id": [self.room_id],
                "room_type": [self.room_type],
                "price": [self.price],
                "status": ["available"]
            })
            rooms_df = pd.concat([rooms_df, new_room], ignore_index=True)
            rooms_df.to_csv("rooms.csv", index=False)
        else:
            print(f"Room {self.room_id} already exists in the system.")

    @staticmethod
    def list_rooms():
        # Declare global for rooms_df
        global rooms_df
        return rooms_df

    @staticmethod
    def check_availability(room_id):
        global rooms_df
        # Check if the room is available
        room = rooms_df.loc[rooms_df['room_id'] == room_id]
        if room['status'].values[0] == "available":
            return True
        else:
            return False

class Guest:
    def __init__(self, name, contact_number, email):
        self.name = name
        self.contact_number = contact_number
        self.email = email

    def save(self):
        # Declare global for guests_df
        global guests_df
        # Save guest details to the CSV
        new_guest = pd.DataFrame({
            "name": [self.name],
            "contact_number": [self.contact_number],
            "email": [self.email]
        })
        guests_df = pd.concat([guests_df, new_guest], ignore_index=True)
        guests_df.to_csv("guests.csv", index=False)

class Reservation:
    def __init__(self, guest, room, booking_date):
        self.guest = guest
        self.room = room
        self.booking_date = booking_date

    def save(self):
        # Declare global for rooms_df and reservations_df
        global rooms_df, reservations_df
        # Save reservation details to the reservations CSV
        reservation_data = pd.DataFrame({
            "guest_name": [self.guest.name],
            "room_id": [self.room.room_id],
            "booking_date": [self.booking_date]
        })
        rooms_df.loc[rooms_df['room_id'] == self.room.room_id, 'status'] = "booked"
        rooms_df.to_csv("rooms.csv", index=False)

        # Save to reservations.csv
        reservations_df = pd.concat([reservations_df, reservation_data], ignore_index=True)
        reservations_df.to_csv("reservations.csv", index=False)

        print(f"Reservation for {self.guest.name} confirmed for room {self.room.room_id} on {self.booking_date}.")

# Check-In/Check-Out Management

class CheckInOut:
    @staticmethod
    def check_in(reservation):
        global rooms_df
        # Mark the room as 'occupied'
        rooms_df.loc[rooms_df['room_id'] == reservation.room.room_id, 'status'] = "occupied"
        rooms_df.to_csv("rooms.csv", index=False)
        print(f"Checked in {reservation.guest.name} to room {reservation.room.room_id}.")

    @staticmethod
    def check_out(reservation):
        global rooms_df
        # Mark the room as 'available' again
        rooms_df.loc[rooms_df['room_id'] == reservation.room.room_id, 'status'] = "available"
        rooms_df.to_csv("rooms.csv", index=False)
        print(f"Checked out {reservation.guest.name} from room {reservation.room.room_id}.")

# Basic Billing System

class Billing:
    def __init__(self, reservation, payment_method, amount_paid):
        self.reservation = reservation
        self.payment_method = payment_method
        self.amount_paid = amount_paid

    def generate_invoice(self):
        # Generate the invoice
        invoice = f"""
        Hotel Invoice
        -------------------------
        Guest: {self.reservation.guest.name}
        Room ID: {self.reservation.room.room_id}
        Booking Date: {self.reservation.booking_date}
        Amount: {self.reservation.room.price}
        Payment Method: {self.payment_method}
        Amount Paid: {self.amount_paid}
        -------------------------
        Thank you for choosing our hotel!
        """
        print(invoice)
        return invoice

    def process_payment(self):
        # Process payment (This could be more complex with a payment gateway integration)
        print(f"Payment of {self.amount_paid} processed using {self.payment_method}.")

# Room Management (Cleaning, Maintenance, and Availability)

class RoomManagement:
    @staticmethod
    def mark_as_clean(room_id):
        global rooms_df
        rooms_df.loc[rooms_df['room_id'] == room_id, 'status'] = "clean"
        rooms_df.to_csv("rooms.csv", index=False)
        print(f"Room {room_id} marked as clean.")

    @staticmethod
    def mark_as_under_maintenance(room_id):
        global rooms_df
        rooms_df.loc[rooms_df['room_id'] == room_id, 'status'] = "under maintenance"
        rooms_df.to_csv("rooms.csv", index=False)
        print(f"Room {room_id} marked as under maintenance.")

# Function to Reserve a Room
def reserve_room():
    # Collect guest information
    name = input("Enter your name: ")
    contact_number = input("Enter your contact number: ")
    email = input("Enter your email address: ")

    guest = Guest(name=name, contact_number=contact_number, email=email)
    guest.save()

    # List available rooms
    available_rooms = rooms_df[rooms_df['status'] == "available"]
    if available_rooms.empty:
        print("Sorry, no rooms are available.")
        return

    print("\nAvailable Rooms:")
    print(available_rooms[['room_id', 'room_type', 'price']])

    # Choose a room to book
    room_id = input("Enter the room_id you want to book: ")
    if not Room.check_availability(room_id):
        print("The selected room is not available. Please try again.")
        return

    # Select a booking date
    booking_date = input("Enter your booking date (YYYY-MM-DD): ")

    # Create reservation
    selected_room = Room(room_id=room_id, room_type=available_rooms.loc[available_rooms['room_id'] == room_id, 'room_type'].values[0], 
                         price=available_rooms.loc[available_rooms['room_id'] == room_id, 'price'].values[0])
    
    reservation = Reservation(guest=guest, room=selected_room, booking_date=booking_date)
    reservation.save()

# Main System Workflow

def main():
    # Reserve a room for the guest
    reserve_room()

    # Get the reservation and check-in
    guest = guests_df.iloc[-1]  # Get the most recently added guest
    room = rooms_df.loc[rooms_df['status'] == "booked"].iloc[0]  # Get the most recently booked room
    reservation1 = Reservation(guest=Guest(name=guest['name'], contact_number=guest['contact_number'], email=guest['email']),
                               room=Room(room_id=room['room_id'], room_type=room['room_type'], price=room['price']),
                               booking_date="2025-03-27")

    check_in = CheckInOut()
    check_in.check_in(reservation1)

    # Generate the bill
    bill1 = Billing(reservation1, payment_method="credit card", amount_paid="100")
    bill1.generate_invoice()
    bill1.process_payment()

    # Mark room 101 as clean and under maintenance
    RoomManagement.mark_as_clean("101")
    RoomManagement.mark_as_under_maintenance("101")

    # Check-out guest1
    check_in.check_out(reservation1)

if __name__ == "__main__":
    main()
