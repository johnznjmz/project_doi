from .models import Article, Book, ConferencePaper, Document, db
from sqlalchemy import inspection
from sqlalchemy.exc import OperationalError


ENTRY_TYPE = 'ENTRYTYPE'
DOI = 'doi'
BOOK = 'book'
PAPER = 'paper'
ARTICLE = 'article'
CHAPTER = 'chapter'


def object_as_dict(obj):
    """
        The rows returned from table converted to dictionary with keys as column heading.

    :param obj: rows fron table as object
    :return: dictionary of rows

    """
    return {c.key: getattr(obj, c.key)
            for c in inspection.inspect(obj).mapper.column_attrs}


def check(dois):
    """
        Check Table Document for DOI 's and returns the list of DOI 's which are not present.

    :param dois: the list of DOI 's entered by user
    :return doi_temp: the list of DOI 's not present in the database

    """

    out = {'data': []}
    doi_temp = []
    for i in dois:
        data = Document.query.filter_by(doi=i).first()
        if data:
            out['data'].append(object_as_dict(data))
        else:
            doi_temp.append(i)
    return doi_temp


def read(dois):
    """
        Go through each of the tables and returns the bibliographical data as a dictionary.

    The rows returned from each table are saved to keys in the dictionary corresponding to the their entry type or the table name

    :param dois: the list of dois' entered by the user
    :return out_db: the dictionary of bibliographical data with respect to the list of details.
                    the dictionary has three keys, book, article, paper . Each of them pointing to
                    list of bibliographical data  based on the type of articles(ENTRYTYPE).

    """
    out_db = {BOOK: [],
              ARTICLE: [],
              PAPER: [],
              }
    out = {'data': []}
    doi_temp = []
    for i in dois:
        data = Document.query.filter_by(doi=i).first()
        if data:
            out['data'].append(object_as_dict(data))
        else:
            doi_temp.append(i)
    for i, j in out.items():
        for k in j:
            if k[ENTRY_TYPE] == BOOK:
                out_db[BOOK].append(object_as_dict(Book.query.filter_by(doi=k[DOI]).first()))
            elif k[ENTRY_TYPE] == PAPER or k[ENTRY_TYPE] == CHAPTER:
                out_db[PAPER].append(object_as_dict(ConferencePaper.query.filter_by(doi=k[DOI]).first()))
            else:
                out_db[ARTICLE].append(object_as_dict(Article.query.filter_by(doi=k[DOI]).first()))
    return out_db


def read_all():
    """
        To read all the entries present in the database.

    :return: dictionary containing each rows , separated based on the type of the entry

    """

    out_db = {BOOK: [object_as_dict(book) for book in Book.query.all()],
              ARTICLE: [object_as_dict(article) for article in Article.query.all()],
              PAPER: [object_as_dict(paper) for paper in ConferencePaper.query.all()],
              }
    if out_db.values():
        return out_db
    else:
        return 'No Entries'


def save(item):
    """
        Function to write the scraped data to the database.

    * The item is saved according to the ENTRYTYPE.
    * The item with ENTRYTYPE as book is saved to the Book
    * The item with ENTRYTYPE as paper or chapter is saved to the ConferencePaper
    * The item with ENTRYTYPE other than the above mentioned are saved to article

    :param item: Item retrieved using scrapy

    """
    from doi_app import app
    if item:
        if item[ENTRY_TYPE] == BOOK:
            def book(author, title, doi, url, ENTRYTYPE, ID, publisher, chapters, ISBN, abstract):
                return Book(author=author, title=title, doi=doi,
                            url=url, ENTRYTYPE=ENTRYTYPE, ID=ID,
                            publisher=publisher, chapters=chapters,
                            isbn=ISBN, abstract=abstract
                            )

            data = book(**item)
        elif item[ENTRY_TYPE] == PAPER or item[ENTRY_TYPE] == CHAPTER:
            def paper(author, title, doi, url, ENTRYTYPE, ID,
                      booktitle, publisher, year, abstract, timestamp):
                return ConferencePaper(author=author, title=title, doi=doi,
                                       url=url, ENTRYTYPE=ENTRYTYPE, ID=ID,
                                       booktitle=booktitle, publisher=publisher,
                                       year=year, abstract=abstract, timestamp=timestamp
                                       )

            data = paper(**item)
        else:
            def article(author, title, doi, url, ENTRYTYPE, ID,
                        journal, year, publisher, abstract, timestamp):
                return Article(author=author, title=title, doi=doi,
                               url=url, ENTRYTYPE=ENTRYTYPE, ID=ID, abstract=abstract,
                               journal=journal, year=year, publisher=publisher, timestamp=timestamp)

            data = article(**item)
        with app.app_context():
            db.session.add(data)
            db.session.commit()
