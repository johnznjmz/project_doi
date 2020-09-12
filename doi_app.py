import os
import doi
from flask import (Flask, render_template, request, url_for,
                   redirect, flash, current_app)
from werkzeug.utils import secure_filename
from flask_classful import FlaskView, route
from flask_migrate import Migrate
from project_doi import (config, export, scrape, api)


app = Flask(__name__)
app.config.from_object(config.Config)
try:
    os.makedirs(app.instance_path)
except OSError:
    pass
try:
    os.makedirs(app.config['UPLOAD_FOLDER'])
except OSError:
    pass

from project_doi import models
db = models.db
db.init_app(app)
migrate = Migrate(app, db)

with app.app_context():
    db.create_all()

out_db = {'book': [],
          'article': [],
          'paper': [],
          }
doi_s = ''

api.ApiView.register(app, route_base='/api/')


class DOIView(FlaskView):
    """
            **Create application**

        * This creates an instance of the flask app and runs it
        * Doi is entered by the user , as text or as csv or json files
        * Check the validity of the doi
        * Check whether doi is present in the database if not the respected spider is called based on the domain name

    """

    route_base = '/'
    excluded_methods = ['allowed_file', 'upload_contents']

    @route('/')
    def index(self):
        """
            By Default Flask will come into this when we run the file.

        :return: search_doi.html file in search folder in templates folder.

        """
        return render_template("search/search_doi.html")

    @route('/', methods=['POST'])
    def search_doi(self):
        """
            Get Input from the user , validate and return the bibliographical details

        After clicking the submit button or search button , flask comes here.
        The values of DOI 's are obtained from the user either as string separated by comma or as a json or csv file.
        Uploaded files are saved in the Upload folder.
        The DOI 's are parsed and saved as a list , removed the duplicate ones.
        Validated the DOI 's by checking the correct format of DOI provided by DOI.org .
        The url link is obtained from doi.get_url_from_doi(doi).
        Check the database for the details for each doi.
        If DOI 's are not present in the database, the domains are saved as a list and Scrape object is called.
        The data corresponds to the DOI 's are obtained.

        :return: html page containing the bibliographical data

        """
        from project_doi import database

        global out_db, doi_s
        list_doi = []
        if request.method == 'POST':
            if 'doi' in request.form:
                list_doi = request.form['doi'].split(',')
            if 'file' in request.files:
                file = request.files['file']
                if file and self.allowed_file(file.filename):
                    filename = secure_filename(file.filename)
                    extension = file.filename.rsplit('.', 1)[1].lower()
                    path = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
                    file.save(path)
                    list_doi = self.upload_contents(extension, path)
                else:
                    flash('Please upload only csv and json formats')
            list_doi = list(dict.fromkeys(list_doi))
            doi_s = list_doi.copy()
            domain = {}
            for i in list_doi:
                try:
                    doi.validate_doi(i)
                    domain[i] = doi.get_real_url_from_doi(i)
                except ValueError:
                    flash(f'{i} : is not valid , please try again')
                    doi_s.remove(i)
            if doi_s is None:
                return redirect(url_for('DOIView:index'))
            doi_temp = database.check(doi_s)
            if doi_temp:
                doi_ = doi_temp
                domains = [domain[i] for i in doi_ if i in domain]
                doi_temp.clear()
                scrap = scrape.Scrape()
                scrap.scrape(domains, app.config['DICT_OF_SPIDERS'])
            out_db = database.read(doi_s)
        return render_template("search/search_doi.html", context=out_db)

    @route('/download/<int:file_bool>', methods=['GET', 'POST'])
    def download(self, file_bool):
        """
            Function to facilitate download.

        Any existing temporary files in the download path is removed.

        :param file_bool: True if the requested file type is JSON , False for Bibtex
        :return: file

        """
        global out_db
        temp_name, mimetype = export.export(out_db, file_bool)
        path = os.path.join(current_app.root_path, temp_name)

        def generate():
            with open(path) as f:
                yield from f
            os.remove(path)

        r = current_app.response_class(generate(), mimetype=mimetype)
        r.headers.set('Content-Disposition', 'attachment', filename=temp_name)
        return r

    def allowed_file(self, filename):
        """
            Check whether the file extensions present in the Allowed extensions.

        Allowed extensions are json and csv.

        :param filename: the name of the uploaded file
        :return: true if the file type is present in the ALLOWED_EXTENSIONS object

        """
        return '.' in filename and filename.rsplit('.', 1)[1].lower() in current_app.config['ALLOWED_EXTENSIONS']

    def upload_contents(self, extension, path):
        """
            DOI 's returned as list after parsing the uploaded files.

        Allowed extensions are json and csv.
        The file is removed after parsing the contents.

        :param extension: The file type of the uploaded file, csv or json
        :param path: path of the uploaded file
        :return: the parsed contents of the file as a list

        """
        import json
        import csv
        path = path
        if extension == 'csv':
            with open(path, newline='') as file:
                content = csv.reader(file, quotechar='|')
                list_of_doi = [j for i in content for j in i]
                while "" in list_of_doi:
                    list_of_doi.remove("")
        else:
            with open(path, 'r') as json_file:
                content = json.load(json_file)
                list_of_doi = [i for k, v in content.items() for i in v]

        if os.path.exists(path):
            os.remove(path)
        return list_of_doi


DOIView.register(app)
# db = SQLAlchemy()


if __name__ == '__main__':
    app.run(debug=True)
