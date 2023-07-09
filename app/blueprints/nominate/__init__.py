from flask import Blueprint ,request


bp = Blueprint(
    'nominate',
    __name__,
    url_prefix='/nominate',
    static_folder='static',
    template_folder='templates',
)


from . import views
