from display import print_header, print_menu
from car_manager import check_server, list_cars, delete_car, add_car, update_car


def read_user_choice():
    # reads user choice and checks if it's valid;
    # returns '0', '1', '2', '3' or '4'
    try:
        user_choice = int(input("Enter your choise (0..4):"))
        # make sure that user's choise is one of the item in the list
        assert user_choice in [0, 1, 2, 3, 4]
        return str(user_choice)
    except AssertionError:
        print("The choice you have entered is not in the menu!")
    except ValueError:
        print("The choice you have entered is not valid!")


while True:
    if not check_server():
        print("Server is not responding - quitting!")
        exit(1)
    print_header()
    print_menu()
    choice = read_user_choice()
    print(choice)
    if choice == '0':
        print("Bye!")
        exit(0)
    elif choice == '1':
        list_cars()
    elif choice == '2':
        add_car()
    elif choice == '3':
        delete_car()
    elif choice == '4':
        update_car()
