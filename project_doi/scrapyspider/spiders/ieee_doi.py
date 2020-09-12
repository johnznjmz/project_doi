import scrapy
from scrapy.loader import ItemLoader
from scrapy.loader.processors import Join
import json
import re
from ..items import Book, Article, ConferencePaper


class IeeeDoi(scrapy.Spider):
    """
               **Spider class implementation for ieeexplore.ieee.org**

   """
    name = 'ieee'

    def __init__(self, category='', **kwargs):
        """
            Initialize the start url for the spyder.

        :param category: string (start url)

        """
        self.start_urls = [category]
        super().__init__(**kwargs)

    def parse(self, response):
        r"""
               Parse the page

           * The type of the publication is found out from meta tag og:type.
           * The fields are extracted from the web-page from javascript variable global.document.metadata, selector is the response object itself and loaded into Article or Book or ConferencePaper Item depend on the contentType
           * The javascript variable is extracted using regex r"global.document.metadata=(.+?);" and saved as a json object
           * title,
           * author,
           * Journal,
           * publisher,
           * year,
           * abstract,
           * doi,
           * timestamp,
           * url,
           * booktitle,
           * ENTRYTYPE,
           * ID, (The ID populated from the function load_id))

           :return: Itemloader (item= Article or Conference paper depending on the type)

        """
        data = re.findall(r"global.document.metadata=(.+?);\n", response.body.decode("utf-8"), re.S)
        data_dict = json.loads(data[0])
        if data_dict:
            if data_dict['contentType'] == 'books':
                loader = ItemLoader(item=Book(), selector=response)
                loader.default_output_processor = Join()
                loader.add_value('title', data_dict['title'])
                loader.add_value('author', [i['name'] for i in data_dict['authors']])
                loader.add_value('publisher', data_dict['publisher'])
                loader.add_value('chapters', '0')
                loader.add_value('abstract', data_dict['abstract'])
                loader.add_value('doi', data_dict['doi'])
                loader.add_value('ISBN', [i['value'] for i in data_dict['isbn']][1])
                loader.add_value('url', self.start_urls[0])
                loader.add_value('ID', loader.get_output_value('author').split(' ')[0])
                loader.add_value('ENTRYTYPE', 'Book')
            elif data_dict['contentType'] == 'conferences' or data_dict['contentType'] == 'chapter':
                loader = ItemLoader(item=ConferencePaper(), selector=response)
                loader.default_output_processor = Join()
                loader.add_value('title', data_dict['title'])
                loader.add_value('author', [i['name'] for i in data_dict['authors']])
                loader.add_value('booktitle', data_dict['publicationTitle'])
                loader.add_value('publisher', data_dict['publisher'])
                loader.add_value('year', data_dict['publicationYear'])
                loader.add_value('abstract', data_dict['abstract'])
                loader.add_value('doi', data_dict['doi'])
                loader.add_value('timestamp', data_dict['publicationDate'])
                loader.add_value('url', self.start_urls[0])
                loader.add_value('ENTRYTYPE', 'paper')
                loader.add_value('ID', load_id(loader))
            else:
                loader = ItemLoader(item=Article(), selector=response)
                loader.default_output_processor = Join()
                loader.add_value('author', [i['name'] for i in data_dict['authors']])
                loader.add_value('title', data_dict['title'])
                loader.add_value('journal', data_dict['publicationTitle'])
                loader.add_value('publisher', data_dict['publisher'])
                loader.add_value('abstract', data_dict['abstract'])
                loader.add_value('year', data_dict['publicationYear'])
                loader.add_value('timestamp', data_dict['journalDisplayDateOfPublication'])
                loader.add_value('doi', data_dict['doi'])
                loader.add_value('url', self.start_urls[0])
                loader.add_value('ENTRYTYPE', 'article')
                loader.add_value('ID', load_id(loader))
            yield loader.load_item()


def load_id(loader):
    """
        ID is created by adding author and year

    :param loader: ItemLoader
    :return: ID (first name of author+year)

    """
    author = loader.get_output_value('author').split(' ')[0]
    year = loader.get_output_value('year')
    return author+year


