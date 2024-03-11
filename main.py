'''
Library System 
- user input of user_name !
- inventory book names - stored data of how many of those books are in the system !
- checkout_book function - limits to 5 books borrowed per user at any time, book borrowed stored in user_name list !
- return_book function - then takes borrowed book away from user_name, reduces borrow count by 1 !
- give fines for people who don't return their book within the maximum borrow period (5 days) 
'''

import csv
from datetime import datetime, timedelta
from tabulate import tabulate
import sys

inventory = []

'''
# Date for fines - current date for checking out - then compare to new current date?
def get_current_date():
    borrow_day = datetime.now()
    print(borrow_day)
    compare_date(borrow_day)
    
def compare_date(borrow_day):
    
    current_date = datetime.now()
    
    time_diff = current_date - borrow_day
    
    if time_diff > timedelta(days= 5):
        print("borrow over 5 days")
        
    else:
        print("borrow time ok")

'''

# Function to pull book name based off index
def get_book_from_index(book_choice):
    try:
        with open('inventory.csv', mode='r') as csvfile_inventory:
            csv_reader = csv.DictReader(csvfile_inventory)
            for row in csv_reader:
               if int(row['Index']) == book_choice:
                   print(f"\nYou would like to borrow: {row['Title']}")
                   return row['Title']
               
        return None
                   
    except FileNotFoundError:
        return 1

# Function to get the next index
def get_next_index():
    try:
        with open('inventory.csv', mode='r') as csvfile_inventory:
            csv_reader = csv.DictReader(csvfile_inventory)
            return max(int(row['Index']) for row in csv_reader) + 1
    except FileNotFoundError:
        return 1  # Return 1 if the file doesn't exist

# User main function
def users():

    while True:
        try:
            # Ask if existing user
            user_question = input("\nAre you an existing user? (y/n) : ").lower()
            
            # Check against user list
            if user_question == 'y':
                user_check = input("\nEnter name: ").capitalize()
                with open('users.csv', 'r') as csvfile_users:
                    csv_reader = csv.DictReader(csvfile_users)
                    for row in csv_reader:
                        if row['Name'] == user_check:
                            print(f"\nWelcome {user_check}!")
                            return user_check
                    
                    else:
                        print("\nName not in database.")
                                 
            # If not an existing user, call add user function
            if user_question == 'n':
                user_add_name = input("\nEnter your name : ").capitalize()
                add_user_csv(user_add_name)
                print(f"\nWelcome {user_add_name}! Please login now")
                      
        except ValueError:
            print("\nInvalid Input")

# Add user calling name from user function, initial data is 0 borrowed books / fines - written to csv file 'users.csv'
def add_user_csv(name):
    data = [{'Name' : name, 'Borrowed Books' : '', 'Fines' : 0}]
    with open('users.csv', 'a', newline='') as csvfile_users:
        fieldnames = ['Name', 'Borrowed Books', 'Fines']
        writer = csv.DictWriter(csvfile_users, fieldnames= fieldnames)
        
        if csvfile_users.tell() == 0:
            writer.writeheader()
        
        writer.writerows(data)

# Main menu - lists all functions
def main():
    print("""
What would you like to do?
1 - See the list of books we have
2 - Add a book to the library
3 - Checkout book
4 - Return book
5 - See list of fines
6 - See list of borrowed books
7 - Exit
""")
    main_func = int(input(": "))
    
    # Call book list
    if main_func == 1:
        display_inventory()
        goto_main()
    
    # Call add book
    elif main_func == 2:
        add_book()
        goto_main()
    
    # Call checkout book
    elif main_func == 3:
        checkout_book()
        goto_main()
        
    # Call return book
    elif main_func == 4:
        book_return()
        goto_main()
        
    # Call fines list
    elif main_func == 5:
        fines_list()
        goto_main()
    
    # See which books are borrowed by who and when
    elif main_func == 6:
        borrowed_books()
        goto_main()
        
    # Exit program
    elif main_func == 7:
        exit()
        
    else:
        print("\nInvalid input")
        
