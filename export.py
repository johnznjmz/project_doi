import json
import tempfile
import os
from pathlib import Path
import bibtexparser
from bibtexparser.bibdatabase import BibDatabase


def export(data, file_bool):
    """
        Convert the data to json or bibtex and write to a temporary file.

    :param data: The data containing the bibliographical details
    :param file_bool: True for the file to be exported as json False for bibtex format
    :return: the filename and the mimetype

    """
    data_ = [k for i, j in data.items() if j for k in j]

    for i in data_:
        try:
            if 'timestamp' in i:
                i['timestamp'] = i['timestamp'].strftime('%Y/%m/%d')
        except AttributeError:
            pass
        for k in i:
            i[k] = str(i[k])

    path = Path(os.path.abspath(os.path.dirname(__file__))).parent
    if file_bool:
        mimetype = 'application/json'
        with tempfile.NamedTemporaryFile(dir=path, delete=False, suffix='.json') as temp:
            temp.write(bytes(json.dumps(data_), encoding='utf-8'))
    else:
        mimetype = 'application/x-bibtex'
        bib_db = BibDatabase()
        bib_db.entries = data_
        bibtex_str = bibtexparser.dumps(bib_db)
        with tempfile.NamedTemporaryFile(dir=path, delete=False, suffix='.bib') as temp:
            temp.write(bytes(bibtex_str, encoding='utf-8'))

    return temp.name.split('\\')[-1], mimetype
