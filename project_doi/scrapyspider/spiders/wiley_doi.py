import scrapy
from scrapy.loader import ItemLoader
from ..items import Article, ConferencePaper
from scrapy.loader.processors import Join


class WileyDoi(scrapy.Spider):
    """
           **Spider class implementation for onlinelibrary.wiley.com**

   """
    name = 'wiley'

    def __init__(self, category='', **kwargs):
        """
            Initialize the start url for the spyder.

        :param category: string

        """
        self.start_urls = [category]
        super().__init__(**kwargs)

    def parse(self, response):
        r"""
                Parse the page.

            * The type of the publication is found out from meta tag og:type
            * The fields are extracted from the web-page from meta tag selector is the response object itself and loaded into Article Item
            * title, (//meta[@name='citation_title']/@content)
            * author, (//meta[@name='citation_author']/@content)
            * author, (//*[@id='a1_Ctrl']/span/text())
            * journal, (//meta[@name='citation_journal_title']/@content)
            * publisher, (//meta[@name='citation_publisher']/@content)
            * year, (//meta[@name='citation_online_date']/@content)
            * abstract, (normalize-space(//meta[@property='og:description']/@content))
            * doi, (//meta[@name='citation_doi']/@content)
            * timestamp, (//meta[@name='citation_online_date']/@content)
            * url, (//meta[@property='og:url']/@content)
            * booktitle, (//meta[@name='citation_book_title']/@content)
            * ENTRYTYPE, (//meta[@property='og:type']/@content)
            * ID, (The ID populated from the function load_id))

        :return: Itemloader (item= Article or Conference paper depending on the type)

        """
        type_of_article = response.xpath("//meta[@property='og:type']/@content").extract()[0]
        if type_of_article == 'Article':
            details = response
            loader = ItemLoader(item=Article(), selector=details)
            loader.default_output_processor = Join()
            loader.add_xpath('title', "//meta[@name='citation_title']/@content")
            loader.add_xpath('author', "//meta[@name='citation_author']/@content")
            loader.add_xpath('author', "//*[@id='a1_Ctrl']/span/text()")
            loader.add_xpath('journal', "//meta[@name='citation_journal_title']/@content")
            loader.add_xpath('publisher', "//meta[@name='citation_publisher']/@content")
            loader.add_xpath('year', "//meta[@name='citation_online_date']/@content")
            loader.add_xpath('abstract', "normalize-space(//meta[@property='og:description']/@content)")
            loader.add_xpath('doi', "//meta[@name='citation_doi']/@content")
            loader.add_xpath('timestamp', "//meta[@name='citation_online_date']/@content")
            loader.add_xpath('url', "//meta[@property='og:url']/@content")
            loader.add_xpath('ENTRYTYPE', "//meta[@property='og:type']/@content")
            loader.add_value('ID', load_id(loader))
        else:
            details = response
            loader = ItemLoader(item=ConferencePaper(), selector=details)
            loader.default_output_processor = Join()
            loader.add_xpath('title', "//meta[@name='citation_title']/@content")
            loader.add_xpath('booktitle', "//meta[@name='citation_book_title']/@content")
            loader.add_xpath('author', "//meta[@name='citation_author']/@content")
            loader.add_xpath('author', "//*[@id='a1_Ctrl']/span/text()")
            loader.add_xpath('publisher', "//meta[@name='citation_publisher']/@content")
            loader.add_xpath('year', "//meta[@name='citation_online_date']/@content")
            loader.add_xpath('abstract', "normalize-space(//meta[@property='og:description']/@content)")
            loader.add_xpath('doi', "//meta[@name='citation_doi']/@content")
            loader.add_xpath('timestamp', "//meta[@name='citation_online_date']/@content")
            loader.add_xpath('url', "//meta[@property='og:url']/@content")
            loader.add_xpath('ENTRYTYPE', "//meta[@property='og:type']/@content")
            loader.add_value('ID', load_id(loader))
        yield loader.load_item()


def load_id(loader):
    """
        ID is created by concatenating author and year.

    :param loader: ItemLoader
    :return: ID (first name of author+year)

    """
    author = loader.get_output_value('author').split(' ')[0]
    year = loader.get_output_value('year')
    return author + str(year)
