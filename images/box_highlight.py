

from PIL import Image, ImageDraw, ImageFilter

def get_artifact_box(element_color: str, quality_color: str):
    img = Image.new("RGB", (600, 600), "white")
    draw = ImageDraw.Draw(img)

    box_x = 100
    box_y = 100
    box_w = box_x + 280
    box_h = box_y + 200

    shadow_blur = 3

    draw.rectangle((box_x, box_y, box_x + box_w, box_y + box_h), fill="blue")

    shadow_img = Image.new("RGBA", (600, 600), "black")
    shadow_draw = ImageDraw.Draw(shadow_img)
    shadow_draw.rounded_rectangle(
        (box_x, box_y, box_x + box_w, box_y + box_h),
        radius=10,
        fill=quality_color
    )

    blur_intensity = 15
    for _ in range(blur_intensity):
        shadow_img = shadow_img.filter(ImageFilter.GaussianBlur(shadow_blur))

    img.paste(shadow_img, (0, 0), shadow_img)

    draw.rounded_rectangle(
        (box_x + 7, box_y + 7, box_x + box_w - 7, box_y + box_h - 7),
        radius=10,
        fill=element_color
    )

    return img
