from flightBooking import User, Passenger, Flight, Booking,FlightSystem
from IdGenerate import generateUniqueID
from colorama import Fore, Back, Style

# CLI interface of YourSky system
flightSystem = FlightSystem()

def adminMenu(flightSystem:FlightSystem):    
    while True:
        #flightSystem.clearTerminal()
        menu = '''
-----------------------------------------------------------------------------------------------------------------
|                                               Admin Dashboard                                                 |
-----------------------------------------------------------------------------------------------------------------
           
A:  Add a flight                  S:   Search for flights                  DP: Display my Profile
B:  Book a flight                 C:   Cancel booking                      UP: Update my Profile 
DB: Display Booking               DAF: Display All Flights info            DU: Display user profile by username
DF: Display Flight info           DAU: Display All Users info              CR: Change Role of user
E:  Exit                                                                
    
Choice: 
'''
        choice = input(Fore.LIGHTCYAN_EX+menu)
        print(Style.RESET_ALL)
        # Add a new flight to YourSky             
        if choice.upper() == 'A':
            flightNumber = generateUniqueID()
            if flightNumber in flightSystem.flights:
                print(f"Flight Number {flightNumber} already exists.")
                return
            flightName = input("Enter flight name: ")
            origin = input("Enter departure airport name: ")
            destination = input("Enter arrival airport name: ")
            departureTime = input("Enter departure time: ")
            arrivalTime = input("Enter arrival time: ")
            # store operation days for the flight
            operationDays = []
            operationDay = input("Enter operation day [1 for Monday or 2 for Tuesday,..etc: ")
            while operationDay.upper() != "":
                operationDays.append(flightSystem.getDayName(operationDay))
                operationDay = input("Enter another operation day or press Enter to finish: ")
            
            flight = Flight(flightNumber, flightName, origin, destination, departureTime, arrivalTime,operationDays)
            flightSystem.addFlight(flight)

        elif choice.upper() == 'S':
            # Search for flights
            origin = input("Enter departure city: ")
            destination = input("Enter arrival city: ")
            date = input("Enter date (YYYY/MM/DD): ")
            foundFlights = flightSystem.searchFlights(origin, destination, date)
            if len(foundFlights) != 0:
                for flight in foundFlights:
                    flight.getFlightDetails()
                input("Press Enter to continue..")
            else:
                print("Unfortunately, no flights available. Please try another date.")
                input("\nPress Enter to continue..")

        elif choice.upper() == 'B':
            # Book a flight
            selectedPassengersSeats = {}
            flightNumber = input("Enter flight number you want to book: ")
            if flightNumber in flightSystem.flights:
                flight = flightSystem.flights[flightNumber]
                seats = flight.getAvailableSeats()
                while True:
                    passengerID = input("Enter passenger ID: ")
                    name = input("Enter passenger full name: ")
                    birthDate = input("Enter passenger birthDate: ")
                    input("Press Enter to proceed for seat selection..")
                    print(seats)
                    seatNumber = input("Please choose passenger seat number: ").upper()
                    while seatNumber.upper() not in seats:
                        seatNumber = input("This seat is not available. Please choose another one: ").upper()

                    selectedPassengersSeats[passengerID] = seatNumber.upper()
                    passenger = Passenger(passengerID, name, birthDate)
                    flightSystem.passengers[passengerID]={"name":name, "birthDate":birthDate}
                    flightSystem.saveToFile(flightSystem.passengers,FlightSystem.passengersFile)
                    print("passenger allocated a seat successfully")
                    choice = input("Do you want to add another passenger? [Y/N]: ")
                    if choice.upper() == "N":
                        break
                    seats.remove(seatNumber.upper())
                flightSystem.makeBooking(flightNumber, selectedPassengersSeats)
            else:
                print("This flight does not exist")
                input("\nPress Enter to continue..")
            
    
        elif choice.upper() == 'DB':
            # Display passenger booking confirmation
            flightSystem.dispalyBooking()
            
        elif choice.upper() == 'C':
            # Cancel booking
            passengerId = input("Enter your passenger ID: ")
            flightNumber = input("Enter flight number to cancel booking: ")
            flightSystem.cancel_booking(passengerId, flightNumber)

        elif choice.upper() == 'DF':
            # Display flight details
            flightNumber = input("Enter flight number: ")
            flightSystem.displayFlightDetails(flightNumber)
        
        elif choice.upper() == 'DAF':
            # Display all flights details
            flightSystem.displayAllFlights()

        elif choice.upper() == 'R':
            # Register a user
            flightSystem.register()

        elif choice.upper() == 'L':
            # Login a user
            flightSystem.login()
        
        elif choice.upper() == 'DU':
            # Display a user profile
            flightSystem.displayUserByUserName()
        
        elif choice.upper() == 'DP':
            # Display a user profile
            flightSystem.displayMyProfile()

        elif choice.upper() == 'UP':
            # Update user profile]
            newUserName = input("Enter new username: ")
            while (newUserName in flightSystem.users and newUserName != flightSystem.currentUserName):
                newUserName = input("Username taken! Try again: ")

            newPassword = input("Enter new password: ")
            newFullName = input("Enter new fullName: ")
            newBirthDate = input("Enter new birthDate: ")
            newEmail = input("Enter new email: ")
            newMobile = input("Enter new mobile: ")
            try:
                flightSystem.updateMyProfile(newUserName,newPassword,newFullName,newBirthDate,newEmail,newMobile)
                #print(Fore.GREEN+"User Profile has been updated successfully.")
            except Exception as e:
                print(e)

        elif choice.upper() == 'DAU':
            # Display all users
            flightSystem.displayAllUsers()
        
        elif choice.upper() == 'CR':
            # Change the role of a user
            flightSystem.changeRole()


        elif choice.upper() == 'E':
            # Exit YourSky
            break

        else:
            print(Fore.RED+"Invalid choice. Please try again.")
            print(Style.RESET_ALL)
            input("Press Enter to continue..")

