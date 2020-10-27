from abc import ABCMeta, abstractmethod
import logging
import math
from urllib import parse

logger = logging.getLogger(__name__)


class BasePaginator(metaclass=ABCMeta):
    """
    This class implements paginator functionality that can be added onto any
    API client class.

    This class requires the subclass to implement property methods for
        - page size
        - total results
        - current page
        - getting parameters for pagination

    This class structures pagination protocols based on the following:
    An API request will match some number of results, or total results.

    The request returns a set of results of fixed size, or page size.

    A request usually takes a page, or current page.

    The total pages can be derived from the total results and page size.

    To continue pagination, the current page should be less than the total pages.
    If you are on the last page, i.e. total pages number, then there are no more
    results.
    """

    def _get_url_query_param(self, url, value):
        """
        Helper function to extract a query parameter (value) from a given url.

        Args:
            url (str): Url to parse
            value (str): Query paramter

        Returns:
            str: The value of query parameter
        """
        url_parts = parse.parse_qs(parse.urlparse(url).query)
        return url_parts.get(value)[0]

    @abstractmethod
    def page_size(self):
        """
        This method should return the size or count of results expected per
        API request. Usually this is passed as a query parameter in the API
        request.

        Returns:
            int: number of results per response
        """
        pass

    @abstractmethod
    def total_results(self):
        """
        This method should return the total results of the request.
        Usually returned in the API response.

        Returns:
            int: total results available for the request
        """
        pass

    @property
    def total_pages(self):
        """
        This method calculated the total number of pages it would take to
        collect all results based off the page size and total results for
        the request.

        Returns:
            int: total pages to paginate
        """
        return math.ceil(self.total_results / self.page_size)

    @abstractmethod
    def current_page(self):
        """
        This method should return the current page representing which set of
        results of the total results reached. Usually this is passed as a 
        query parameter in the API request.

        Returns:
            int: current page of results
        """
        pass

    def continue_pagination(self, max_pages=None):
        """
        This method determines if there are more results to fetch on another
        page. You can specify a number of pages to paginate by passing in
        max_pages.

        Args:
            max_pages (int, None): number of pages to paginate

        Returns:
            bool: True if pagination can continue, False if not
        """
        logger.debug(
            f'current page {self.current_page}, {type(self.current_page)}, {self.total_pages}, {type(self.total_pages)}')

        if not max_pages:
            # ok to paginate if current page is less than total pages.
            # don't paginate if current page is equal to total pages number.
            return self.current_page < self.total_pages

        if max_pages > self.total_pages:
            logger.warning(
                f'max pages requested {max_pages} is greater than total pages {self.total_pages}, setting to {self.total_pages}')
            max_pages = self.total_pages

        # don't paginate if max pages is the current page
        return not (max_pages == self.current_page)

    @abstractmethod
    def get_next_params(self):
        """
        This method should return the params required only to make the next
        paginated request.

        Returns:
            dict: key, val of query parameters for next request
        """
        pass


class BingPaginatorMixin(BasePaginator):
    @property
    def offset(self):
        return int(self._get_url_query_param(self.response_url, 'offset'))

    @property
    def page_size(self):
        return int(self._get_url_query_param(self.response_url, 'count'))

    @property
    def total_results(self):
        return self.response.json()['totalEstimatedMatches']

    @property
    def current_page(self):
        return self.offset // self.page_size + 1

    def get_next_params(self):
        return {'offset': self.offset + self.page_size}


class NewsApiPaginatorMixin(BasePaginator):
    @property
    def page_size(self):
        return int(self._get_url_query_param(self.response_url, 'pageSize'))

    @property
    def total_results(self):
        return self.response.json()['totalResults']

    @property
    def current_page(self):
        return int(self._get_url_query_param(self.response_url, 'page'))

    def get_next_params(self):
        return {'page': self.current_page + 1}
