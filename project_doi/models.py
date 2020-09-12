from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class Document(db.Model):
    """
            Class that represents basic DOI details

    The following attributes of a DOI are stored in this table:
        * author (author of the publication)
        * title (title of the publication)
        * doi (DOI of the publication)
        * url (the resolved URL)
        * ENTRYTYPE (The type of article, book, article, paper(Conference Paper)
        * ID (ID created using the first name of an author and the year of publication or in case of book the name of the author)

       """

    author = db.Column(db.String(256))
    title = db.Column(db.String(256))
    doi = db.Column(db.String(128), primary_key=True)
    url = db.Column(db.String(128))
    ENTRYTYPE = db.Column(db.String(128))
    ID = db.Column(db.String(128))
    __table_args__ = {'extend_existing': True}
    article = db.relationship('Article', lazy='select',
                              backref=db.backref('document', lazy='joined'))
    book = db.relationship('Book', lazy='select',
                           backref=db.backref('document', lazy='joined'))
    conferencepaper = db.relationship('ConferencePaper', lazy='select',
                                      backref=db.backref('document', lazy='joined'))


class Article(Document):
    """
           Class that represents  DOI details corresponding to an article.

       Inherited from class Document.
       The following attributes of a DOI are stored in this table:
           * journal (the name of the journal in which the article is published)
           * publisher ( name of the publisher of the article)
           * year ( the year of publication)
           * abstract ( the abstract of the publication )
           * timestamp ( the published date of the article)

   """
    journal = db.Column(db.String(128))
    publisher = db.Column(db.String(128))
    year = db.Column(db.String(32))
    abstract = db.Column(db.String(2048))
    timestamp = db.Column(db.Date())
    __tablename__ = 'Article'
    __table_args__ = {'extend_existing': True}
    doi = db.Column(None, db.ForeignKey('document.doi'), primary_key=True)


class Book(Document):
    """
               Class that represents  DOI details corresponding to a book.

       Inherited from class Document.
       The following attributes of a DOI are stored in this table:
           * publisher ( name of the publisher of the article)
           * chapters ( the number of chapters included in the book)
           * isbn ( the isbn of the book)
           * abstract ( the abstract of the publication )

       """
    publisher = db.Column(db.String(128))
    chapters = db.Column(db.String(32))
    isbn = db.Column(db.String(128))
    abstract = db.Column(db.String(2048))
    __tablename__ = 'Book'
    __table_args__ = {'extend_existing': True}
    doi = db.Column(None, db.ForeignKey('document.doi'), primary_key=True)


class ConferencePaper(Document):
    """
       Class that represents  DOI details corresponding to a Conference paper.

           Inherited from class Document.
           The following attributes of a DOI are stored in this table:
               * booktitle (the name of the journal in which the article is published)
               * publisher ( name of the publisher of the article)
               * year ( the year of publication)
               * abstract ( the abstract of the publication )
               * timestamp ( the published date of the article)

       """
    booktitle = db.Column(db.String(256))
    publisher = db.Column(db.String(128))
    year = db.Column(db.String(32))
    abstract = db.Column(db.String(2048))
    timestamp = db.Column(db.Date())
    __tablename__ = 'ConferencePaper'
    __table_args__ = {'extend_existing': True}
    doi = db.Column(None, db.ForeignKey('document.doi'), primary_key=True)
