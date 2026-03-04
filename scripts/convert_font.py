from PIL import Image, ImageDraw, ImageFont
import numpy as np


def get_max_h(font, chars):
    result = 0
    for ch in chars:
        (_l, t, _r, b) = font.getbbox(ch)
        if b - t > result:
            result = b - t
    return result


def ascii_to_dict(
    font_path: str,
    goal_height: int = 16,
    img_size: int = 1280,
    threshold: int = 180,
) -> dict[str, list[int]]:
    ascii_chars = (
        [chr(i) for i in range(ord("A"), ord("Z") + 1)]
        + [chr(i) for i in range(ord("0"), ord("9") + 1)]
        + [
            "|",
            "/",
            "@",
            "&",
            "\\",
            "#",
            "$",
            "%",
            "^",
            "&",
            "*",
            "(",
            ")",
            "-",
            "+",
            "_",
        ]
    )
    font = ImageFont.truetype(font_path, img_size)

    max_h = get_max_h(font, ascii_chars)

    result = {}
    for ch in ascii_chars:
        img = Image.new("L", (img_size * 2, img_size * 2), color=255)
        draw = ImageDraw.Draw(img)
        (l, t, r, b) = font.getbbox(ch)
        x, y = 0, 0
        if l < 0:
            x = abs(l)
            r = r + abs(l)
            l = 0
        if t < 0:
            y = abs(t)
            b = t + abs(t)
        t = 0
        draw.text((x, y), ch, font=font, fill=0)

        # t = t + b - max_h 

        img = img.crop((l, t, r, b))
        print(ch)
        print((l, t, r, b))
        goal_width = int((r - l) / (b - t) * goal_height)
        # img.show()
        img = img.resize((goal_width, goal_height))
        arr = np.array(img)
        width = arr.shape[1]
        arr = (arr < threshold).astype(int)
        flat = arr.flatten().tolist()
        flat.append(width)

        result[ch] = flat
    return result


def print_bitmap(bitmap):
    width = bitmap[-1]
    j = 0
    for i in bitmap[:-1]:
        if i:
            print("██", end="")
        else:
            print("  ", end="")
        j += 1
        if j == width:
            j = 0
            print("")


if __name__ == "__main__":
    FONT_PATH = "calibri.ttf"

    bitmap_dict = ascii_to_dict(FONT_PATH)
    for k in bitmap_dict:
        print_bitmap(bitmap_dict[k])
        print("")
    # print(f"\nwidth 'A' = {width} px")
