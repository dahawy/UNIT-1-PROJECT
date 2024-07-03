from datetime import datetime, date
import uuid
import pickle
import os
import sys
import time
from IdGenerate import generateUniqueID,hashPassword,verifyPassword
from colorama import Fore, Back, Style
import getpass


class User:
    def __init__(self, userName:str, password:str, fullName:str, birthDate:str, email:str, mobile:str,role:bool = False):
        self.__userName = userName
        self.__password =  password
        self.fullName = fullName
        self.birthDate = birthDate
        self.email = email
        self.mobile = mobile 
        self.__role = role
    
    def getPassword(self):
        return self.__password
    
    def setPassword(self,password):
        self.__password = password

    def getUserName(self):
        return self.__userName
    
    def setUserName(self,username):
        self.__userName = username
    
    def getRole(self):
        return self.__role
    
    def setRole(self,newRole):
        self.__role = newRole
    
    def displayUserProfile(self):
        print(f"Username:      {self.getUserName()}")
        print(f"Full Name:     {self.fullName}")
        print(f"Date of Birth: {self.birthDate}")
        print(f"Email:         {self.email}")
        print(f"Mobile:        {self.mobile}")
        print(f"Role:          {'admin' if self.getRole() else 'user'}")


class Flight:
    # A constructor to initialize a flight info.
    def __init__(self, flightNumber, flightName, origin: str, destination: str, departureTime:datetime, arrivalTime:datetime, operationDays:list):
        self.flightNumber = flightNumber  # A unique identifier for each flight. 
        self.flightName = flightName
        self.origin = origin
        self.destination = destination
        self.departureTime = departureTime
        self.arrivalTime = arrivalTime
        self.operationDays = operationDays
        self.seats = {}

    # Display a flight details.
    def getFlightDetails(self):
        print(f"Flight Number: {self.flightNumber} - {self.flightName} - {self.origin} to {self.destination} - departure: {self.departureTime} - arrival: {self.arrivalTime} - Seats: {len(self.seats)}")
        
    
    def addSeatToFlight(self, seatNumber, price, available= True):
        if seatNumber in self.seats:
          print(f"Seat Number {seatNumber} already exists for Flight {self.flightNumber}.")
          return 
        self.seats[seatNumber] = Seat(seatNumber, price, available)

    def getAvailableSeats(self):
        return [seatNumber for seatNumber, seat in self.seats.items() if seat.available]
    
    def seatIsAvailable(self, seatNumber):
        if seatNumber in self.seats:
            return self.seats[seatNumber].available
        else:
            return False  # Seat does not exist in this flight

    def getBookedSeats(self):
        return [seatNumber for seatNumber, seat in self.seats.items() if not seat.available]


    def updateFlightDetails(): # Allows administrators to update flight details.
        pass

    def isOnDate(self, date):
        return self.departure_date == date

    def operatesFromTO(self, origin, destination):
        return self.origin == origin and self.destination == destination
    
    def book_seat(self, seat_id):
        if seat_id not in self.seats:
            print(f"Seat ID '{seat_id}' does not exist for Flight '{self.flight_id}'.")
            return False
        if not self.seats[seat_id]:
            print(f"Seat ID '{seat_id}' is already booked for Flight '{self.flight_id}'.")
            return False
        self.seats[seat_id] = False
        print(f"Seat ID '{seat_id}' successfully booked for Flight '{self.flight_id}'.")
        return True


class Seat:
    def __init__(self, seatNumber, price, available= True):
        self.seatNumber = seatNumber
        self.price = price
        self.available = available
        
        

    def bookSeat(self):
        if self.available:
            self.available = False
            return True
        else:
            return False

    def releaseSeat(self):
        self.available = True


class Passenger:
    # A Constructor to initialize a passenger info.
    def __init__(self, passengerID, name:str, birthDate:date):
        self.passengerSerial=  generateUniqueID() # Passenger's serial number.
        self.passengerID = passengerID
        self.name = name # Passenger's full name.
        self.birthDate = birthDate # P
        self.bookings = {} # Dictionary to store booked flights.

    
    # Updates passenger's info.
    def updatePassengerInfo(self, newInfo):
        pass


