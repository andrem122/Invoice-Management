class Project:
    """
    Gets details about each house/project.
    """

    def __int__(self, house):


    def expenses(self, house):
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
            house=house,
        )

    def completed_jobs(self, house):
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
            approved=True,
            balance_amount__lte=0,
            house__archived=False,
        )
