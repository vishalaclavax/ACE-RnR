from flask import Blueprint ,request


bp = Blueprint(
    'awards',
    __name__,
    url_prefix='/awards',
    static_folder='static',
    template_folder='templates',
)


from . import views
