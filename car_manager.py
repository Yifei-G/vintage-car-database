import json
import requests
from display import print_cars_header, print_car
from car import Car


server_url = "http://localhost:3000/cars"
close_header = {"Connection": "Close"}
content_header = {"Content-Type": "application/json"}


def check_server(cid=None):
    # returns True or False;
    # when invoked without arguments simply checks if server responds;
    # invoked with car ID checks if the ID is present in the database;
    if cid is None:
        try:
            print("Checking Car server status...")
            reply = requests.head(server_url, headers=close_header)

            if reply.status_code == requests.codes.ok:
                print("Sever is available!")
                return True
            else:
                return False

        except requests.exceptions.InvalidURL:
            print("The URL you entered is not valid!")
            exit(1)

        except requests.exceptions.ConnectionError:
            print("Can't connect to the Sever!", server_url)
            exit(2)

        except requests.RequestException:
            print("Error get response from the server!")
            exit(3)
    else:
        print("Checking if a car exists...")
        if cid is not None:
            car_url = server_url + "/" + cid
            try:
                reply = requests.head(car_url, headers=close_header)

                if reply.status_code == requests.codes.ok:
                    return True
                else:
                    return False

            except requests.exceptions.InvalidURL:
                print("The URL you entered is not valid!")
                exit(1)

            except requests.exceptions.ConnectionError:
                print("Can't connect to the Sever!", server_url)
                exit(2)

            except requests.RequestException:
                print("Error get response from the server!")
                exit(3)


def name_is_valid(name):
    # checks if name (brand or model) is valid;
    # valid name is non-empty string containing
    # digits, letters and spaces;
    # returns True or False;

    # Delete all the spaces in the name
    # check if the string only contains letters or digitis
    if (name != "") and (name.replace(" ", "").isalnum()):
        return True
    else:
        return False


def enter_id():
    # allows user to enter car's ID and checks if it's valid;
    # valid ID consists of digits only;
    # returns int or None (if user enters an empty line);
    try:
        input_id = input("Enter car ID, empty value to exit:")
        assert (input_id.isdigit()) or (input_id == "")
        if input_id == "":
            input_id = None
        return input_id
    except AssertionError:
        print("You didn't enter a valid ID number!")


def enter_name(what):
    # allows user to enter car's name (brand or model) and checks if it's valid;
    # uses name_is_valid() to check the entered name;
    # returns string or None  (if user enters an empty line);
    # argument describes which of two names is entered currently ('brand' or
    # 'model');
    if what == "brand":
        input_brand = input("Enter the brand, empty value to exit:")
        if name_is_valid(input_brand):
            return input_brand
        elif input_brand == "":
            return None
        else:
            print("The brand is not valid!")
    else:
        input_model = input("Enter the model, empty value to exit:")
        if name_is_valid(input_model):
            return input_model
        elif input_model == "":
            return None


def enter_production_year():
    # allows user to enter car's production year and checks if it's valid;
    # valid production year is an int from range 1900..2000;
    # returns int or None  (if user enters an empty line);
    try:
        input_year = input("Enter production year, empty value to exit:")
        assert ((input_year.isdigit()) and (int(input_year) > 1900 and int(input_year) < 2000)) or (input_year == "")

        if input_year == "":
            input_year = None

        return input_year
    except AssertionError:
        print("You didn't enter a valid year!")


def enter_convertible():
    # allows user to enter Yes/No answer determining if the car is convertible;
    # returns True, False or None  (if user enters an empty line);
    try:
        input_convertible = input("Is convertible? [y/n]:")
        assert (input_convertible == "") or (
            input_convertible.lower() in ["y", "n", "yes", "no"])
        if input_convertible == "":
            input_convertible = None
        elif input_convertible.lower() in ["y", "yes"]:
            input_convertible = True
        elif input_convertible.lower() in ["n", "no"]:
            input_convertible = False

        return input_convertible
    except AssertionError:
        print("You didn't enter a valid input, please usse y or n!")


