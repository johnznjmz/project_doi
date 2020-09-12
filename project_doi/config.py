import os
from project_doi.scrapyspider.spiders import springer_doi, wiley_doi, ieee_doi

SpringerDoi = springer_doi.SpringerDoi
WileyDoi = wiley_doi.WileyDoi
IeeeDoi = ieee_doi.IeeeDoi
basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    """
            **Config**

    Contains all the configurations for flask:
     * SQLALCHEMY_DATABASE_URI = 'sqlite:///app.db'
     * SQLALCHEMY_TRACK_MODIFICATIONS = False
     * SECRET_KEY = 'dev'
     * ALLOWED_EXTENSIONS = {'csv', 'json'}
     * DICT_OF_SPIDERS = {'springer': SpringerDoi, 'wiley': WileyDoi, 'ieee': IeeeDoi}
     * UPLOAD_FOLDER = os.path.join(basedir, 'uploads')

    """
    SQLALCHEMY_DATABASE_URI = 'sqlite:///app.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = 'dev'
    ALLOWED_EXTENSIONS = {'csv', 'json'}
    DICT_OF_SPIDERS = {'springer': SpringerDoi, 'wiley': WileyDoi, 'ieee': IeeeDoi}
    UPLOAD_FOLDER = os.path.join(basedir, 'uploads')

