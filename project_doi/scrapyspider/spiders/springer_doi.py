import scrapy
from scrapy.loader import ItemLoader
from ..items import Book, Article, ConferencePaper
from scrapy.loader.processors import Join


class SpringerDoi(scrapy.Spider):
    """
              **Spider class implementation for link.springer.com**

      """
    name = 'springer'

    def __init__(self, category='', **kwargs):
        """
            Initialize the start url for the spyder.

        :param category: string

        """
        self.start_urls = [category]
        super().__init__(**kwargs)

    def parse(self, response):
        """
            Parse the page.

        * The type of the publication is found out from meta tag og:type
        * The fields are extracted from the web-page from meta tag , selector is the response object itself and loaded into Article Item
        * title,(//div[@class='page-title']/h1/text())
        * author, (//span[@class='authors-affiliations__name']/text())
        * Journal,
        * publisher,(//span[@id='publisher-name']/text())
        * chapters, (//span[@class='c-tabs__deemphasize']/text())
        * year, (//meta[@name='citation_publication_date']/@content)
        * abstract, (//meta[@name='description']/@content)
        * doi, (//input[@name='doi']/@value)
        * timestamp, (//meta[@name='citation_publication_date']/@content)
        * url, (//meta[@property='og:url']/@content)
        * booktitle, (//meta[@name='citation_inbook_title']/@content)
        * ENTRYTYPE, (//meta[@property='og:type']/@content)
        * ID, (The ID populated from the function load_id))

        :return: Itemloader (item= Article or Conference paper depending on the type)

        """
        if response.xpath("//meta[@property='og:type']/@content").extract():
            type_of_article = response.xpath("//meta[@property='og:type']/@content").extract()[0]
        elif response.xpath("//span[@class='test-content-type']/text()"):
            type_of_article = 'Book'
        else:
            return None

        if type_of_article == 'Book':
            book = response.xpath("//body")
            loader = ItemLoader(item=Book(), selector=book)
            loader.default_output_processor = Join()
            loader.add_xpath('title', "//div[@class='page-title']/h1/text()")
            loader.add_xpath('author', "//span[@class='authors-affiliations__name']/text()")
            loader.add_xpath('publisher', "//span[@id='publisher-name']/text()")
            loader.add_xpath('chapters', "//span[@class='c-tabs__deemphasize']/text()")
            loader.add_xpath('abstract', "//meta[@name='description']/@content")
            loader.add_xpath('doi', "//input[@name='doi']/@value")
            loader.add_xpath('ISBN', "//span[@id='electronic-isbn']/text()")
            loader.add_value('url', self.start_urls[0])
            loader.add_value('ID', loader.get_output_value('author').split(' ')[0])
            loader.add_value('ENTRYTYPE', 'Book')
        elif type_of_article == 'Paper':
            details = response
            loader = ItemLoader(item=ConferencePaper(), selector=details)
            loader.default_output_processor = Join()
            loader.add_xpath('title', "//meta[@name='citation_title']/@content")
            loader.add_xpath('author', "//meta[@name='citation_author']/@content")
            loader.add_xpath('booktitle', "//meta[@name='citation_inbook_title']/@content")
            loader.add_xpath('publisher', "//meta[@name='citation_publisher']/@content")
            loader.add_xpath('year', "//meta[@name='citation_publication_date']/@content")
            loader.add_xpath('abstract', "//meta[@name='description']/@content")
            loader.add_xpath('doi', "//meta[@name='citation_doi']/@content")
            loader.add_xpath('timestamp', "//meta[@name='citation_publication_date']/@content")
            loader.add_xpath('url', "//meta[@property='og:url']/@content")
            loader.add_value('ENTRYTYPE', type_of_article)
            loader.add_value('ID', load_id(loader))
        else:
            details = response
            loader = ItemLoader(item=Article(), selector=details)
            loader.default_output_processor = Join()
            loader.add_xpath('author', "//meta[@name='citation_author']/@content")
            loader.add_xpath('title', "//meta[@name='citation_title']/@content")
            loader.add_xpath('journal', "//meta[@name='citation_journal_title']/@content")
            loader.add_xpath('publisher', "//meta[@name='dc.publisher']/@content")
            loader.add_xpath('abstract', "//div[@class='c-article-section__content']/p/text()")
            loader.add_xpath('year', "//meta[@name='citation_publication_date']/@content")
            loader.add_xpath('timestamp', "//meta[@name='dc.date']/@content")
            loader.add_xpath('timestamp', "//meta[@name='citation_publication_date']/@content")
            loader.add_xpath('doi', "//meta[@name='citation_doi']/@content")
            loader.add_xpath('url', "//meta[@name='prism.url']/@content")
            loader.add_value('ENTRYTYPE', type_of_article)
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
    return author+year
