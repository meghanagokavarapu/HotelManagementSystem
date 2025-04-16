<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Hotel Management System README</title>
</head>
<body>
    <h1>Hotel Management System</h1>

    <h2>Overview</h2>
    <p>This Hotel Management System allows you to manage room reservations, guest information, check-ins/check-outs, room availability, and billing. It also handles the maintenance of room statuses (available, booked, occupied, clean, and under maintenance).</p>

    <h2>Features</h2>

    <h3>1. Room Management</h3>
    <ul>
        <li><strong>Add Room</strong>: Rooms are added to the system with unique <code>room_id</code>, <code>room_type</code>, and <code>price</code>. Rooms can be marked as available, booked, occupied, clean, or under maintenance.</li>
        <li><strong>Check Room Availability</strong>: You can check whether a room is available for booking based on its status.</li>
    </ul>

    <h3>2. Guest Management</h3>
    <ul>
        <li><strong>Add Guest</strong>: Guests can be added to the system with their <code>name</code>, <code>contact_number</code>, and <code>email</code>.</li>
    </ul>

    <h3>3. Reservation Management</h3>
    <ul>
        <li><strong>Reserve Room</strong>: Guests can reserve rooms by selecting an available room and providing a booking date.</li>
        <li><strong>View Available Rooms</strong>: Available rooms are listed, and guests can choose the room they wish to book.</li>
        <li><strong>Room Booking Status</strong>: Rooms are marked as "booked" once reserved, and their status is updated.</li>
    </ul>

    <h3>4. Check-In and Check-Out</h3>
    <ul>
        <li><strong>Check-In</strong>: Rooms are marked as "occupied" once a guest checks in.</li>
        <li><strong>Check-Out</strong>: Rooms are marked as "available" once a guest checks out.</li>
    </ul>

    <h3>5. Billing System</h3>
    <ul>
        <li><strong>Generate Invoice</strong>: An invoice is created for the guest reservation, showing booking details and payment information.</li>
        <li><strong>Process Payment</strong>: Payments are processed using a specified payment method (e.g., credit card).</li>
    </ul>

    <h3>6. Room Management (Cleaning & Maintenance)</h3>
    <ul>
        <li><strong>Mark Room as Clean</strong>: Rooms can be marked as clean when ready for new guests.</li>
        <li><strong>Mark Room as Under Maintenance</strong>: Rooms can be marked as under maintenance if repairs or other work is required.</li>
    </ul>

    <h2>Files</h2>
    <ul>
        <li><strong>rooms.csv</strong>: Stores information about all the rooms (<code>room_id</code>, <code>room_type</code>, <code>price</code>, <code>status</code>).</li>
        <li><strong>guests.csv</strong>: Stores information about all the guests (<code>name</code>, <code>contact_number</code>, <code>email</code>).</li>
        <li><strong>reservations.csv</strong>: Stores information about all the reservations (<code>guest_name</code>, <code>room_id</code>, <code>booking_date</code>).</li>
    </ul>

    <h2>Classes</h2>
    <ul>
        <li><strong>Room</strong>: Represents a room, provides methods for saving, listing, and checking availability.</li>
        <li><strong>Guest</strong>: Represents a guest, provides methods for saving guest information.</li>
        <li><strong>Reservation</strong>: Represents a reservation, allows saving reservation details.</li>
        <li><strong>CheckInOut</strong>: Manages the check-in and check-out process.</li>
        <li><strong>Billing</strong>: Manages invoice generation and payment processing.</li>
        <li><strong>RoomManagement</strong>: Handles room cleaning and maintenance status.</li>
    </ul>

    <h2>Example Workflow</h2>
    <ol>
        <li>A guest provides their information (name, contact, email).</li>
        <li>Available rooms are displayed, and the guest selects a room to book.</li>
        <li>The room's status is updated to "booked", and the reservation is saved.</li>
        <li>The guest checks in, marking the room as "occupied".</li>
        <li>An invoice is generated for the booking and payment is processed.</li>
        <li>The room is marked as clean or under maintenance as required.</li>
        <li>Finally, the guest checks out, and the room becomes available again.</li>
    </ol>

    <h2>Requirements</h2>
    <ul>
        <li>Python 3.x</li>
        <li>Pandas library (<code>pip install pandas</code>)</li>
    </ul>

    <h2>Usage</h2>
    <p>To run the system:</p>
    <ol>
        <li>Ensure the <code>rooms.csv</code>, <code>guests.csv</code>, and <code>reservations.csv</code> files are in the same directory as the script.</li>
        <li>Run the script <code>main.py</code>:</li>
        <pre><code>python main.py</code></pre>
    </ol>

    <h2>License</h2>
    <p>This software is provided under the MIT License.</p>

</body>
</html>
