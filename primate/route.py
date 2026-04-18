from __future__ import annotations

import inspect

from .i18n import I18N
from .request import Request
from .response import Response
from .session import Session, SessionInstance


def _make_verb_method(verb: str):
  def method(cls, func=None, *, content_type=None):
    def decorator(f):
      cls._bucket()[verb] = {"handler": f, "content_type": content_type}
      return f

    if func is not None:
      return decorator(func)
    return decorator

  return classmethod(method)


class Route:
  _scopes: dict[str, dict[str, dict]] = {}
  _current_scope: str = "__default__"

  Request = Request

  @classmethod
  def scope(cls, name: str) -> None:
    cls._current_scope = name
    cls._scopes.setdefault(name, {})

  @classmethod
  def current_scope(cls) -> str:
    return cls._current_scope

  @classmethod
  def clear(cls, name: str | None = None) -> None:
    if name is None:
      cls._scopes.clear()
      cls._current_scope = "__default__"
      return
    cls._scopes.pop(name, None)
    if cls._current_scope == name:
      cls._current_scope = "__default__"

  @classmethod
  def _bucket(cls, name: str | None = None) -> dict:
    key = name or cls._current_scope
    return cls._scopes.setdefault(key, {})

  @classmethod
  def registry(cls, name: str | None = None) -> dict:
    return cls._bucket(name).copy()

  @classmethod
  def set_session(cls, session_obj, helpers) -> None:
    session_instance = SessionInstance(session_obj, helpers)
    Session.set_current(session_instance)

  @classmethod
  def set_i18n(cls, i18n_obj) -> None:
    I18N.set_current(i18n_obj)

  @classmethod
  def call_route(cls, method: str, request, scope: str | None = None):
    bucket = cls._bucket(scope)
    entry = bucket.get(method.upper())
    if entry is None:
      return Response.error({"status": 404})
    return entry["handler"](request)

  @classmethod
  async def call_js(
    cls, scope, method, js_request, helpers_obj, session_obj, i18n_obj
  ):
    cls.set_session(session_obj, helpers_obj)
    cls.set_i18n(i18n_obj)
    req = cls.Request(js_request, helpers_obj)
    result = cls.call_route(method, req, scope)
    if inspect.isawaitable(result):
      result = await result
    return result


for _verb in [
  "GET",
  "POST",
  "PUT",
  "PATCH",
  "DELETE",
  "HEAD",
  "OPTIONS",
  "CONNECT",
  "TRACE",
]:
  setattr(Route, _verb.lower(), _make_verb_method(_verb))
