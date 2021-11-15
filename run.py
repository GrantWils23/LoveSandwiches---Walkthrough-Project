import gspread
from google.oauth2.service_account import Credentials
from pprint import pprint

SCOPE = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/drive"
    ]

CREDS = Credentials.from_service_account_file('creds.json')
SCOPED_CREDS = CREDS.with_scopes(SCOPE)
GSPREAD_CLIENT = gspread.authorize(SCOPED_CREDS)
SHEET = GSPREAD_CLIENT.open('love_sandwiches')

# sales = SHEET.worksheet('sales')

# data = sales.get_all_values()

# print(data)


def get_sales_data():

    """
    Get sales input figures from the user.
    Run a while loop to collect a valid string of data from the user via,
    the terminal, which must be a string of 6 numbers seperated by commas,
    The loop will repeatedly request data, until the data provided is valid.
    """
    while True:
        print("please enter sales data from the last market.")
        print("data should be 6 numbers, seperated by commas.")
        print("Example: 10,20,30,40,50,60\n")

        data_str = input("Enter your data here:")
        print(f"The data provided is {data_str}")

        sales_data = data_str.split(",")

        if validate_data(sales_data):
            print("Data is valid")
            break

    return sales_data


def validate_data(values):
    """
    inside the try, converts all strings into intergers.
    Raises ValueError if strings cannot be converted into int,
    or if they aren't exactly 6 values.
    """
    try:
        [int(value) for value in values]
        if len(values) != 6:
            raise ValueError(
                f"Exactly 6 values required, you provided {len(values)}"
            )
    except ValueError as e:
        print(f"Invalid data: {e}, please try again.\n")
        return False

    return True


def update_sales_worksheet(data):
    """
    Update the sales worksheet, add new row with the list data provided.
    """
    print("updating sales worksheet...\n")
    sales_worksheet = SHEET.worksheet("sales")
    sales_worksheet.append_row(data)
    print("sales worksheet updated successfully.\n")


def update_surplus_worksheet(data):
    """
    Update the surplus worksheet, add new row into the list data provided.
    """
    print("updating the surplus worksheet...\n")
    surplus_worksheet = SHEET.worksheet("surplus")
    surplus_worksheet.append_row(data)
    print("surplus worksheet updated successfully.\n")


def calculated_surplus_data(sales_row):
    """
    Compare sales with stock and calculate the surplus for each item.

    The surplus is defined as the sales figures subtracted from the stock:
    - Positive surplus indicates waste.
    - Negative surplus indicates extras made when the stock was sold out.
    """
    print("calculating surplus data...\n")
    stock = SHEET.worksheet("stock").get_all_values()
    stock_row = stock[-1]
    stock_data = [int(num) for num in stock_row]
    print(f"stock_row: {stock_data}")
    print(f"sales_row: {sales_row}")

    surplus_data = []
    for stock, sales in zip(stock_data, sales_row):
        surplus = stock - sales
        surplus_data.append(surplus)
    print(surplus_data)


def main():
    """
    Run all program functions.
    """
    data = get_sales_data()
    sales_data = [int(num) for num in data]
    update_sales_worksheet(sales_data)
    surplus_data = calculated_surplus_data(sales_data)
    update_surplus_worksheet(surplus_data)


print("Welcome to Love Sandwiches Data Automation!\n")
main()
