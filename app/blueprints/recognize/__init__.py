from flask import Blueprint ,request


bp = Blueprint(
    'recognize',
    __name__,
    url_prefix='/recognize',
    static_folder='static',
    template_folder='templates',
)


from . import views
