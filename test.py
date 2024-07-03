import sys
from datetime import datetime,date
import time
import os
from flightBooking import FlightSystem,Seat,Passenger,Booking


# selectedPassengersSeats={"123":"1111","332":"222"}

# for passengerID, seatNumber in selectedPassengersSeats.items():
#     print(passengerID,seatNumber)

fs = FlightSystem()
#for bookingID, booking in fs.bookings.items():
    #print(bookingID, booking.flightNumber,booking.bookingTime)
    #print((booking.passengers).get(passengerID))
    #print((booking.passengers).keys().name)
if 'BF402322'in fs.bookings:
    if fs.passengers in (fs.bookings['BF402322'].passengers.keys()):
        print("good")
    #     print(passengerid)fs.bookings['BF402322'])