def input_car_data(with_id):
    # lets user enter car data;
    # argument determines if the car's ID is entered (True) or not (False);
    # returns None if user cancels the operation or a dictionary of the following structure:
    # {'id': int, 'brand': str, 'model': str, 'production_year': int, 'convertible': bool }
    car_id = enter_id()
    if car_id is None:
        return None
    car_brand = enter_name("brand")
    if car_brand is None:
        return None
    car_model = enter_name("model")
    if car_model is None:
        return None
    car_product_year = enter_production_year()
    if car_product_year is None:
        return None
    car_is_convertible = enter_convertible()
    if car_is_convertible is None:
        return None

    car = Car(car_id, car_brand, car_model, car_product_year, car_is_convertible)
    return car.__dict__


def list_cars():
    # gets all cars' data from server and prints it;
    # if the database is empty prints diagnostic message instead;

    try:
        print("Checking Car server status...")
        reply = requests.get(server_url, headers=close_header)
        print_cars_header()
        if len(reply.json()) > 1:
            for carJSON in reply.json():
                print_car(carJSON)
        else:
            print_car(reply.json())

    except requests.exceptions.InvalidURL:
        print("The URL you entered is not valid!")
        exit(1)

    except requests.exceptions.ConnectionError:
        print("Can't connect to the Sever!", server_url)
        exit(2)

    except requests.RequestException:
        print("Error get response from the server!")
        exit(3)


def add_car():
    # invokes input_car_data(True) to gather car's info and adds it to the
    # database;

    print("Please enter the following information to add a car into the database!")
    new_car = input_car_data(True)
    if type(new_car) is dict:
        is_car_exist = check_server(new_car["id"])
        if is_car_exist:
            print("The ID has already associated a car! Check all Cars using option 1 first!")
            exit()
        else:

            new_car_JSON = json.dumps(new_car, default=Car.jsonEncoder)
            try:
                reply = requests.post(server_url, headers=content_header, data=new_car_JSON)
                if reply.status_code == requests.codes.created:
                    print("Sucess! New Car created!")
                else:
                    print("Opss.. Some error has occured!")
            except requests.exceptions.InvalidURL:
                print("The URL you entered is not valid!")
                exit(1)
            except requests.exceptions.ConnectionError:
                print("Can't connect to the Sever!", server_url)
                exit(2)
            except requests.RequestException:
                print("Error get response from the server!")
                exit(3)
    else:
        print("Operation canceled!")


def update_car():
    # invokes enter_id() to get car's ID if the ID is present in the database;
    # invokes input_car_data(False) to gather new car's info and updates the
    # database;
    print("Enter the car ID you want to modify:")
    car_id = enter_id()
    car_url = server_url + "/" + car_id
    if check_server(car_id):
        print("Car exists!")
        exit_car = input_car_data(False)
        if type(exit_car) is dict:
            exit_car_JSON = json.dumps(exit_car, default=Car.jsonEncoder)
            try:
                reply = requests.put(car_url, headers=content_header, data=exit_car_JSON)
                if reply.status_code == requests.codes.ok:
                    print("Sucess! Car modified!")
                else:
                    print("Opss.. Some error has occured!")
            except requests.exceptions.InvalidURL:
                print("The URL you entered is not valid!")
                exit(1)
            except requests.exceptions.ConnectionError:
                print("Can't connect to the Sever!", car_url)
                exit(2)
            except requests.RequestException:
                print("Error get response from the server!")
                exit(3)
        else:
            print("Operation canceled!")
    else:
        print("The car you trying to modify doesn't exist!")


def delete_car():
    # asks user for car's ID and tries to delete it from database;
    print("Enter the car ID you want to delete:")
    car_id = enter_id()
    car_url = server_url + "/" + car_id
    try:
        reply = requests.delete(car_url, headers=close_header)
        print(reply.status_code)
        if reply.status_code == requests.codes.not_found:
            print("The car you trying to delete doesn't exist!")
        elif reply.status_code == requests.codes.ok:
            print("Sucess! car deleted!")

    except requests.exceptions.InvalidURL:
        print("The URL you entered is not valid!")
        exit(1)
    except requests.exceptions.ConnectionError:
        print("Can't connect to the Sever!", server_url)
        exit(2)

    except requests.RequestException:
        print("Error get response from the server!")
        exit(3)