def userMenu(flightSystem:FlightSystem):    
    while True:
        #flightSystem.clearTerminal()
        menu = '''
-----------------------------------------------------------------------------------------------------------------
|                                              User Dashboard                                                   |
-----------------------------------------------------------------------------------------------------------------
           
B:  Book a flight                      S: Search for flights                          DP: Display my Profile
DB: Display Booking                    C: Cancel booking                              UP: Update my Profile 
E:  Exit                                                                
    
Choice: '''
        choice = input(Fore.LIGHTBLUE_EX+menu)
        print(Style.RESET_ALL)
        if choice.upper() == 'S':
            # Search for flights
            origin = input("Enter departure airport: ")
            destination = input("Enter arrival airport: ")
            date = input("Enter date (YYYY-MM-DD): ")
            flightSystem.search_flights(origin, destination, date)

        elif choice.upper() == 'B':
            # Book a flight
            passengerId = input("Enter your passenger ID: ")
            flightNumber = input("Enter flight number: ")
            flightSystem.bookFlight(passengerId, flightNumber)

        
        elif choice.upper() == 'DB':
            # Display passenger booking confirmation
            bookingID =input("Enter booking ID: ")
            if bookingID in flightSystem.bookings:
                flightSystem.bookings[bookingID].dispalyBooking()
                
                
            
            
            for idx, passenger in enumerate(flightSystem.passengers.values, start=1):
                print(f"Passenger {idx}: {passenger}")
            
        elif choice.upper() == 'C':
            # Cancel booking
            passengerId = input("Enter your passenger ID: ")
            flightNumber = input("Enter flight number to cancel booking: ")
            flightSystem.cancel_booking(passengerId, flightNumber)


        elif choice.upper() == 'R':
            # Register a user
            flightSystem.register()

        elif choice.upper() == 'L':
            # Login a user
            flightSystem.login()
        
        elif choice.upper() == 'DP':
            # Display a user profile
            flightSystem.displayMyProfile()

        elif choice.upper() == 'UP':
            # Update user profile]
            newUserName = input("Enter new username: ")
            while (newUserName in flightSystem.users and newUserName != flightSystem.currentUserName):
                newUserName = input("Username taken! Try again: ")
            newPassword = input("Enter new password: ")
            newFullName = input("Enter new fullName: ")
            newBirthDate = input("Enter new birthDate: ")
            newEmail = input("Enter new email: ")
            newMobile = input("Enter new mobile: ")
            try:
                flightSystem.updateMyProfile(newUserName,newPassword,newFullName,newBirthDate,newEmail,newMobile)
                #print(Fore.GREEN+"User Profile has been updated successfully.")
            except Exception as e:
                print(e)

        elif choice.upper() == 'E':
            # Exit YourSky
            break

        else:
            print(Fore.RED+"Invalid choice. Please try again.")
            print(Style.RESET_ALL)
            input("Press Enter to continue..")

def main():
    while True:
        #flightSystem.clearTerminal()
        menu = '''
-----------------------------------------------------------------------------------------------------------------
|                                             WELCOME TO YOUR SKY                                               |
-----------------------------------------------------------------------------------------------------------------
           
L: Login                   R: Register                    C: Continue as guest                         E: Exit

Choice: '''

        choice = input(Fore.CYAN+menu)
        print(Style.RESET_ALL)
        if choice.upper() == 'L':
            try:
                role = flightSystem.login()
                if role != None:
                    if role :
                        adminMenu(flightSystem) 
                    else:
                        userMenu(flightSystem)
            except Exception as e:
                print(e)
        elif choice.upper() == 'R':
            flightSystem.register()
        elif choice.upper() == 'C':
            pass
        elif choice.upper() == 'E':
            break
        else:
            print(Fore.RED+"Invalid choice. Please try again.")
            input(Fore.CYAN+"Press Enter to continue..")
            print(Style.RESET_ALL)


if __name__ == "__main__":
    main()