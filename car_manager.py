import json
import requests
from display import print_cars_header, print_car
from car import Car


server_url = "http://localhost:3000/cars"
c_header = {"Connection": "Close"}


def check_server(cid=None):
    # returns True or False;
    # when invoked without arguments simply checks if server responds;
    # invoked with car ID checks if the ID is present in the database;

    try:
        print("Checking Car server status...")
        reply = requests.head(server_url, headers=c_header)

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


def list_cars():
    # gets all cars' data from server and prints it;
    # if the database is empty prints diagnostic message instead;

    try:
        print("Checking Car server status...")
        reply = requests.get(server_url, headers=c_header)
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


def enter_id():
    # allows user to enter car's ID and checks if it's valid;
    # valid ID consists of digits only;
    # returns int or None (if user enters an empty line);
    try:
        input_id = input("Enter car ID, empty value to exit:")
        assert (input_id.isdigit()) or (input_id == "")
        return input_id
    except AssertionError:
        print("You didn't enter a valid ID number!")


def delete_car():
    # asks user for car's ID and tries to delete it from database;
    print("Enter the car ID you want to delete:")
    car_id = enter_id()
    car_url = server_url + "/" + car_id
    try:
        reply = requests.delete(car_url, headers=c_header)
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
