from scrapy.item import Item, Field
import re
from scrapy.loader.processors import MapCompose, Join, TakeFirst
import datetime


def filter_number(value):
    """
            The digits are extracted for chapters

    :param value: string
    :return: integer

    """
    return re.search(r'\d+', value).group()


def date_convert(value):
    """
        The date is parsed to python datetime (default: current time)

    :param value: date as string
    :return: datetime.datetime

    """
    date_format = ["%Y/%m/%d", "%Y-%m-%d", "%Y/%m", "%Y", "%b. %Y", "%d %B %Y"]
    for i in date_format:
        try:
            create_date = datetime.datetime.strptime(value, i).date()
            return create_date
        except ValueError:
            pass
    return datetime.datetime.now().date()


class Document(Item):
    """
        Defines your fields for Item

       * author (author of the publication)
       * title (title of the publication)
       * doi (DOI of the publication)
       * url (the resolved URL)
       * ENTRYTYPE (The type of article, book, article, paper(Conference Paper)
       * ID (ID created using the first name of an author and the year of publication or in case of book the name of the author)

    """
    author = Field(
        input_processor=MapCompose(lambda v: v.replace(u'\xa0', u' ')),
        output_processor=Join(separator=',')
    )
    title = Field()
    doi = Field()
    url = Field()
    ENTRYTYPE = Field(
        input_processor=MapCompose(lambda v: v.lower())
    )
    ID = Field()


class Article(Document):
    """
           Class that represents fields for the item corresponding to an article.

           Inherited from class Document.
           The following attributes of a DOI are stored in this table:
               * journal (the name of the journal in which the article is published)
               * publisher ( name of the publisher of the article)
               * year ( the year of publication)
               * abstract ( the abstract of the publication )
               * timestamp ( the published date of the article)

       """
    journal = Field()
    publisher = Field(output_processor=Join(separator=','))
    year = Field(
        input_processor=MapCompose(lambda v: v.split('/')[0] or v.split('-')[0] or v[0], str),
    )
    abstract = Field()
    timestamp = Field(
        input_processor=MapCompose(date_convert),
        output_processor=TakeFirst()
    )


class Book(Document):
    """
           Class that represents  fields for the item  corresponding to a book.

           Inherited from class Document.
           The following attributes of a DOI are stored in this table:
               * publisher ( name of the publisher of the article)
               * chapters ( the number of chapters included in the book)
               * isbn ( the isbn of the book)
               * abstract ( the abstract of the publication )

           """
    publisher = Field(
        output_processor=Join(separator=',')
    )
    chapters = Field(
        input_processor=MapCompose(filter_number, int),
        output_processor=TakeFirst()
    )
    ISBN = Field()
    abstract = Field()


class ConferencePaper(Document):
    """
           Class that represents fields for the item corresponding to a Conference paper.

               Inherited from class Document.
               The following attributes of a DOI are stored in this table:
                   * booktitle (the name of the journal in which the article is published)
                   * publisher ( name of the publisher of the article)
                   * year ( the year of publication)
                   * abstract ( the abstract of the publication )
                   * timestamp ( the published date of the article)

           """
    booktitle = Field()
    publisher = Field(output_processor=Join(separator=','))
    year = Field(
        input_processor=MapCompose(lambda v: v.split('/')[0] or v.split('-')[0] or v[0], str),
    )
    abstract = Field(input_processor=MapCompose(lambda v: v.rsplit(), str)
                     )
    timestamp = Field(
        input_processor=MapCompose(date_convert),
        output_processor=TakeFirst()
    )
