"""
Sherlock Notify Module

This module defines the objects for notifying the caller about the
results of queries.
"""
import abc
from typing import Optional

from colorama import Fore, Style

from .result import QueryResult, QueryStatus

globvar = 0  # global variable to count the number of results.


class QueryNotify(metaclass=abc.ABCMeta):
    """
    Query Notify Object

    Base class that describes methods available to notify the results of
    a query.
    It is intended that other classes inherit from this base class and
    override the methods to implement specific functionality.
    """

    def __init__(self, result: Optional[QueryResult] = None) -> None:
        """
        Create Query Notify Object

        Contains information about a specific method of notifying the results
        of a query.

        Arguments:
        result                 -- Object of type QueryResult() containing
                                  results for this query.
        """

        self.result = result

    @abc.abstractmethod
    def start(self, message: str) -> None:
        """
        Notify Start

        Notify method for start of query.  This method will be called before
        any queries are performed.  This method will typically be
        overridden by higher level classes that will inherit from it.

        Arguments:
        message                -- Object that is used to give context to start
                                  of query.
        """
        raise NotImplementedError

    @abc.abstractmethod
    def update(self, result: QueryResult) -> None:
        """
        Notify Update

        Notify method for query result.  This method will typically be
        overridden by higher level classes that will inherit from it.

        Arguments:
        result                 -- Object of type QueryResult() containing
                                  results for this query.
        """
        raise NotImplementedError

    @abc.abstractmethod
    def finish(self, message: Optional[str] = None) -> None:
        """
        Notify Finish

        Notify method for finish of query.  This method will be called after
        all queries have been performed.  This method will typically be
        overridden by higher level classes that will inherit from it.

        Arguments:
        message                -- Object that is used to give context to start
                                  of query.
                                  Default is None.
        """
        raise NotImplementedError


class QueryNotifyPrint(QueryNotify):
    """
    Query Notify Print Object.
    Query notify class that prints results.
    """

    def __init__(
        self,
        result: Optional[QueryResult] = None,
        verbose: Optional[bool] = False,
        print_all: Optional[bool] = False,
    ) -> None:
        """
        Create Query Notify Print Object

        Contains information about a specific method of notifying the results
        of a query.

        Arguments:
        result                 -- Object of type QueryResult() containing
                                  results for this query.
        verbose                -- Boolean indicating whether to give verbose output.
        print_all              -- Boolean indicating whether to only print all sites, including not found.

        """

        super().__init__(result)
        self.verbose = verbose
        self.print_all = print_all

    def start(self, message: str) -> None:
        """
        Notify Start

        Will print the title to the standard output.

        Arguments:
        message                -- String containing username that the series
                                  of queries are about.
        """

        title = "Checking username"

        print(
            Style.BRIGHT
            + Fore.GREEN
            + "["
            + Fore.YELLOW
            + "*"
            + Fore.GREEN
            + f"] {title}"
            + Fore.WHITE
            + f" {message}"
            + Fore.GREEN
            + " on:"
        )
        # An empty line between first line and the result(more clear output)
        print("\r")

    def count_results(self) -> int:
        """
        This function counts the number of results. Every time the function is called,
        the number of results is increasing

        Return Value:
        The number of results by the time we call the function.
        """
        global globvar
        globvar += 1
        return globvar

    def update(self, result: QueryResult) -> None:
        """
        Notify Update

        Will print the query result to the standard output.

        Arguments:
        result                 -- Object of type QueryResult() containing
                                  results for this query.
        """
        self.result = result

        response_time_text = ""
        if self.result.query_time is not None and self.verbose:
            response_time_text = f" [{round(self.result.query_time * 1000)}ms]"

        # Output to the terminal is desired.
        if result.status == QueryStatus.CLAIMED:
            self.count_results()
            print(
                Style.BRIGHT
                + Fore.WHITE
                + "["
                + Fore.GREEN
                + "+"
                + Fore.WHITE
                + "]"
                + response_time_text
                + Fore.GREEN
                + f" {self.result.site_name}: "
                + Style.RESET_ALL
                + f"{self.result.site_url_user}"
            )

        elif result.status == QueryStatus.AVAILABLE:
            if self.print_all:
                print(
                    Style.BRIGHT
                    + Fore.WHITE
                    + "["
                    + Fore.RED
                    + "-"
                    + Fore.WHITE
                    + "]"
                    + response_time_text
                    + Fore.GREEN
                    + f" {self.result.site_name}:"
                    + Fore.YELLOW
                    + " Not Found!"
                )

        elif result.status == QueryStatus.UNKNOWN:
            if self.print_all:
                print(
                    Style.BRIGHT
                    + Fore.WHITE
                    + "["
                    + Fore.RED
                    + "-"
                    + Fore.WHITE
                    + "]"
                    + Fore.GREEN
                    + f" {self.result.site_name}:"
                    + Fore.RED
                    + f" {self.result.context}"
                    + Fore.YELLOW
                )

        elif result.status == QueryStatus.ILLEGAL:
            if self.print_all:
                msg = "Illegal Username Format For This Site!"
                print(
                    Style.BRIGHT
                    + Fore.WHITE
                    + "["
                    + Fore.RED
                    + "-"
                    + Fore.WHITE
                    + "]"
                    + Fore.GREEN
                    + f" {self.result.site_name}:"
                    + Fore.YELLOW
                    + f" {msg}"
                )

        else:
            # It should be impossible to ever get here...
            raise ValueError(f"Unknown Query Status '{result.status}' for site '{self.result.site_name}'")

    def finish(self, message: Optional[str] = "The processing has been finished.") -> None:
        """
        Notify finish

        Will print the last line to the standard output.

        Arguments:
        message                -- The 2 last phrases.
        """
        number_of_results = self.count_results() - 1

        title = "Results:"

        print(
            Style.BRIGHT
            + Fore.GREEN
            + "["
            + Fore.YELLOW
            + "*"
            + Fore.GREEN
            + f"] {title}"
            + Fore.WHITE
            + f" {number_of_results}"
        )

        title = "End"

        print("\r")  # An empty line between last line of main output and last line(more clear output)
        print(
            Style.BRIGHT
            + Fore.GREEN
            + "["
            + Fore.YELLOW
            + "!"
            + Fore.GREEN
            + f"] {title}"
            + Fore.GREEN
            + ": "
            + Fore.WHITE
            + f" {message}"
        )

        # An empty line between first line and the result(more clear output)
        print("\r")

    def __str__(self) -> str:
        """
        Convert Object To String

        Return Value: nicely formatted string to get information about this object
        """
        return str(self.result)
