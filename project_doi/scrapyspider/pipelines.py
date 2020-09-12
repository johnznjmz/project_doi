from sqlalchemy.orm import sessionmaker
import os

basedir = os.path.abspath(os.path.dirname(__file__))


class DefaultValuesPipeline(object):
    def process_item(self, item, spider):
        for field in item.fields:
            item.setdefault(field, 'Not Present')
        return item



