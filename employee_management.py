from abc import ABC, abstractmethod
 
 
# --- Base Employee class ---
 
class Employee(ABC):
    def __init__(self, emp_id, name, department):
        self.emp_id = emp_id
        self.name = name
        self.department = department
 
    @abstractmethod
    def calculate_salary(self):
        pass
 
    def get_details(self):
        return {
            "id": self.emp_id,
            "name": self.name,
            "department": self.department,
            "type": self.__class__.__name__,
            "salary": self.calculate_salary(),
        }
 
    def __str__(self):
        return f"[{self.emp_id}] {self.name} | {self.department} | Salary: {self.calculate_salary():,.2f}"
 
 
class FullTimeEmployee(Employee):
    def __init__(self, emp_id, name, department, monthly_salary):
        super().__init__(emp_id, name, department)
        self.monthly_salary = monthly_salary
 
    def calculate_salary(self):
        return self.monthly_salary
 
 
class PartTimeEmployee(Employee):
    def __init__(self, emp_id, name, department, hourly_rate, hours_per_month):
        super().__init__(emp_id, name, department)
        self.hourly_rate = hourly_rate
        self.hours_per_month = hours_per_month
 
    def calculate_salary(self):
        return self.hourly_rate * self.hours_per_month
 
 
class ContractEmployee(Employee):
    def __init__(self, emp_id, name, department, contract_value, duration_months):
        super().__init__(emp_id, name, department)
        self.contract_value = contract_value
        self.duration_months = duration_months
 
    def calculate_salary(self):
        return self.contract_value / self.duration_months
 
 
# --- Department class ---
 
class Department:
    def __init__(self, name):
        self.name = name
        self._employees = []
 
    def add_employee(self, employee):
        self._employees.append(employee)
 
    def remove_employee(self, emp_id):
        before = len(self._employees)
        self._employees = [e for e in self._employees if e.emp_id != emp_id]
        return len(self._employees) < before
 
    def get_employees(self):
        return list(self._employees)
 
    def total_payroll(self):
        return sum(e.calculate_salary() for e in self._employees)
 
    def __str__(self):
        return f"Department: {self.name} | Headcount: {len(self._employees)} | Payroll: {self.total_payroll():,.2f}"
 
 
# --- EmployeeManager class ---
 
class EmployeeManager:
    def __init__(self):
        self._employees = {}
        self._departments = {}
 
    def add_department(self, name):
        if name in self._departments:
            raise ValueError(f"Department '{name}' already exists.")
        self._departments[name] = Department(name)
 
    def hire(self, employee):
        if employee.emp_id in self._employees:
            raise ValueError(f"Employee ID {employee.emp_id} already exists.")
        if employee.department not in self._departments:
            raise KeyError(f"Department '{employee.department}' does not exist.")
        self._employees[employee.emp_id] = employee
        self._departments[employee.department].add_employee(employee)
        print(f"Hired: {employee.name} ({employee.__class__.__name__}) in {employee.department}")
 
    def terminate(self, emp_id):
        if emp_id not in self._employees:
            raise KeyError(f"Employee ID {emp_id} not found.")
        employee = self._employees.pop(emp_id)
        self._departments[employee.department].remove_employee(emp_id)
        print(f"Terminated: {employee.name}")
 
    def get_employee(self, emp_id):
        if emp_id not in self._employees:
            raise KeyError(f"Employee ID {emp_id} not found.")
        return self._employees[emp_id]
 
    def list_all(self):
        if not self._employees:
            print("No employees on record.")
            return
        for emp in self._employees.values():
            print(f"  {emp}")
 
    def department_report(self):
        for dept in self._departments.values():
            print(f"  {dept}")
            for emp in dept.get_employees():
                print(f"    - {emp.name} ({emp.__class__.__name__}): {emp.calculate_salary():,.2f}/mo")
 
    def total_payroll(self):
        return sum(e.calculate_salary() for e in self._employees.values())
 
 
if __name__ == "__main__":
    manager = EmployeeManager()
 
    # Setup departments
    for dept in ["Engineering", "Marketing", "HR"]:
        manager.add_department(dept)
 
    # Hire employees
    manager.hire(FullTimeEmployee(101, "Alice", "Engineering", 95000))
    manager.hire(FullTimeEmployee(102, "Bob", "Marketing", 68000))
    manager.hire(PartTimeEmployee(103, "Charlie", "HR", hourly_rate=40, hours_per_month=80))
    manager.hire(ContractEmployee(104, "Diana", "Engineering", contract_value=120000, duration_months=6))
 
    print("\n--- All Employees ---")
    manager.list_all()
 
    print("\n--- Department Report ---")
    manager.department_report()
 
    print(f"\nTotal Monthly Payroll: {manager.total_payroll():,.2f}")
 
    # Terminate and check
    print("\n--- Terminating Bob ---")
    manager.terminate(102)
    print(f"Updated Payroll: {manager.total_payroll():,.2f}")
 
    # Error handling
    print("\n--- Error Handling Demo ---")
    try:
        manager.get_employee(999)
    except KeyError as e:
        print(f"Caught: {e}")
 
    try:
        manager.hire(FullTimeEmployee(105, "Eve", "Finance", 75000))
    except KeyError as e:
        print(f"Caught: {e}")
