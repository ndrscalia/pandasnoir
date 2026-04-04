from PIL import Image
from rich_pixels import Pixels
from textual.widget import Widget


class Mascot(Widget):
    def __init__(self, image_path, sizes: tuple, title: str, **kwargs):
        super().__init__(**kwargs)
        self.border_title = title
        with Image.open(image_path) as img:
            img = img.resize(sizes, Image.Resampling.NEAREST)
            self.pixels = Pixels.from_image(img)

    def render(self):
        return self.pixels
