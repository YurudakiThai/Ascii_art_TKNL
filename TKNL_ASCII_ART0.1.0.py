from PIL import Image, ImageOps
import sys
import numpy as np

def stucki_dither(image):
    """Optimized Stucki dithering"""
    arr = np.array(image.convert("L"), dtype=np.float32)
    h, w = arr.shape

    weights = [
        (1, 0, 8),
        (2, 0, 4),
        (-2, 1, 2),
        (-1, 1, 4),
        (0, 1, 8),
        (1, 1, 4),
        (2, 1, 2),
        (-2, 2, 1),
        (-1, 2, 2),
        (0, 2, 4),
        (1, 2, 2),
        (2, 2, 1),
    ]
    total_weight = 42

    for y in range(h):
        for x in range(w):
            old = arr[y, x]
            new = 0 if old < 80 else 255
            arr[y, x] = new
            err = old - new
            for dx, dy, weight in weights:
                nx, ny = x + dx, y + dy
                if 0 <= nx < w and 0 <= ny < h:
                    arr[ny, nx] += err * weight / total_weight

    return Image.fromarray(np.clip(arr, 0, 255).astype("uint8"))

def resize_image(image_in, new_width=100):
    """Resize image maintaining aspect ratio"""
    width, height = image_in.size
    ratio = height / width
    new_height = int(new_width * ratio)
    return image_in.resize((new_width, new_height), Image.LANCZOS)

def braille_from_dots(dot_list):
    """Convert list of dot positions to Braille character"""
    base = 0x2800
    value = 0
    for dot in dot_list:
        if 1 <= dot <= 8:
            value |= 1 << (dot - 1)
    return chr(base + value)

def pixels_to_ascii(image):
    """Convert image to ASCII using Braille characters - Optimized version"""
    pixels = list(image.get_flattened_data())

    # Group pixels into pairs (2 pixels per group)
    matrix_pixels = [
        pixels[w : w + 2]
        for w in range(0, len(pixels), 2)
    ]

    # Reshape into 2D matrix (height x width/2)
    matrix_pixels = [
        matrix_pixels[round(image.width / 2) * i_ : round(image.width / 2) + round(image.width / 2) * i_]
        for i_ in range(0, image.height)
    ]

    # Pad last row if needed
    if len(matrix_pixels) > 1:
        matrix_pixels[-1] = matrix_pixels[-1] + [[0, 0]] * (
            len(matrix_pixels[-2]) - len(matrix_pixels[-1])
        )

    # Braille dot mapping: [[1, 4], [2, 5], [3, 6], [7, 8]]
    list_dot = [[1, 4], [2, 5], [3, 6], [7, 8]]
    list_num_toDot = []

    # Process in 4-row blocks
    for h_D4 in range(round(len(matrix_pixels) / 4)):
        h_D4bypart = matrix_pixels[4 * h_D4 : 4 + 4 * h_D4]
        for i_ in range(len(h_D4bypart)):
            for j_ in h_D4bypart[i_]:
                if j_[0] == 255 and j_[1] == 0:
                    list_num_toDot.append([list_dot[i_][0]])
                elif j_[0] == 0 and j_[1] == 255:
                    list_num_toDot.append([list_dot[i_][1]])
                elif j_[0] == 255 and j_[1] == 255:
                    list_num_toDot.append(list_dot[i_])
                else:
                    list_num_toDot.append([])

    # Reshape for width
    list_num_toDot = [
        list_num_toDot[round(image.width / 2) * i_ : round(image.width / 2) + round(image.width / 2) * i_]
        for i_ in range(0, round(image.height))
    ]

    # Flatten and group into 4-dot groups
    list_num_toDot_2 = []
    for h_D4 in range(round(len(list_num_toDot) / 4)):
        list_dot4 = list_num_toDot[4 * h_D4 : 4 + 4 * h_D4]
        for w_D2 in range(round(image.width / 2)):
            for i_ in list_dot4:
                list_num_toDot_2.append(i_[w_D2])

    # Group into 4-dot groups for Braille
    list_num_toDot_3 = []
    for list_point in range(round(len(list_num_toDot_2) / 4)):
        list_By4 = list_num_toDot_2[4 * list_point : 4 + 4 * list_point]
        list_plus = []
        for i in list_By4:
            list_plus.extend(i)
        list_num_toDot_3.append(list_plus)

    # Convert to Braille characters
    ascii_str = "".join(list(map(lambda x: braille_from_dots(x), list_num_toDot_3)))
    return ascii_str

def invert_RGBorRGBA(image_in):
    """Optimized image inversion"""
    if image_in.mode in ("RGBA", "P"):
        return ImageOps.invert(image_in.convert("RGB"))
    elif image_in.mode == "RGB":
        return ImageOps.invert(image_in)
    else:
        return ImageOps.invert(Image.merge("RGB", (image_in.split()[:3])))

