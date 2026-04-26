from __future__ import print_function
import logging

import grpc
import EmployeeService_pb2
import EmployeeService_pb2_grpc

import const

def run():
    with grpc.insecure_channel(const.IP+':'+const.PORT) as channel:
        stub = EmployeeService_pb2_grpc.EmployeeServiceStub(channel)

        # Query an employee's data
        response = stub.GetEmployeeDataFromID(EmployeeService_pb2.EmployeeID(id=101))
        print ('Employee\'s data: ' + str(response))

        # Add a new employee
        response = stub.CreateEmployee(EmployeeService_pb2.EmployeeData(id=301, name='Jose da Silva', title='Programmer'))
        print ('Added new employee ' + response.status)

        # Change an employee's title
        response = stub.UpdateEmployeeTitle(EmployeeService_pb2.EmployeeTitleUpdate(id=301, title='Senior Programmer'))
        print ('Updated employee ' + response.status)

        # Delete an employee
        response = stub.DeleteEmployee(EmployeeService_pb2.EmployeeID(id=201))
        print ('Deleted employee ' + response.status)

        # List all employees
        response = stub.ListAllEmployees(EmployeeService_pb2.EmptyMessage())
        print ('All employees: ' + str(response))

        # Update employee name and title at once
        response = stub.UpdateEmployee(EmployeeService_pb2.EmployeeFullUpdate(id=101, name='Saravanan S', title='Principal Engineer'))
        print ('Updated employee (name+title): ' + response.status)

        # Search employees by partial name
        response = stub.SearchEmployeesByName(EmployeeService_pb2.SearchQuery(name='Saravanan'))
        print ('Search by name "Saravanan": ' + str(response))

        # Stream all employees one by one (server-side streaming)
        print ('Streaming all employees:')
        for emp in stub.StreamAllEmployees(EmployeeService_pb2.EmptyMessage()):
            print ('  ' + str(emp).strip())

        # Batch create multiple employees (client-side streaming)
        new_employees = iter([
            EmployeeService_pb2.EmployeeData(id=401, name='Ana Lima', title='DevOps Engineer'),
            EmployeeService_pb2.EmployeeData(id=501, name='Carlos Pereira', title='Data Scientist'),
        ])
        response = stub.BatchCreateEmployees(new_employees)
        print ('Batch create status: ' + response.status)

if __name__ == '__main__':
    logging.basicConfig()
    run()