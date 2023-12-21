import socket
import os

employees = {
    '221': {
        'Name': 'John Doe',
        'MonthlySalary': 5000,
        'AnnualLeaveDays': 20,
        'LeaveDaysUsed': 5
    },
    '222': {
        'Name': 'Jane Doe',
        'MonthlySalary': 6000,
        'AnnualLeaveDays': 22,
        'LeaveDaysUsed': 3
    },
    '223': {
        'Name': 'Lana Shelton',
        'MonthlySalary': 9000,
        'AnnualLeaveDays': 30,
        'LeaveDaysUsed': 2
    }
}


# Verify that the given Employee ID is in the list
def verify_id(id):

    employee = employees.get(id)

    if employee is None:
        valid_id = False
    else:
        valid_id = True

    return valid_id


# Return all details related to the Employee using the given Employee ID
def get_employee_details(id):

    details_list = []

    if verify_id(id) is not False:

        employee = employees.get(id)

        emp_id = id
        name = employee['Name']
        month_sal = employee['MonthlySalary']
        year_salary =  month_sal * 12
        annual_leave = employee['AnnualLeaveDays']
        days_used = employee['LeaveDaysUsed']

        details_list = [

            emp_id,
            name,
            month_sal,
            year_salary,
            annual_leave,
            days_used

        ]

    return details_list


# Return the Yearly Salary of the Employee using the given Employee ID
def get_employee_yearly_salary(id):

    yearly_salary = 0

    if verify_id(id) is not False:

        employee = employees.get(id)
        monthly_salary = employee['MonthlySalary']
        yearly_salary = monthly_salary * 12

    return yearly_salary


# Return the Monthly Salary of the Employee using the given Employee ID
def get_employee_monthly_salary(id):

    salary = 0

    if verify_id(id) is not False:

        employee = employees.get(id)
        monthly_salary = employee['MonthlySalary']
        salary = monthly_salary

    return salary


# Return the amount of Leave Days used by the Employee using the given Employee ID
def get_employee_used_leave_days(id):

    remain_days = 0

    if verify_id(id) is not False:

        employee = employees.get(id)
        remain_days = {employee['LeaveDaysUsed']}

    return remain_days


# Return the Total number of Leave Days entitled to the Employee using the given Employee ID
def get_employee__total_leave_days(id):

    leave_days = 0

    if verify_id(id) is not False:

        employee = employees.get(id)
        leave_days = {employee['AnnualLeaveDays']}

    return leave_days


def start_server():

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('localhost', 12345))
    server_socket.listen(1)

    while True:

        # Closes the socket if close.txt exists in the running directory
        if os.path.exists('close.txt'):
            print("Closing server...")
            server_socket.close()
            os.remove('close.txt')
            exit()

        client_socket, addr = server_socket.accept()
        print(f"Connection from {addr} has been established!")

        # Server sends Menu to Client
        client_socket.send(bytes("\n========== HR Control Panel Server ==========" +
                                 "\n\t1. Get Employee Monthly Salary" +
                                 "\n\t2. Get Employee Yearly Salary" +
                                 "\n\t3. Get remaining Employee Vacation Days" +
                                 "\n\t4. Get total Employee Vacation Days" +
                                 "\n\t5. Get all available information about Employee" +
                                 "\n\t6. Exit the Control Panel\n",
                                 "utf-8"))

        # Server gets user choice from Client
        ch_in = client_socket.recv(1024).decode('utf-8')
        ch = int(ch_in)
        print(ch)

        try:
            if ch < 1 or ch > 6:

                client_socket.send(bytes("\nInvalid choice, Please provide a number between 1 and 6: ", "utf-8"))

            else:

                # Checking for menu item 6 because the Server does not need more information from Client
                if ch == 6:

                    client_socket.send(bytes("\n\nThank you for using the HR Control Panel!\n\n", "utf-8"))

                else:

                    # Request Employee ID from Client
                    client_socket.send(bytes("Enter Employee ID: ", "utf-8"))
                    emp_id = client_socket.recv(1024).decode('utf-8')

                    # Handle calling the methods required
                    if ch == 1:

                        if verify_id(emp_id) is not False:

                            month_sal = get_employee_monthly_salary(emp_id)
                            client_socket.send(bytes(f"\nThis Employee's Monthly Salary is: €{month_sal}\n", "utf-8"))

                        else:
                            client_socket.send(bytes("\nError: Invalid Employee ID.", "utf-8"))

                    elif ch == 2:

                        if verify_id(emp_id) is not False:
                            year_sal = get_employee_yearly_salary(emp_id)
                            client_socket.send(
                                bytes(f"\nThe Yearly Salary for this Employee is: €{year_sal}\n", "utf-8"))

                        else:
                            client_socket.send(bytes("\nError: Invalid Employee ID.", "utf-8"))

                    elif ch == 3:

                        if verify_id(emp_id) is not False:

                            used_days = get_employee_used_leave_days(emp_id)
                            client_socket.send(bytes(f"\nThis Employee used {used_days} Leave Days\n", "utf-8"))

                        else:
                            client_socket.send(bytes("\nError: Invalid Employee ID.", "utf-8"))

                    elif ch == 4:

                        if verify_id(emp_id) is not False:

                            total_days = get_employee__total_leave_days(emp_id)
                            client_socket.send(
                                bytes(f"\nThis Employee has {total_days} Leave Days available\n", "utf-8"))

                        else:
                            client_socket.send(bytes("\nError: Invalid Employee ID.", "utf-8"))

                    elif ch == 5:

                        if verify_id(emp_id) is not False:

                            emp_details = get_employee_details(emp_id)
                            id, name, month_salary, year_salary, leave_days_available, leave_days_used = emp_details

                            client_socket.send(bytes(f"\nThe available information for this Employee is: " +
                                                     f"\n\tEmployee ID: {id}" +
                                                     f"\n\tEmployee Name: {name}" +
                                                     f"\n\tEmployee Monthly Salary: €{month_salary}" +
                                                     f"\n\tEmployee Yearly Salary: €{year_salary}" +
                                                     f"\n\tEmployee Leave Days available: {leave_days_available}" +
                                                     f"\n\tEmployee Leave Days used: {leave_days_used} \n",
                                                     "utf-8"))
                        else:
                            client_socket.send(bytes("\nError: Invalid Employee ID.", "utf-8"))

        except ValueError:
            client_socket.send(bytes("Invalid choice, Please provide a number", "utf-8"))

        client_socket.close()


if __name__ == "__main__":
    start_server()