def main(
    image_path_in: str,
    output_width=100,
    invert_yn: str = "n",
    image_path_OUT: str = "ascii_image.txt",
):
    """Main function to convert image to ASCII art"""
    try:
        image_ = Image.open(image_path_in)
    except Exception as e:
        print(f"\n{'Error: Not a valid image file'.center(110, '!')}\n")
        Show_title()
        return

    if invert_yn.lower() == "y":
        image_ = invert_RGBorRGBA(image_)

    image_ = resize_image(image_, output_width)
    image_ = image_.convert("L")
    image_ = stucki_dither(image_)

    ascii_str = pixels_to_ascii(image_)

    ascii_img = "\n".join(
        ascii_str[i_ : (i_ + (image_.width // 2))]
        for i_ in range(0, len(ascii_str), (image_.width // 2))
    )

    Text_re = "RESULT (ASCII ART)\n"
    print("=" * output_width + "\n")
    print(Text_re.center(output_width))
    print("=" * output_width + "\n")
    print(ascii_img)

    with open(image_path_OUT, "w", encoding="utf-8") as f:
        f.write(ascii_img)
    print(f"\nSuccess: ASCII art saved to {image_path_OUT}")

def Show_title():
    """Display program title and usage information"""
    Head_text = (
        "TKNL_ASCII_ART V.0.1.0 OPTIMIZED",
        "-->by Thanakrit Na-Lamphun [6804101333]",
    )
    HOW_text = (
        ">>Usage: python TKNL_ASCII_ART0.0.1.py <path_to_image> [width] [invert(y/n)] <path_out.txt>",
        ">>Example: python TKNL_ASCII_ART0.0.1.py Albert_Einstein.jpg 35 n Downloads/ascii_text.txt",
        ">>Note: [width] defaults to 100 px if not specified or invalid",
        ">>Note: Input must be a valid image file",
        ">>Note: <path_out.txt> must end with .txt, defaults to ascii_image.txt",
    )

    print("=" * len(HOW_text[0]))
    print(f"\n{' ' * int(0.5 * (len(HOW_text[0]) + 2 - len(Head_text[0])))}{Head_text[0]}")
    print(f"""
    {"███████████     █████     █████████".center(len(HOW_text[0]))}
    {"▒ ▓▓▓▓▓     ▓▓▓▓  ▓▓   ▓▓▓▓▓ ▓       ".center(len(HOW_text[0]))}
    {"█ ██ ███ ███ ███ ███ ██ ███ ██ █ v.OPT".center(len(HOW_text[0]))}
    """)

    print(f"{' ' * int(0.5 * (len(HOW_text[0]) - len(Head_text[1])))}{Head_text[1]}\n")
    print("=" * len(HOW_text[0]))
    print(f"\n{' ' * int(0.5 * (len(HOW_text[0]) - len('How it WORK')))}How it WORK\n")
    print(HOW_text[0])
    print(HOW_text[1])
    print(HOW_text[2])
    print(HOW_text[3])
    print(HOW_text[4])
    print("""
Example:
█
█████     █████     █████
█████     ████  ██   █████ █
    """)

if __name__ == "__main__":
    try:
        if len(sys.argv) < 2:
            Show_title()
            sys.exit(1)

        image_path_in = sys.argv[1]

        width = 100
        if len(sys.argv) > 2:
            try:
                width_val = int(sys.argv[2])
                if 0 < width_val <= 10000:
                    width = width_val
            except (ValueError, IndexError):
                width = 100

        invert_YN = "n"
        if len(sys.argv) > 3:
            invert_input = sys.argv[3].lower()
            if invert_input in ("y", "yes"):
                invert_YN = "y"
            elif invert_input in ("n", "no"):
                invert_YN = "n"

        image_path_out = "ascii_image.txt"
        if len(sys.argv) > 4:
            if sys.argv[4].endswith(".txt"):
                image_path_out = sys.argv[4]

        Text_list_show = (
            f"INPUT image path = {image_path_in}",
            f"WIDTH input = {width} px",
            f"[INVERT(y/n)] = {invert_YN}",
            f"OUTPUT image path = {image_path_out}",
        )
        print("\n" + f"{Text_list_show[0]}".center(width, ".") + "\n")
        print("\n" + f"{Text_list_show[1]}".center(width, ".") + "\n")
        print("\n" + f"{Text_list_show[2]}".center(width, ".") + "\n")
        print("\n" + f"{Text_list_show[3]}".center(width, ".") + "\n")

        main(image_path_in, width, invert_YN, image_path_out)

    except Exception as e:
        print(f"\n{'Error: Invalid command'.center(129, '!')}\n")
        print(f"{'Please check your input and try again.'.center(129, '!')}\n")
        print(f"{str(e)}".center(129))
        Show_title()       """
