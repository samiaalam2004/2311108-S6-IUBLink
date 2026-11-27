from models.user import USERS_SQL, USERS_ALTER_SQL
from models.post import POSTS_SQL
from models.session import SESSIONS_SQL
from models.audit import AUDIT_LOGS_SQL, LOGIN_ATTEMPTS_SQL

ALL_TABLES = [
    USERS_SQL,
    *USERS_ALTER_SQL,
    POSTS_SQL,
    SESSIONS_SQL,
    AUDIT_LOGS_SQL,
    LOGIN_ATTEMPTS_SQL,
]