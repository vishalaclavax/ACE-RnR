from flask import Blueprint ,request


bp = Blueprint(
    'rewards',
    __name__,
    url_prefix='/rewards',
    static_folder='static',
    template_folder='templates',
)


from . import views
