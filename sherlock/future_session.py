from concurrent.futures import Future
from time import monotonic
from typing import Any, Callable, Dict, List, Optional, Tuple, Union

from requests_futures.sessions import FuturesSession


class SherlockFuturesSession(FuturesSession):
    def request(
        self,
        method: str,
        url: str,
        hooks: Optional[Dict[str, Union[List[Callable], Tuple[Callable]]]] = None,
        *args: Any,
        **kwargs: Any,
    ) -> Future:
        """
        Request URL

        This extends the FuturesSession request method to calculate a response
        time metric to each request.

        It is taken (almost) directly from the following Stack Overflow answer:
        https://github.com/ross/requests-futures#working-in-the-background

        Arguments:
        method                 -- String containing method desired for request.
        url                    -- String containing URL for request.
        hooks                  -- Dictionary containing hooks to execute after
                                  request finishes.
        args                   -- Arguments.
        kwargs                 -- Keyword arguments.

        Return Value: request object
        """

        # Record the start time for the request.
        if hooks is None:
            hooks = {}
        start = monotonic()

        def response_time(resp, *args, **kwargs):
            """
            Response Time Hook

            Arguments:
            resp                   -- Response object.
            args                   -- Arguments.
            kwargs                 -- Keyword arguments.
            """
            resp.elapsed = monotonic() - start

            return

        # Install hook to execute when response completes.
        # Make sure that the time measurement hook is first, so we will not
        # track any later hook's execution time.
        try:
            if isinstance(hooks["response"], list):
                hooks["response"].insert(0, response_time)
            elif isinstance(hooks["response"], tuple):
                # Convert tuple to list and insert time measurement hook first.
                hooks["response"] = list(hooks["response"])
                hooks["response"].insert(0, response_time)
            else:
                # Must have previously contained a single hook function,
                # so convert to list.
                hooks["response"] = [response_time, hooks["response"]]
        except KeyError:
            # No response hook was already defined, so install it ourselves.
            hooks["response"] = [response_time]

        return super().request(method, url, hooks=hooks, *args, **kwargs)
