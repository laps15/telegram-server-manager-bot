import config

from logging import Logger

def allowed_user(username: str, action: str) -> bool:
    if config.acl_enabled:
        try:
            acl = config.acl[username]
        except:
            try:
                acl = config.acl['default']
            except:
                acl = []
        if len(acl) < 1:
            return False
        return action in acl or "all" in acl and not ("~"+action) in acl

    return True


def authenticate_user(username: str, action: str, logger: Logger = None) -> bool:
    if not allowed_user(username, action):
        if logger is not None:
            logger.info("Unauthorized user(%s) requested action(%s)", username, action)
        return False
    return True
