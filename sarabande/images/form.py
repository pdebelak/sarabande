from io import BytesIO

from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileRequired
from PIL import Image as PIL
from werkzeug.utils import secure_filename

from sarabande.models import Image


class ImageForm(FlaskForm):
    class Meta:
        csrf_enabled = False

    upload = FileField(validators=[FileRequired()])

    def to_image(self, user=None):
        image = self._thumbnail_image()
        return Image(
            name=self._filename,
            mimetype=self.upload.data.mimetype,
            image=image,
            user=user,
        )

    def _thumbnail_image(self):
        image = PIL.open(self.upload.data.stream)
        image.thumbnail((400, 400))
        data = BytesIO()
        image.save(data, format=image.format)
        data.seek(0)
        return data.read()

    @property
    def _filename(self):
        return secure_filename(self.upload.data.filename)
