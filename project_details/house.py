from jobs.models import Job
from expenses.models import Expenses

class _House:
    """
    Gets details about each house.
    """

    """Class Variables"""
    closing_cost = 0.933 #closing costs cost 6.7% of house price
    broker_fee = 400.00

    def __init__(self, house):
        """
        self: The instance of the class
        house: The house object
        """
        self.house = house
        self.vars = {
            'after_repair_value': float(self.house.after_repair_value),
            'purchase_price': float(self.house.purchase_price),
            'profit': float(self.house.profit),
        }

    def expenses(self):
        """
        Fetches all expenses for the house

        Args:
            self: The object instance.
            houses: The house object.

        Returns:
            A queryset.

        Raises:
            None.
        """

        return Expenses.objects.filter(
            house=self.house,
        )

    def completed_jobs(self):
        """
        Fetches all completed jobs for the house

        Args:
            self: The object instance.
            houses: The house object.

        Returns:
            A queryset.

        Raises:
            None.
        """

        return Job.objects.filter(
            house=self.house,
            approved=True,
            balance_amount__lte=0,
        )

    def budget(self):
        """
        Calculates the budget for the house based on three variables
        input by the user: after_repair_value, purchase_price, profit
        This assumes a 6.7% closing cost (includes realtor commissions).

        Args:
            self: The object instance.

        Returns:
            A float.

        Raises:
            None.
        """

        budget = (_House.closing_cost*self.vars['after_repair_value']) - self.vars['purchase_price'] - self.vars['profit'] - _House.broker_fee
        return round(budget, 2)

    def total_spent(self):
        """
        Calculates the total amount spent for the house by
        adding all expenses and completed jobs.

        Args:
            self: The object instance.

        Returns:
            A float.

        Raises:
            None.
        """

        completed_jobs = Job.objects.filter(
            house=self.house,
            approved=True,
            balance_amount__lte=0,
            house__archived=False,
        )

        expenses = Expenses.objects.filter(
            house=self.house,
        )

        total = 0

        for job in completed_jobs:
            total += job.total_paid

        for expense in expenses:
            total += expense.amount

        return float(round(total, 2))

    def budget_balance(self):
        """
        Calculates the balance budget by taking the budget amount
        and subtracting the total spent amount.

        Args:
            self: The object instance.

        Returns:
            A float.

        Raises:
            None.
        """
        return self.budget() - self.total_spent()

    def potential_profit(self):
        potential_profit = (_House.closing_cost*self.vars['after_repair_value']) - self.vars['purchase_price'] - self.total_spent() - _House.broker_fee
        return round(potential_profit, 2)
