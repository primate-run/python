from .request import Request
from .response import Response
from .session import Session, SessionInstance


class Route:
  _routes = {}
  Request = Request

  @classmethod
  def get(cls, func):
    cls._routes["GET"] = func
    return func

  @classmethod
  def post(cls, func):
    cls._routes["POST"] = func
    return func

  @classmethod
  def put(cls, func):
    cls._routes["PUT"] = func
    return func

  @classmethod
  def patch(cls, func):
    cls._routes["PATCH"] = func
    return func

  @classmethod
  def delete(cls, func):
    cls._routes["DELETE"] = func
    return func

  @classmethod
  def head(cls, func):
    cls._routes["HEAD"] = func
    return func

  @classmethod
  def options(cls, func):
    cls._routes["OPTIONS"] = func
    return func

  @classmethod
  def connect(cls, func):
    cls._routes["CONNECT"] = func
    return func

  @classmethod
  def trace(cls, func):
    cls._routes["TRACE"] = func
    return func

  @classmethod
  def registry(cls):
    return cls._routes.copy()

  @classmethod
  def call_route(cls, method, request):
    handler = cls._routes.get(method.upper())
    if not handler:
      return Response.error({"status": 404})

    return handler(request)

  @classmethod
  def set_session(cls, session_obj, helpers):
    session_instance = SessionInstance(session_obj, helpers)
    Session.set_current(session_instance)
