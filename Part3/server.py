import socket
import os
import threading
import queue

# Create the Employees List to store Employee details
employees = {
    '001': {
        'Name': 'John Doe',
        'MonthlySalary': 5000,
        'AnnualLeaveDays': 20,
        'LeaveDaysUsed': 5
    },
    '002': {
        'Name': 'Jane Doe',
        'MonthlySalary': 6000,
        'AnnualLeaveDays': 22,
        'LeaveDaysUsed': 3
    },
    '003': {
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
    if verify_id(id) is not False:
        employee = employees.get(id)

        emp_id = id
        name = employee['Name']
        month_sal = employee['MonthlySalary']
        year_salary = employee['MonthlySalary'] * 12
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


# Create message queue to send to RabbitMQ
message_queue = queue.Queue()


# The start of server socket code
# Create a thread class to handle the new client connection
class ClientThread(threading.Thread):

    def __init__(self, client_socket, addr):

        threading.Thread.__init__(self)
        self.client_socket = client_socket
        self.addr = addr

    def run(self):

        print(f"Connection from {self.addr} has been established!")

        # Server sends Menu to Client
        self.client_socket.send(bytes("\n========== HR Control Panel Server ==========" +
                                      "\n\t1. Get Employee Monthly Salary" +
                                      "\n\t2. Get Employee Yearly Salary" +
                                      "\n\t3. Get remaining Employee Vacation Days" +
                                      "\n\t4. Get total Employee Vacation Days" +
                                      "\n\t5. Get all available information about Employee" +
                                      "\n\t6. Exit the Control Panel\n",
                                      "utf-8"))

        # Server gets user choice from Client
        ch_in = self.client_socket.recv(1024).decode('utf-8')
        ch = int(ch_in)
        print(ch)

        # Check ch to make sure it is in range of the menu options, pass ValueError if not
        try:
            if ch < 1 or ch > 6:

                self.client_socket.send(bytes("\nInvalid choice, Please provide a number between 1 and 6: ", "utf-8"))

            else:

                # Checking for menu item 6 because the Server does not need more information from Client
                if ch == 6:

                    self.client_socket.send(bytes("\n\nThank you for using the HR Control Panel!\n\n", "utf-8"))

                else:

                    # Request Employee ID from Client
                    self.client_socket.send(bytes("Enter Employee ID: ", "utf-8"))
                    emp_id = self.client_socket.recv(1024).decode('utf-8')

                    # Handle calling the methods required
                    if ch == 1:

                        if verify_id(emp_id) is not False:

                            month_sal = get_employee_monthly_salary(emp_id)
                            self.client_socket.send(
                                bytes(f"\nThis Employee's Monthly Salary is: €{month_sal}\n", "utf-8"))

                            # Send message to RabbitMQ Queue
                            message_queue.put((emp_id, 'Get Employee Monthly Salary', self.addr))

                        else:
                            self.client_socket.send(bytes("\nError: Invalid Employee ID.", "utf-8"))

                    elif ch == 2:

                        if verify_id(emp_id) is not False:
                            year_sal = get_employee_yearly_salary(emp_id)
                            self.client_socket.send(
                                bytes(f"\nThe Yearly Salary for this Employee is: €{year_sal}\n", "utf-8"))

                            # Send message to RabbitMQ Queue
                            message_queue.put((emp_id, 'Get Employee Yearly Salary', self.addr))

                        else:
                            self.client_socket.send(bytes("\nError: Invalid Employee ID.", "utf-8"))

                    elif ch == 3:

                        if verify_id(emp_id) is not False:

                            used_days = get_employee_used_leave_days(emp_id)
                            self.client_socket.send(bytes(f"\nThis Employee used {used_days} Leave Days\n", "utf-8"))

                            # Send message to RabbitMQ Queue
                            message_queue.put((emp_id, 'Get Employee Used Leave Days', self.addr))

                        else:
                            self.client_socket.send(bytes("\nError: Invalid Employee ID.", "utf-8"))

                    elif ch == 4:

                        if verify_id(emp_id) is not False:

                            total_days = get_employee__total_leave_days(emp_id)
                            self.client_socket.send(
                                bytes(f"\nThis Employee has {total_days} Leave Days available\n", "utf-8"))

                            # Send message to RabbitMQ Queue
                            message_queue.put((emp_id, 'Get Employee Total Leave Days', self.addr))

                        else:
                            self.client_socket.send(bytes("\nError: Invalid Employee ID.", "utf-8"))

                    elif ch == 5:

                        if verify_id(emp_id) is not False:

                            emp_details = get_employee_details(emp_id)
                            id, name, month_salary, year_salary, leave_days_available, leave_days_used = emp_details

                            self.client_socket.send(bytes(f"\nThe available information for this Employee is: " +
                                                          f"\n\tEmployee ID: {id}" +
                                                          f"\n\tEmployee Name: {name}" +
                                                          f"\n\tEmployee Monthly Salary: €{month_salary}" +
                                                          f"\n\tEmployee Yearly Salary: €{year_salary}" +
                                                          f"\n\tEmployee Leave Days available: {leave_days_available}" +
                                                          f"\n\tEmployee Leave Days used: {leave_days_used} \n",
                                                          "utf-8"))

                            # Send message to RabbitMQ Queue
                            message_queue.put((emp_id, 'Get all available Employee Details', self.addr))

                        else:
                            self.client_socket.send(bytes("\nError: Invalid Employee ID.", "utf-8"))

        except ValueError:
            self.client_socket.send(bytes("Invalid choice, Please provide a number", "utf-8"))

        self.client_socket.close()


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

        # Create a new thread for each client connection
        client_thread = ClientThread(client_socket, addr)
        client_thread.start()


if __name__ == "__main__":
    start_server()
