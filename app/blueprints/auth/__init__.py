from flask import Blueprint ,request


bp = Blueprint(
    'auth',
    __name__,
    url_prefix='/auth',
    static_folder='static',
    template_folder='templates',
)


from . import views