# Function run after function in main to give users option to return to main menu to execute multiple functions
def goto_main():
    # Code to return to main menu from functions
    while True:
        try:
            user_input = input("\nEnter 'q' to exit to Main Menu : ").lower()
            if user_input == 'q':
                main()
            else:
                print("\nInvalid Input!")
        except ValueError:
            print("\nInvalid Input")
        
# Displays Inventory func from 'inventory.csv'     
def display_inventory():
    headers = ["Index", "Book Title", "Availible Copies"]
    data = []
    
    with open('inventory.csv', mode='r') as csvfile_inventory:
        csv_reader = csv.DictReader(csvfile_inventory)
        for row in csv_reader:
            index = row['Index']
            title = row['Title']
            copies = row['Copies']
            data.append([index, title, copies])
            
            
    print(tabulate(tabular_data= data, headers= headers, tablefmt= 'grid'))
       
# Func to add books to inventory
def add_book():
    get_next_index()
    
    # User Input to add books into Library
    title = input("\nName of book to add to library inventory : ")
    copies = int(input("\nHow many copies would you like to add? : "))
    index = get_next_index()
    
    data = [{'Index' : index, 'Title' : title, 'Copies' : copies}]
    
    with open('inventory.csv', 'a', newline='') as csvfile_inventory:
        fieldnames = ['Index', 'Title', 'Copies']    
        writer = csv.DictWriter(csvfile_inventory, fieldnames= fieldnames)
        
        if csvfile_inventory.tell() == 0:
            writer.writeheader()
            
        writer.writerows(data)
                 
# Func to checkout books - checks books user has borrowed - if checkout is allowed, adds to their profile
def checkout_book():
    
    # Check how many books user has - if 5 or more, don't let them check book out
    # Call list of books
    max_books = 5
    with open('users.csv', 'r') as csvfile_users:
        csv_reader = csv.DictReader(csvfile_users)
        for row in csv_reader:
            if row['Name'] == name:
                if len(row["Borrowed Books"].split(",")) >= max_books:
                    print("\nBook limit reached, please return a book to borrow another.")
                    
                else:
                    print("\nWhich book would you like to borrow?")
                    display_inventory()
                    book_choice = int(input("\nEnter book index : "))
                    book_name = get_book_from_index(book_choice)
                    add_book_to_user(book_name)
                    
# Function to add borrowed book to user's profile         
def add_book_to_user(book_name):
    
    # opens csv to read data of books borrowed
    with open('users.csv', 'r') as csvfile_users:
        csv_reader = list(csv.DictReader(csvfile_users))
        for user in csv_reader:
            if user['Name'] == name:
                current_borrowed = user.get('Borrowed Books', '')
                if current_borrowed:
                    current_borrowed += f", {book_name}"
                
                else:
                    current_borrowed = book_name
                    
                user['Borrowed Books'] = current_borrowed
    
    # writes new borrowed book to users account    
    fieldnames = ['Name', 'Borrowed Books', 'Fines']
    with open('users.csv', 'w', newline= '') as csvfile_bookupdate:
        csv_writer = csv.DictWriter(csvfile_bookupdate, fieldnames= fieldnames)
        csv_writer.writeheader()
        csv_writer.writerows(csv_reader)
        
    remove_book_copies(book_name)

# Function to remove 1 copy from book that has been taken out of library                
def remove_book_copies(book_name):
    
    # Reads csv file to extract current int value of copies
    with open('inventory.csv', 'r') as csvfile_inventory: 
        csv_reader = csv.DictReader(csvfile_inventory)
        rows = list(csv_reader)
    
    # Takes 1 from the book copies
    for title in rows:
        if title['Title'] == book_name:
            current_book_copies = int(title.get('Copies', ''))
            title['Copies'] = str(current_book_copies - 1)
            
    # Write updated data back to csv file
    with open('inventory.csv', 'w', newline='') as csv_copies_update:
        fieldnames = csv_reader.fieldnames
        csv_writer = csv.DictWriter(csv_copies_update, fieldnames=fieldnames)
        csv_writer.writeheader()
        csv_writer.writerows(rows)  
    
    print("\nBook successfully checked out!")      
                       
