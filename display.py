key_title_names = ["ID", "Brand", "Model", "Year of production", "Convertible"]
key_title_width = [8, 15, 20, 20, 12]
key_car_names = ["id", "brand", "model", "production_year", "convertible"]


def print_header():
    # prints elegant cars table header;
    header_line = "+" + "-" * 35 + "+"
    header_title = "|".ljust(8) + "Vintage Car Database" + "|".rjust(9)
    print()
    print("WELCOME BACK!")
    print(header_line)
    print(header_title)
    print(header_line)


def print_menu():
    # prints user menu - nothing else happens here;
    menu = "M E N U"

    sep_line = "======"
    option1 = "1. List cars"
    option2 = "2. Add new car"
    option3 = "3. Delete car"
    option4 = "4. Update car"
    option0 = "0. Exit"
    print(menu)
    print(sep_line)
    print(option1)
    print(option2)
    print(option3)
    print(option4)
    print(option0)


def print_cars_header():
    for (name, width) in zip(key_title_names, key_title_width):
        print(name.ljust(width), end=" |")
    print()


def print_car(car):
    for (name, width) in zip(key_car_names, key_title_width):
        print(str(car[name]).ljust(width), end=" |")
    print()
