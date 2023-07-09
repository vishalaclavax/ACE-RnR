from flask import Blueprint ,request


bp = Blueprint(
    'notifications',
    __name__,
    url_prefix='/notifications',
    static_folder='static',
    template_folder='templates',
)


from . import views
