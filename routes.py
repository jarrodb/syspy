# URL Routes
from tornado.web import URLSpec, StaticFileHandler
from settings import settings
import modules
import views
import api

routes = [
    URLSpec(r"/", views.core.IndexHandler, name="index"),
    ]

# API Routes
routes.extend([
    ])

# Admin
routes.extend([
    ])

# Static files
# - Production front-end should capture these requests, but
#   still allow us to reverse_url('static')in our templates.
routes.append(
    URLSpec(
        r"/static/(.*)",
        StaticFileHandler,
        dict(path=settings.static_path),
        name="static",
        )
    )