class Booking:
    # A constructor to initialize the booking system.
    def __init__(self, bookingID, flightNumber:str, bookingTime:datetime):
        self.bookingID = bookingID
        # ID of the passenger making the booking
        self.flightNumber = flightNumber  
        self.passengers = {}
        self.bookingTime = bookingTime  
        self.paymentStatus= "pending"

    def addPassenger(self, passengerID, seatNumber):
        self.passengers[passengerID] = seatNumber

    def getBookingDetails(self):
        print(f"booking ID: {self.bookingID}    Flight Number: {self.flightNumber}      Booking Time: {self.bookingTime}      paymet status: {self.paymentStatus}")

    def get_passenger_names(self):
        return [passenger.name for passenger in self.passengers.values()]

        

class FlightSystem:
    usersFile = "usersFile.pkl"
    flightsFile = "flightsFile.pkl"
    bookingsFile = "bookingsFile.pkl"
    passengersFile = "passengersFile.pkl"
     
    def __init__(self):
        self.flights = self.loadFromFile(FlightSystem.flightsFile) #Dictionary to hold Flight objects
        self.users = self.loadFromFile(FlightSystem.usersFile) #Dictionary to hold User objects
        self.bookings = self.loadFromFile(FlightSystem.bookingsFile) ##Dictionary to hold booking objects
        self.passengers = self.loadFromFile(FlightSystem.passengersFile)# Dictionary to hold Passenger objects
        self.currentUserName = None
        

    def register(self): # Allows users to create a new account.
        userName = input("Enter username: ")
        while userName in self.users:
            userName = input("Username taken! Try again: ")
            
        password = getpass.getpass("Enter password: ")
        fullName = input("Enter your full name: ")
        birthDate = input("Enter birthDate: ")
        email = input("Enter email: ")
        mobile = input("Enter mobile number: ")

        user = User(userName, hashPassword(password), fullName, birthDate, email, mobile)
         #store user in users dictionary
        self.users[user.getUserName()] = user
        # Saving user info to users file
        self.saveToFile(self.users,FlightSystem.usersFile)
        print(Fore.GREEN+"You have been registered successfully")
        print(Style.RESET_ALL)
        input("Press Enter to continue..")


    #Authenticates users based on username and hashed password.
    def login(self):
        if len(self.users) != 0: 
            for attempt in range(3):
                username = input(Fore.LIGHTGREEN_EX+"Enter username: ")
                password = getpass.getpass("Enter password: ")
                print(Style.RESET_ALL)
                
                if username in self.users and verifyPassword(password, self.users[username].getPassword()):
                    #self.clearTerminal()
                    self.printWelcomeMessage(Fore.LIGHTYELLOW_EX+self.users[username].fullName)
                    print(Style.RESET_ALL)
                    self.userRole = {username : self.users[username].getRole()}
                    self.currentUserName = username
                    return self.users[username].getRole()
                else:
                    print(Fore.RED+"Wrong username or password! Please try again.")
                    print(Style.RESET_ALL)
            print(Fore.RED+"You have exceeded the number of allowed attempts!")
            print(Style.RESET_ALL)
            input("Press Enter to continue..")
            return None
        else:
            print("Please register first.")
            input("Press Enter to continue..")


    # Display users profiles.
    def displayAllUsers(self):
        if len(self.users) != 0:
            print("-----------------------------------------------------------------------------------------------------------------")
            print("|                                        Users Registered In The System                                         |")
            print("-----------------------------------------------------------------------------------------------------------------")
            for i, userName in enumerate(self.users,start=1):
                user = self.users[userName]
                print(f"{i}- {user.getUserName()} - {user.fullName} - {user.email} - {'admin' if user.getRole() else 'user'}")
            print("")
        else:
            print("There are no users registered yet.")
        input("Press Enter to continue..")

    # Display a user profile by username.
    def displayUserByUserName(self):
        if len(self.users) != 0:
            username = input("Enter username: ")
            if username in self.users:
                user = self.users[username]
                print("-------------------------------------------------------------------------------------------------------------")
                print("|                                               User Profile                                                |")
                print("-------------------------------------------------------------------------------------------------------------")
                print(f"{user.getUserName()} - {user.fullName} - {user.email} - {'admin' if user.getRole() else 'user'}\n")
            else:
                print(f"The user: {username} does not exist!")
        else:
            print("There are no users registered yet.")
        input("Press Enter to continue..")

    # Display a user profile.
    def displayMyProfile(self):
        if len(self.users) != 0:
            username = self.currentUserName
            if username in self.users:
                user = self.users[username]
                print("----------------------------------------------------------------------------------------------------------")
                print("|                                              My Profile                                                |")
                print("----------------------------------------------------------------------------------------------------------")
                user.displayUserProfile()
            else:
                print(f"The user: {username} does not exist!")
        else:
            print("There are no users registered yet.")
        input("\nPress Enter to continue..")

    # Update user profile.
    def updateMyProfile(self, newUserName:str, newPassword:str, newFullName:str, newBirthDate:str, newEmail:str, newMobile:str):
        # Changing the dictionary key: "username" for the current user
        self.users[newUserName] = self.users.pop(self.currentUserName)
        if(newUserName): self.users[newUserName].setUserName(newUserName)
        if(newPassword): self.users[newUserName].setPassword(newPassword)
        if(newFullName): self.users[newUserName].fullName = newFullName
        if(newBirthDate): self.users[newUserName].birthDate = newBirthDate
        if(newEmail): self.users[newUserName].email = newEmail
        if(newMobile): self.users[newUserName].mobile = newMobile
        self.saveToFile(self.users,FlightSystem.usersFile)
        self.currentUserName = newUserName
        print(Fore.GREEN+"You profile has been updated successfully.")
        print(Style.RESET_ALL)
        input("Press Enter to continue..")


    # Allows admins to update a current user role.
    def changeRole(self):
        username = input("Enter the user username: ")
        if username in self.users:
            print(f"{username} current role is {'admin' if self.users[username].getRole() else 'user'}")
            answer = input(f"Are you sure you want to change role to {'user' if self.users[username].getRole() else 'admin'}? [Y/N]:")
            if answer.upper() == 'Y':
                newRole = not self.users[username].getRole()
                self.users[username].setRole(newRole)
                self.saveToFile(self.users,FlightSystem.usersFile)
                print(Fore.GREEN+"Role has been changed successfully")
                print(Style.RESET_ALL)
        else:
            print("The user doesn't exist in the system!")
        input("Press Enter to continue..")
        

    def dispalyBooking(self): # Retrieves a booking according to bookingID.
        bookingID= input("Enter booking ID: ")
        if bookingID in self.bookings:
            booking = self.bookings[bookingID]
            booking.getBookingDetails()
        input("\nPress Enter to continue..")

    # Adds a new flight to the system.
    def addFlight(self, flight:Flight): 
        self.flights[flight.flightNumber] = flight
        # Generate a list of 160 seats numbers (40 long - 4 width)
        seatsNumbersList = self.generateSeatsNumbers(3,4)
        price = float(input("Enter seat price: "))
        for seatNumber in seatsNumbersList:
            self.flights[flight.flightNumber].addSeatToFlight(seatNumber, price)
        self.saveToFile(self.flights,FlightSystem.flightsFile)
        print(f"Flight with number: {flight.flightNumber} has been added successfully.")
        input("\nPress Enter to continue..")


    # Handles booking process, updates flight seats and passenger bookings.
    def makeBooking(self, flightNumber, selectedPassengersSeats):
        if flightNumber in self.flights:
            flight = self.flights[flightNumber]
            bookingID = generateUniqueID()
            booking = Booking(bookingID, flightNumber, datetime.now())
            for passengerID, seatNumber in selectedPassengersSeats.items():
                    if flight.seatIsAvailable(seatNumber):
                        booking.addPassenger(passengerID, seatNumber)
                        flight.seats[seatNumber].available = False  # Book the seat
                    else:
                        print(f"Seat {seatNumber} is not available on flight {flight.flightNumber}")
            self.saveToFile(self.flights,FlightSystem.flightsFile)
            # Add booking to flightSystem bookings dictionary
            self.bookings[bookingID] = booking
            self.saveToFile(self.bookings,FlightSystem.bookingsFile)
            print(f"\nBooking with ID {bookingID} successfully made for {len(selectedPassengersSeats)} passengers.")
            input("\nPlease press Enter to proceed for payment..")
            cardNumber = input("Enter card Number: ")
            cvcCode = input("Enter CVC code: ")
            print(Fore.YELLOW+"Checking with your bank...")
            print(Style.RESET_ALL)
            time.sleep(3)
            print(Fore.GREEN+"Payment made successfully. Thank you for choosing YourSky.")
            print(Style.RESET_ALL)
            # Set payment status for the booking
            booking.paymentStatus = "paid"
            input("\nPress Enter to continue..")
        else:
            print(f"Flight {flightNumber} does not exist.")



    def searchFlights(self, origin, destination, date):
        day = self.getDayName(date)
        foundFlights = []
        for flightNumber, flight in self.flights.items():
            if flight.origin == origin and flight.destination == destination and day in flight.operationDays:
                foundFlights.append(flight)
        return foundFlights
    

    def cancelBooking(self, passengerId, flightNumber): # Cancels a booking for a specific passenger.
        pass

    
    def getPassengerBookings(self, passengerId): # Retrieves booking history for a passenger.
        pass

    def addPassenger(self, passengerid, name, birthDate):
        if passengerid not in self.passengers:
            self.passengers[passengerid] = Passenger(passengerid, name, birthDate)
            print(f"Passenger: {passengerid} - ({name}) added successfully.")
        else:
            print(f"Passenger {passengerid} already exists.")


    # Displays detailed information about a specific flight.
    def displayFlightDetails(self, flightNumber): 
        print("---------------------------------------------------------------------------------------------------------------------")
        print("|                                                Flight Details                                                     |")
        print("---------------------------------------------------------------------------------------------------------------------")
        if flightNumber in self.flights:
            flight = self.flights[flightNumber]
            flight.getFlightDetails()
            input("\nPress Enter to continue..")
        else:
            print(f"The flight does not exist.")
            input("\nPress Enter to continue..")
    
    # Displays detailed information about all flights.All Flights Added To The System 
    def displayAllFlights(self): 
        print("---------------------------------------------------------------------------------------------------------------------")
        print("|                                       All Flights Added To The System                                             |")
        print("---------------------------------------------------------------------------------------------------------------------")
        if not self.flights:
            print("No flights available.")
        else:
            for flightNumber, flight in self.flights.items():
                flight.getFlightDetails()
        input("\nPress Enter to continue..")

    # Takes either a date or a day code then convert either one to the coressponing day of the week.
    #  i.e:
    # 2024/12/1 --> Monday
    # or 1 --> Monday
    def getDayName(self,date_or_Daycode):
        try:
            if date_or_Daycode.isdigit() and 1 <= int(date_or_Daycode) <= 7:
                # Get day name based on code (1 for Monday, 2 for Tuesday, ..., 7 for Sunday)
                return date(2024, 1, int(date_or_Daycode)).strftime("%A")
            elif '/' in date_or_Daycode:
                # Parse the date string into a datetime.date object
                date_obj = datetime.strptime(date_or_Daycode, '%Y/%m/%d').date()
                # Get the day name corresponding to the date
                return date_obj.strftime("%A")
            else:
                return "Invalid input"
        
        except ValueError:
            return "Invalid input format"

    # Generate 160 seats numbers
    def generateSeatsNumbers(self,seatsLength, seatsWidth):
        seatsNumbers = []
        for i in range(1, seatsLength + 1):
            numberFormat = f"{i:02}"  # Ensure two-digit formatting the number part
            for j in range(seatsWidth):
                seatLetter = chr(65 + j)  # Convert index to corresponding letter (A, B, C, ...)
                seatNumber = f"{numberFormat}{seatLetter}"
                seatsNumbers.append(seatNumber)

        return seatsNumbers

    
    def printWelcomeMessage(self,username):
        welcome = '''
-----------------------------------------------------------------------------------------------------------------
|                                             WELCOME TO YOUR SKY                                               |
-----------------------------------------------------------------------------------------------------------------
'''
        print(Fore.YELLOW+welcome)
        print(Style.RESET_ALL)
        # Calculate the middle point for cursor positioning
        width = 119  # Adjust based on your terminal width
        middle_pos = (width - len(username)) // 2
        # Move cursor to the middle position
        sys.stdout.write(f"\033[{middle_pos}G")  # Move cursor to column 'middle_pos'
        sys.stdout.flush()
        # Print username letter by letter with delay
        for char in username:
            sys.stdout.write(char)
            sys.stdout.flush()
            time.sleep(0.15)  # Adjust pause time as needed
        # Move cursor to the next line after printing username
        input(Fore.CYAN+"\n\n\nPress Enter to continue..")
        print(Style.RESET_ALL)
        


    def clearTerminal(self):
         os.system('clear')

    def saveToFile(self,dictionary, filename: str):
        try:
             with open(filename, "wb") as file:
                pickle.dump(dictionary, file)
        except Exception as e:
            print(e)

    def loadFromFile(self, filename: str):
        try:
            if os.path.exists(filename) and os.stat(filename).st_size != 0:
                with open(filename, "rb") as file:
                    dictionary = pickle.load(file)
            else:
                dictionary = {}
        except Exception as e:
            print(e)
        return dictionary

