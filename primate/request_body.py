from .readable import Readable
from .uploaded_file import UploadedFile


class Multipart:
  def __init__(self, form, files):
    self.form = form
    self.files = files


class RequestBody:
  def __init__(self, body, helpers):
    self.body = body
    self.helpers = helpers

  def json(self):
    import json

    return json.loads(str(self.body.jsonSync()))

  def text(self):
    return str(self.body.textSync())

  def form(self):
    import json

    return json.loads(str(self.body.formSync()))

  def multipart(self):
    import json

    form = json.loads(str(self.body.formSync()))
    files_js = self.body.filesSync()
    files = []
    for i in range(files_js.length):
      f = files_js[i]
      files.append(
        UploadedFile(
          field=str(f.field),
          name=str(f.name),
          type=str(f.type),
          size=int(f.size),
          bytes_data=f.bytes,
        )
      )
    return Multipart(form, files)

  def blob(self):
    return Readable(self.body.blobSync(), str(self.body.blobTypeSync()))
