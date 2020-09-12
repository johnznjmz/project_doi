import crochet

crochet.setup()  # initialize crochet before further imports

from scrapy import signals
from scrapy.crawler import CrawlerRunner
from scrapy.signalmanager import dispatcher
from scrapy.settings import Settings
from scrapy.utils.log import configure_logging
from . import database
import sys
sys.path.insert(0, 'project_doi/scrapyspider')
from .scrapyspider import settings as sets


class Scrape:
    """
            Class that represents connection between flask and scrapy.

     * run crawler in twisted reactor synchronously
     * Initialize CrawlRunner()

    """
    crawl_runner = CrawlerRunner()
    dict_of_spiders = {}

    def scrape(self, domain, dict_of_spiders):
        """
                run crawler in twisted reactor synchronously.

        :param domain:  the list of domains
        :param dict_of_spiders:{'springer': SpringerDoi, 'wiley': WileyDoi, 'ieee': IeeeDoi}

        """
        domains = domain
        self.dict_of_spiders = dict_of_spiders

        for domain in domains:
            try:
                self.scrape_with_crochet(domain).wait(timeout=5)
            except crochet.TimeoutError:
                self.scrape_with_crochet(domain).cancel()
                raise

    @crochet.run_in_reactor
    def scrape_with_crochet(self, domain):
        """
                signal fires when single item is processed and calls _crawler_result to save that item.

        Consider some synchronous do-one-thing-after-the-other application code that wants to use event-driven Twisted-using code.
        We have two threads at a minimum: the application thread(s) and the reactor thread. There are also multiple layers
        of code involved in this interaction

        Twisted code: Should only be called in reactor thread. This may be code from the Twisted package itself, or more
        likely code you have written that is built on top of Twisted.

        @wait_for/@run_in_reactor wrappers: The body of the functions runs in the reactor thread... but the caller
        should be in the application thread.

        The application code: Runs in the application thread(s), expects synchronous/blocking calls.
        dispatcher.connect will connect to the dispatcher that will kind of loop the code between these two functions.
        crawl_runner.crawl will connect to the our particular spider function based on the domain name,
        in our scrapy file and after each yield will pass to the crawler_result function.
        The setting.py is applied to the crawl runner.

        :param domain: the domain to crawl
        :return: a twisted.internet.defer.Deferred

        """
        configure_logging({'LOG_FORMAT': '%(levelname)s: %(message)s'})
        crawler_settings = Settings()
        crawler_settings.setmodule(sets)
        self.crawl_runner.settings = crawler_settings
        dispatcher.connect(self._crawler_result, signal=signals.item_scraped)

        for i in self.dict_of_spiders:
            if i in domain:
                eventual = self.crawl_runner.crawl(self.dict_of_spiders[i], category=domain)
                return eventual

    def _crawler_result(self, item, response, spider):
        """
           A callback that is fired after the scrape has completed.
           The scraped results are saved to Database.

        :param item: The items scraped from the website
           """
        database.save(dict(item))
