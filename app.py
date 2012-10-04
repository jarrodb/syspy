import tornado.httpserver
import tornado.ioloop
import tornado.web
from settings import settings
from routes import routes
from models import engine

settings.engine = engine

tornapp = tornado.web.Application(routes, **settings)

