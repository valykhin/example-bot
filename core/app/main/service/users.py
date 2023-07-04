import logging.config
from sqlalchemy.exc import IntegrityError, NoResultFound
from sqlalchemy.orm import attributes

from core.app.extensions import db
from ..dto.exceptions import InvalidUsage
from ..model.user import User

logger = logging.getLogger('core')


def get_users(telegram_id=None):
    logger.info("Get user list, filter by {}".format([telegram_id]))
    users = User.query.filter(User.telegram_id == telegram_id) if telegram_id is not None else User.query.all()
    logger.info("Read users: {}".format(users))
    return users


def get_user(user_id):
    logger.info("Get user by id: {}".format(user_id))
    user = User.query.filter(User.id == user_id).one()
    logger.info("Read user {} with name: {}".format(user.id, user.name))
    return user


def create_user(data):
    logger.info("Create user name: {}, telegram_id: {}".format(data.get('name'), data.get('telegram_id')))
    try:
        telegram_id = data['telegram_id']
        user = None
        if telegram_id:
            logger.info("Check if user with telegram_id: {} exists".format(data['telegram_id']))
            try:
                user = User.query.filter(User.telegram_id == telegram_id).one()
            except NoResultFound:
                logger.info("User with telegram_id: {} not exist".format(data['telegram_id']))
        if not user:
            user = User.from_dict(data).save()
    except IntegrityError as err:
        logger.error("Error occurred while creating user in DB: {}".format(err.detail))
        db.session.rollback()
        raise InvalidUsage.unknown_error()
    except AttributeError as err:
        logger.error("Error occurred while creating user in DB: {}".format(err.name))
        raise InvalidUsage.unknown_error()
    logger.info("Created user {} with name: {}".format(user.id, user.name))
    return user


def delete_user(user_id):
    logger.info("Delete user by id: {}".format(user_id))
    user = User.query.filter_by(id=int(user_id)).one()
    User.query.filter_by(id=int(user_id)).delete()
    db.session.commit()
    logger.info("Deleted user {} with name: {}".format(user.id, user.name))
    return user


def patch_user(user_id, data):
    logger.info("Patch user with id: {}".format(user_id))
    user = User.query.filter(User.id == user_id).one()
    for key, value in data.items():
        if key == 'settings':
            user.settings.update(value)
        else:
            setattr(user, key, value)
    attributes.flag_modified(user, 'settings')
    db.session.commit()
    logger.info("Patched user {} with name: {}".format(user.id, user.name))
    return user