# Func to return book - take it away from their profile
def book_return():
    with open('users.csv', 'r') as csvfile_users:
        csv_reader = list(csv.DictReader(csvfile_users))
        for user in csv_reader:
            if user['Name'] == name:
                current_borrowed = user.get('Borrowed Books', '') # Gets list of borrowed books
                
                borrowed_books = [book.strip() for book in current_borrowed.split(',')] # strips and creates list
                borrowed_index = [i + 1 for i in range(len(borrowed_books))] # creates an index system for table
                
                data = list(zip(borrowed_index, borrowed_books))
                headers = ["Index", "Book Title"]
                book_table = tabulate(data, headers= headers, tablefmt= "grid") # Data produced in readable view
                print(book_table)
                
                user_return_choice = int(input("\nWhich book would you like to return? : "))
                book_name = borrowed_books[user_return_choice - 1] # sets the book name for adding to csv file, indexs the origional list by -1 user input as list 0-2
                
                add_book_copies(book_name) # calls function to add book copy to the inventory.csv file
                remove_book_from_user(book_name) # calls function to remove book from user file
                
# Func to add book copies back to inventory when book is returned
def add_book_copies(book_name):
    # Reads csv file to extract current int value of copies
    with open('inventory.csv', 'r') as csvfile_inventory: 
        csv_reader = csv.DictReader(csvfile_inventory)
        rows = list(csv_reader)
    
    # Adds 1 to the book copies
    for title in rows:
        if title['Title'] == book_name:
            current_book_copies = int(title.get('Copies', ''))
            title['Copies'] = str(current_book_copies + 1)
            
    # Write updated data back to csv file
    with open('inventory.csv', 'w', newline='') as csv_copies_update:
        fieldnames = csv_reader.fieldnames
        csv_writer = csv.DictWriter(csv_copies_update, fieldnames=fieldnames)
        csv_writer.writeheader()
        csv_writer.writerows(rows) 

# Func to remove book from user borrowed list
def remove_book_from_user(book_name):
    with open('users.csv', 'r') as csvfile_users:
        csv_reader = list(csv.DictReader(csvfile_users))
        for user in csv_reader:
            if user['Name'] == name:
                current_borrowed = user.get('Borrowed Books', '').split(', ')
                
                if book_name in current_borrowed:
                    current_borrowed.remove(book_name)
                    user['Borrowed Books'] = ', '.join(current_borrowed)
                    print(f"\n{book_name} successfully returned!")
                else:
                    print(f"{name} did not borrow '{book_name}'.")
                
    # Write the updated borrowed books to users.csv
    fieldnames = ['Name', 'Borrowed Books', 'Fines']
    with open('users.csv', 'w', newline='') as csvfile_bookupdate:
        csv_writer = csv.DictWriter(csvfile_bookupdate, fieldnames=fieldnames)
        csv_writer.writeheader()
        csv_writer.writerows(csv_reader)
      
# Displays the list of fines for either individual user or all on system
def fines_list():
    pass

# Shows all borrowed books on either single user or everyone on system
def borrowed_books():
    with open('users.csv', 'r') as csvfile_users:
        csv_reader = list(csv.DictReader(csvfile_users))
        for user in csv_reader:
            if user['Name'] == name:
                current_borrowed = user.get('Borrowed Books', '')
                if len(current_borrowed) == 0:
                    print("\nNo books borrowed")
                
                else:
                    print(f"\nYour current borrowed books are: {current_borrowed}")

# Func to exit program
def exit():
    print("\nExiting the program...")
    sys.exit(0)


name = users()
main()

