import models
from app import db
from logzero import logger
from sqlalchemy import exc


def session_commit():
    try:
        db.session.commit()
    except exc.SQLAlchemyError as e:
        logger.error(e)
        db.session.rollback()


class Create:
    @staticmethod
    def store_media_file(name, file):
        new_file = models.Media(name=name, data=file)
        db.session.add(new_file)
        session_commit()

        return new_file.id


class Read:
    @staticmethod
    def file_by_media_id(media_id):
        try:
            file_data = models.Media.query.filter_by(id=media_id).first()
        except exc.SQLAlchemyError as e:
            logger.error(e)
            db.session.rollback()

        return file_data
