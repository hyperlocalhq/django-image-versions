from pilkit.processors import ResizeCanvas


def resize_canvas_process(self, img):
    from PIL import Image
    from pilkit.processors import Anchor

    original_width, original_height = img.size

    if self.anchor:
        anchor = Anchor.get_tuple(self.anchor)
        anchor_x = original_width * anchor[0]
        anchor_y = original_height * anchor[1]
        delta_x = self.width - original_width
        delta_y = self.height - original_height
        if delta_y == 0:
            # taller image than original
            if anchor_x > original_width - self.width / 2:
                anchor_x = original_width - self.width / 2
            elif anchor_x < self.width / 2:
                anchor_x = self.width / 2
            x = self.width / 2 - anchor_x
            y = 0
        else:
            # wider image than original
            if anchor_y > original_height - self.height / 2:
                anchor_y = original_height - self.height / 2
            elif anchor_y < self.height / 2:
                anchor_y = self.height / 2
            x = 0
            y = self.height / 2 - anchor_y
        x = int(x)
        y = int(y)
    else:
        x, y = self.x, self.y

    new_img = Image.new("RGBA", (self.width, self.height), self.color)
    new_img.paste(img, (x, y))
    return new_img


# Monkey-patching the ResizeCanvas.process() method
ResizeCanvas.process = resize_canvas_process
