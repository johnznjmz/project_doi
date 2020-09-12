import unittest
from flask_sqlalchemy import SQLAlchemy
import doi_app
import io

db = SQLAlchemy()
app = doi_app.app


class Tests(unittest.TestCase):

    def setUp(self):
        """
        Creates a new database for the unit test to use
        """
        self.client = app.test_client()
        self.client.SQLALCHEMY_DATABASE_URI = 'sqlite:///test.db'
        db.init_app(app)

    def tearDown(self):
        """
        Ensures that the database is emptied for next unit test
        """
        db.session.remove()
        with self.client.application.app_context():
            db.drop_all()

    def test_url(self):
        response_1 = self.client.get('/')
        response_2 = self.client.get('/api?doi=all', follow_redirects=True)
        response_3 = self.client.get('12:3.3')
        self.assertEqual(response_1.status_code, 200)
        self.assertEqual(response_2.status_code, 200)
        self.assertEqual(response_3.status_code, 404)

    def test_api(self):
        response_1 = self.client.get('/api?doi=10.1007/s11207-018-1308-3', follow_redirects=True)
        type_ = b'article'
        ID = b'Fabian2018'
        author = b'Fabian Menezes,Adriana Valio'
        doi = b'10.1007/s11207-018-1308-3'
        journal = b'Solar Physics'
        self.assertIn(type_, response_1.data)
        self.assertIn(ID, response_1.data)
        self.assertIn(author, response_1.data)
        self.assertIn(doi, response_1.data)
        self.assertIn(journal, response_1.data)

    def test_api_invalid(self):
        response_1 = self.client.get('/api?doi=x', follow_redirects=True)
        response_2 = self.client.get('/api', follow_redirects=True)
        self.assertIn(b'Invalid doi', response_1.data)
        self.assertIn(b'Error', response_2.data)

    def test_search_doi_invalid(self):
        response = self.client.post('/', data={'doi': "not a valid doi"})
        self.assertIn(b'not a valid doi : is not valid , please try again', response.data)

    def test_springer_book(self):
        response = self.client.post('/', data={'doi': "10.1007/978-3-319-94989-5"})
        publisher = b'Springer, Cham'
        chapters = b'6'
        isbn = b'978-3-319-94989-5'
        abstract = b'This book presents the Statistical Learning Theory in a detailed and easy to understand way'
        doi = b'10.1007/978-3-319-94989-5'
        author = b'Rodrigo Fernandes de Mello,Moacir Antonelli Ponti'
        title = b'Machine Learning'
        url = b'http://link.springer.com/10.1007/978-3-319-94989-5'
        Entrytype = b'book'
        ID = b'Rodrigo Fernandes de Mello,Moacir Antonelli Ponti'
        self.assertIn(publisher, response.data)
        self.assertIn(chapters, response.data)
        self.assertIn(isbn, response.data)
        self.assertIn(abstract, response.data)
        self.assertIn(doi, response.data)
        self.assertIn(author, response.data)
        self.assertIn(title, response.data)
        self.assertIn(url, response.data)
        self.assertIn(Entrytype, response.data)
        self.assertIn(ID, response.data)

    def test_springer_article(self):
        response = self.client.post('/', data={'doi': "10.1007/s10163-016-0545-5"})
        journal = b'Journal of Material Cycles and Waste Management'
        publisher = b'Springer'
        year = b'2017'
        abstract = b'Wastewater is discharged during washing processes in the production of biodiesel fuel (BDF)'
        timestamp = b'2016-09-23'
        doi = b'10.1007/s10163-016-0545-5'
        author = b'Jiro Kohda,Yasuhisa Nakano,Akimitsu Kugimiya,Yu Takano,Takuo Yano'
        title = b'Recycling of biodiesel fuel wastewater for use as a liquid fertilizer for hydroponics'
        url = b'https://link.springer.com/article/10.1007/s10163-016-0545-5'
        Entrytype = b'article'
        ID = b'Jiro2017'
        self.assertIn(journal, response.data)
        self.assertIn(publisher, response.data)
        self.assertIn(year, response.data)
        self.assertIn(abstract, response.data)
        self.assertIn(timestamp, response.data)
        self.assertIn(doi, response.data)
        self.assertIn(author, response.data)
        self.assertIn(title, response.data)
        self.assertIn(url, response.data)
        self.assertIn(Entrytype, response.data)
        self.assertIn(ID, response.data)

    def test_springer_paper(self):
        response = self.client.post('/', data={'doi': '10.1007/978-3-030-00713-3_20'})
        booktitle = b'Exploring Service Science'
        publisher = b'Springer, Cham'
        year = b'2018'
        abstract = b'To ensure availability of industrial machines and reducing breakdown times'
        timestamp = b'2018-09-19'
        doi = b'10.1007/978-3-030-00713-3_20'
        author = b'Daniel Olivotti,Jens Passlick,Alexander Axjonow,Dennis Eilers,Michael H. Breitner'
        title = b'Combining Machine Learning and Domain Experience: A Hybrid-Learning Monitor Approach for Industrial Machines'
        url = b'https://link.springer.com/chapter/10.1007/978-3-030-00713-3_20'
        Entrytype = b'paper'
        ID = b'Daniel2018'
        self.assertIn(booktitle, response.data),
        self.assertIn(publisher, response.data),
        self.assertIn(year, response.data),
        self.assertIn(abstract, response.data),
        self.assertIn(timestamp, response.data),
        self.assertIn(doi, response.data),
        self.assertIn(author, response.data),
        self.assertIn(title, response.data),
        self.assertIn(url, response.data),
        self.assertIn(Entrytype, response.data),
        self.assertIn(ID, response.data)

    def test_wiley_article(self):
        response = self.client.post('/', data={'doi': "10.1002/2017GL074677"})
        journal = b'Geophysical Research Letters'
        publisher = b'John Wiley'
        year = b'2017'
        abstract = b'Machine learning appears to discern the frictional state when applied to laboratory seismic'
        timestamp = b'2017-09-22'
        doi = b'10.1002/2017GL074677'
        author = b'Claudia Hulbert,Nicholas Lubbers,Kipton Barros'
        title = b'Machine Learning Predicts Laboratory Earthquakes'
        url = b'https://agupubs.onlinelibrary.wiley.com/doi/10.1002/2017GL074677'
        Entrytype = b'article'
        ID = b'Bertrand2017'
        self.assertIn(journal, response.data)
        self.assertIn(publisher, response.data)
        self.assertIn(year, response.data)
        self.assertIn(abstract, response.data)
        self.assertIn(timestamp, response.data)
        self.assertIn(doi, response.data)
        self.assertIn(author, response.data)
        self.assertIn(title, response.data)
        self.assertIn(url, response.data)
        self.assertIn(Entrytype, response.data)
        self.assertIn(ID, response.data)

    def test_wiley_paper(self):
        response = self.client.post('/', data={'doi': '10.1002/9781119505914.ch7'})
        booktitle = b'INFORMS Analytics Body of Knowledge'
        publisher = b'John Wiley'
        year = b'2018'
        abstract = b'This chapter provides an overview of machine learning using automated algorithms'
        timestamp = b'2018-09-26'
        doi = b'10.1002/9781119505914.ch7'
        author = b'Samuel H. Huddleston,Gerald G. Brown,Samuel H. Huddleston'
        title = b'Machine Learning'
        url = b'https://onlinelibrary.wiley.com/doi/10.1002/9781119505914.ch7'
        Entrytype = b'chapter'
        ID = b'Samuel2018'
        self.assertIn(booktitle, response.data),
        self.assertIn(publisher, response.data),
        self.assertIn(year, response.data),
        self.assertIn(abstract, response.data),
        self.assertIn(timestamp, response.data),
        self.assertIn(doi, response.data),
        self.assertIn(author, response.data),
        self.assertIn(title, response.data),
        self.assertIn(url, response.data),
        self.assertIn(Entrytype, response.data),
        self.assertIn(ID, response.data)

    def test_ieee_article(self):
        response = self.client.post('/', data={'doi': "10.1109/TPAMI.2008.235"})
        journal = b'IEEE Transactions on Pattern Analysis and Machine Intelligence'
        publisher = b'IEEE'
        year = b'2009'
        abstract = b'Semi-supervised learning has attracted a significant amount of attention'
        timestamp = b'2008-09-26'
        doi = b'10.1109/TPAMI.2008.235'
        author = b'Pavan Kumar Mallapragada,Rong Jin,Anil K. Jain,Yi Liu'
        title = b'SemiBoost: Boosting for Semi-Supervised Learning'
        url = b'http://ieeexplore.ieee.org/document/4633363/'
        Entrytype = b'article'
        ID = b'Pavan2009'
        self.assertIn(journal, response.data)
        self.assertIn(publisher, response.data)
        self.assertIn(year, response.data)
        self.assertIn(abstract, response.data)
        self.assertIn(timestamp, response.data)
        self.assertIn(doi, response.data)
        self.assertIn(author, response.data)
        self.assertIn(title, response.data)
        self.assertIn(url, response.data)
        self.assertIn(Entrytype, response.data)
        self.assertIn(ID, response.data)

    def test_ieee_paper(self):
        response = self.client.post('/', data={'doi': '10.1109/ULTSYM.1994.401941'})
        booktitle = b'1994 Proceedings of IEEE Ultrasonics Symposium'
        publisher = b'IEEE'
        year = b'1994'
        abstract = b'The design of a new wideband, quantitative shock wave hydrophone is presented'
        timestamp = b'1994-01-01'
        doi = b'10.1109/ULTSYM.1994.401941'
        author = b'M. Schafer,T. Kraynak,V. Krakhman'
        title = b'Development of a cost-effective shock wave hydrophone'
        url = b'http://ieeexplore.ieee.org/document/401941/'
        Entrytype = b'paper'
        ID = b'M.1994'
        self.assertIn(booktitle, response.data),
        self.assertIn(publisher, response.data),
        self.assertIn(year, response.data),
        self.assertIn(abstract, response.data),
        self.assertIn(timestamp, response.data),
        self.assertIn(doi, response.data),
        self.assertIn(author, response.data),
        self.assertIn(title, response.data),
        self.assertIn(url, response.data),
        self.assertIn(Entrytype, response.data),
        self.assertIn(ID, response.data)

    def testUpload(self):
        response = self.client.post(
            '/',
            data={
                'file': (io.BytesIO(b'my file contents'), 'doi.csv'),
            }, follow_redirects=True, content_type='multipart/form-data'
        )
        self.assertEqual(response.status_code, 200)


if __name__ == '__main__':
    unittest.main()
