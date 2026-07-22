from PIL import Image, ImageOps
import sys
import numpy as np

# ชุดตัวอักษร ASCII ที่ใช้แทนความเข้มของพิกเซล (จากเข้มไปอ่อน)
Ascii_chars = []
# ย้อนจากอ่อนไปเข้ม


def stucki_dither(image):
    arr = np.array(image.convert("L"), dtype=np.float32)
    h, w = image.height, image.width
    print(w, h)
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

    for y in range(h):
        for x in range(w):
            old = arr[y, x]
            new = 0 if old < 80 else 255
            # new = old
            arr[y, x] = new
            err = old - new
            for dx, dy, weight in weights:
                nx, ny = x + dx, y + dy
                if 0 <= nx < w and 0 <= ny < h:
                    arr[ny, nx] += err * weight / 42
    return Image.fromarray(np.clip(arr, 0, 255).astype("uint8"))


def resize_image(image_in, new_width=100):
    """ปรับขนาดภาพให้กว้างตามที่กำหนด โดยรักษาอัตราส่วน"""
    width, height = image_in.size
    # ปรับอัตราส่วนสำหรับ ASCII (เพราะตัวอักษรไม่เป็นสี่เหลี่ยมจตุรัส)
    ratio = (height) / (width)
    new_height = int(new_width * ratio)
    resized_image = image_in.resize((new_width, new_height))
    return resized_image





# อันนี้ประสิทธิภาพมากที่สุด
def pixels_to_ascii(image):
    # แปลงพิกเซลเป็นตัวอักษร ASCII ตามความเข้ม
    pixels = list(image.getdata())
    print("pixels's len", len(pixels))

    matrix_pixels = list(map(lambda w: pixels[w : w + 2], range(0, len(pixels), 2)))
    print("width/2", len(matrix_pixels))
    matrix_pixels = [
        matrix_pixels[
            round(image.width / 2) * i_ : round(image.width / 2)
            + round(image.width / 2) * i_
        ]
        for i_ in range(0, image.height)
    ]
    matrix_pixels[-1] = matrix_pixels[-1] + [[0, 0]] * (
        len(matrix_pixels[-2]) - len(matrix_pixels[-1])
    )
    print("width/4", len(matrix_pixels))
    n_4d = round(image.height) if len(matrix_pixels) >= 4 else exit(Show_title())
    print("n_4d", n_4d)
    # list_num_toDot = [j_ for i_ in list_num_toDot for j_ in i_]
    fact_widt = round(image.width)
    """จัดเรียงครั้ง 1"""

    list_num_toDot = []
    list_dot = [[1, 4], [2, 5], [3, 6], [7, 8]]
    for h_D4 in range(round(len(matrix_pixels) / 4)):
        h_D4bypart = matrix_pixels[4 * h_D4 : 4 + 4 * h_D4 :]
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

    print("list_num_toDot", len(list_num_toDot))
    list_num_toDot = [
        list_num_toDot[
            round(image.width / 2) * i_ : round(image.width / 2)
            + round(image.width / 2) * i_
        ]
        for i_ in range(0, round(image.height))
    ]
    print("list_num_toDot", len(list_num_toDot))
    # ได้ชุดตัวเลขขนาด width*height
    print("list_num_toDot_2", len(list_num_toDot))
    list_num_toDot_2 = []
    """จัดเรียงครั้ง 2"""
    for h_D4 in range(round(len(list_num_toDot) / 4)):
        list_dot4 = list_num_toDot[4 * h_D4 : 4 + 4 * h_D4 :]
        for w_D2 in range(round(image.width / 2)):
            for i_ in list_dot4:
                # point_i = i_[w_D2]
                list_num_toDot_2.append(i_[w_D2])
    print("list_num_toDot_2", len(list_num_toDot_2))
    """จัดเรียงครั้ง 3"""
    list_num_toDot_3 = []
    for list_point in range(round(len(list_num_toDot_2) / 4)):
        list_By4 = list_num_toDot_2[4 * list_point : 4 + 4 * list_point :]
        list_plus = []
        for i in list_By4:
            list_plus.extend(i)
        list_num_toDot_3.append(list_plus)

    # print(point_i) #list_B = [ k for k in list_A ]
    # print("--",point_i ,len(list_B))
    # list_num_toDot = list(map(lambda x: list_num_toDot[x:x+2],range(0,len(list_num_toDot),2)))

    # print("list_dot--",(list_num_toDot))
    # list_num_toDot = list(map(lambda k: list_num_toDot[round(image.width)*k:round(image.width)+round(image.width)*k:] ,list(range(image.height))))
    # list_num_toDot_beta = [i_[1] for i_ in list_num_toDot]
    # list_partternStack = list_partternStack*2
    # list_partternStack = list_partternStack [:len(list_partternStack):]
    # print(len(list_partternStack))
    # i_ = round(len(list_partternStack)/((image.width/4)))-1
    # dot_list_part = [list_partternStack[round(image.width/4)*i_1:round(image.width/4)+round(image.width/4)*i_1:][i_point][1] for i_point in range(fact_widthD4) for i_1 in range(i_)]
    # for i_point in range(fact_widthD4):
    # for i_1 in range(i_):
    # print(list_partternStack[round(image.width/4)*i_1:round(image.width/4)+round(image.width/4)*i_1:][i_point])

    # print(len(dot_list_part))

    print(len(list_num_toDot))
    """
    for w_ in range(round(len(list_num_toDot)/4)):
        list_4dot = list_num_toDot[4*w_:4+(4)*w_:]
        list_4dot = [ j for i in list_4dot for j in i]
        list_num_toDot_2.append(list_4dot)
        print()
    """

    print(len(list_num_toDot_2))

    def braille_from_dots(dot_list):
        base = 0x2800  # จุดเริ่มต้นของ Braille Patterns
        value = 0
        for dot in dot_list:
            if 1 <= dot <= 8:
                value |= 1 << (dot - 1)
        return chr(base + value)

    """
    dot_result = []

    for k_ in range(round(len(dot_list_part)/4)):
        list_4dot  = dot_list_part[4*k_:4+4*k_:]
        list_4dot = [j_ for i_ in list_4dot for j_ in i_]
        dot_result.append(list_4dot)
    print(len(dot_result))
    """

    # dot_result.append(braille_from_dots([*list_4dot[0],*list_4dot[1],*list_4dot[2],*list_4dot[3]]))

    """
    ascii_str = "".join(
        list(
            map(lambda x: Ascii_chars[int(
                x / (255 / (len(Ascii_chars) - 1)))], pixels)
        )
    )
    """
    ascii_str = "".join(list(map(lambda x: braille_from_dots(x), list_num_toDot_3)))
    return ascii_str


def pixels_to_ascii_dot(image):
    pixels_image = list(image.getdata())

    ascii_str_dots = "".join(
        list(map(lambda dot_1: chr(10240 + dot_1), pixels_image))
    )  # [::-1] ทำาให้กลับหัว
    return ascii_str_dots


def invert_RGBorRGBA(image_in):
    # print(image_in.mode)
    if image_in.mode == "RGBA" or image_in.mode == "P":
        image_inRGB = image_in.convert("RGB")
        return ImageOps.invert(image_inRGB)
    else:
        return ImageOps.invert(Image.merge("RGB", (image_in.split()[:3:])))


def main(
    image_path_in: str,
    output_width=100,
    invert_yn: str = "n",
    image_path_OUT: str = "Downloads/ascii_image.txt",
):  # Defuilt ไว้ 100 px
    try:
        # เปิดภาพ
        image_ = Image.open(image_path_in)
    except Exception as e:
        print(f"{e}".split()[-1].center(110, "!") + "\n")
        print("These file is not image".upper().center(110, "!"))
        Show_title()
        return
    # print(image_)
    # image_ = ImageOps.invert(image_.convert('RGB'))  # กลัยสีรูป
    if invert_yn.lower() == "y":
        image_ = invert_RGBorRGBA(image_)
    # แปลงภาพ
    image_ = resize_image(image_, output_width)
    image_ = image_.convert("L")  # เปลี่ยนภาพเป็นขาวดำา
    image_ = stucki_dither(image_)

    # แปลงเป็น ASCII
    ascii_str = pixels_to_ascii(image_)
    # print(ascii_str)
    # Loop จัดตัวอักขระ(แถว)เป็นรูป
    ascii_img = "\n".join(
        list(
            map(
                lambda i_: ascii_str[i_ : (i_ + round((image_.width) / 2))],
                list(range(0, len(ascii_str), round((image_.width) / 2))),
            )
        )
    )

    # แสดงผล
    Text_re = "RESULT (ผลลัพธ์)\n"
    print("=" * output_width + "\n")
    print(Text_re.center(output_width))  # ทำาให้ข้อความอยู่ตรงกลาง
    print("=" * output_width + "\n")
    print((ascii_img))

    # บันทึกเป็นไฟล์ .txt (optional)
    with open(image_path_OUT, "w", encoding="utf-8") as f:
        f.write(ascii_img)
    print(f"\n,/ Save ASCII art to a file: {image_path_OUT} SUCCESS")


def Show_title():
    Head_text = (
        "TKNL_ASCII_ART V.0.1.0",
        "-->by Thanakrit Na-Lamphun [6804101333]",
    )
    HOW_text = (
        ">>วิธีการใช้งาน: python <file_path>/TKNL_ASCII_ART0.0.1.py <path_to_image_Ascii> [width] [invert(y/n or yes/no)] <path_out_image>",
        ">>ตัวอย่าง: python <file_path>/TKNL_ASCII_ART0.0.1.py Albert_Einstein.jpg 35 n Donwloads/ascii_text.txt",
        ">>ต่าเริ่มต้น [width] เป้น 100 px ทุกตัวอักขระ(Ascii)เท่ากับ 1 px จากนั้นจะนำาไปทำาอัตราส่วน",
        ">>ถ้าใส่ Input ไม่ถูกต้อง จะแสดงหน้านี้",
        ">>ทุก <path_out_image> จะตามด้วย .txt เสมอ ถ้าไม่ใส่ต่ำาแหน่ง/ตำ่าแหน่งไม่ถูกต้อง โปรแกรมจะบันทึกที่ต่ำาแหน่ง Downloads/ascii_text.txt เสมอ",
    )
    print("=" * len(HOW_text[0]))
    # print(len(HOW_text[0]))
    print(
        f"\n{' ' * int(0.5 * (len(HOW_text[0]) + 2 - len(Head_text[0])))}{Head_text[0]}"
    )  # ช่อโปรเจค
    print(f"""
    {"╺┳╸╻┏ ┏┓╻╻     ┏━┓┏━┓┏━╸╻╻   ┏━┓┏━┓╺┳╸       ".center(len(HOW_text[0]))}
    {"┃ ┣┻┓┃┗┫┃     ┣━┫┗━┓┃  ┃┃   ┣━┫┣┳┛ ┃       ".center(len(HOW_text[0]))}
    {"╹ ╹ ╹╹ ╹┗━╸╺━╸╹ ╹┗━┛┗━╸╹╹╺━╸╹ ╹╹┗╸ ╹ v.0.0.1".center(len(HOW_text[0]))}
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
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⢿⡿⣻⢻⡁⠀⢀⣄⣤⢴⠴⡴⣻⡻⣻⡻⣻⢭⢯⡻⣄⠦⠒⠉⠉⠉⡹⠀⢀⠈⠀⠄⠈⣿⢟⣿⡻⡿⣿
⣿⣯⢿⡽⣯⢿⡽⣯⣷⡻⣮⢟⣞⢗⡵⡀⣜⢍⡢⡲⣡⢫⠺⣬⡻⣼⣝⢷⣫⣞⢽⣪⡻⡕⢶⡄⠀⡽⠀⠀⡀⠐⠀⠀⣿⣝⣮⡻⣺⣻
⣿⡯⣿⡽⣯⣟⣿⣳⣽⣯⣻⡽⣝⣗⢕⠮⡪⣞⢽⣝⢷⣝⣽⢮⣻⢞⣮⣟⢮⡯⣳⠵⣝⢝⡵⣕⠀⢾⠀⠀⡀⠀⠐⠀⣿⢮⣞⣝⢷⣻
⣿⣟⡷⣿⢯⣿⣞⡿⣾⢞⣷⢽⡷⣝⣎⡳⣹⢮⣳⣝⢷⣫⣾⣫⣯⡻⣮⢷⡻⣞⣵⢳⡱⣑⠎⢮⠀⣳⠀⢀⠀⠈⠀⠀⣿⣳⢽⡮⣿⣽
⣿⣯⢿⣯⢿⡾⣽⢿⣽⢯⣟⣷⣻⣞⣜⢾⡵⣻⡵⣏⢿⡵⣳⢗⡷⣻⡺⣳⣝⢷⣝⢯⡷⣵⣫⢮⠀⣽⠀⠠⠀⠁⠈⠀⣿⣳⣟⢾⡵⣿
⣿⣟⣯⣟⣿⣻⣟⣯⣿⡽⣗⣿⣺⢞⣮⢷⡻⣵⣫⢏⣷⣝⢷⡽⣝⣮⣻⢮⣞⡵⡝⢷⢝⡷⣻⣗⢀⡿⣀⡴⠤⠵⠢⠊⣿⡵⣯⣗⣟⣿
⣿⣿⣽⣯⣿⡽⠯⠛⠚⠙⠋⠓⠙⠛⠚⠛⠳⠷⠯⠿⢮⡿⣝⣯⡿⣵⣯⣻⢮⡿⣽⢷⢷⣳⣵⣽⣥⣯⣄⣠⣀⣀⣀⠐⣿⡻⡾⣮⢯⣿
⣿⣿⣾⡷⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⠀⠁⠉⠉⠉⠉⠉⠉⠋⠊⠑⠉⠈⠉⠉⠉⠁⠈⠀⠈⠉⠙⣷⣟⣿
⣿⣿⣿⣆⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣤⣶⢾⣟⢾⣿
⣿⣿⣷⣿⣿⣶⣶⣦⣤⣤⣄⣄⣀⡀⠀⡢⠈⠐⡀⠑⠄⠱⡐⠅⡆⢔⠰⡀⠂⠀⡀⠀⡀⠈⡢⡃⠀⢰⡖⠐⠄⠂⠄⢐⣿⣯⢿⡽⣯⣿
⣿⣿⣾⣯⣿⢿⣿⣿⣿⣿⣿⣿⣿⣇⠠⢪⠂⡠⠴⠤⠀⠀⡀⠀⣹⢮⢀⠄⠠⢀⠐⠰⢄⡈⣵⡫⢀⣼⡏⡜⣈⢊⠐⢠⣿⣽⢿⡽⣯⣿
⣿⣿⣾⢷⣿⢿⣯⣿⣽⣯⣿⣽⣟⣿⡄⢱⢝⣤⡰⠢⢜⠣⡔⢆⢜⣷⡑⡮⣜⣱⡪⣷⢴⣝⣮⡃⢠⣿⣧⣮⣴⣤⢧⠴⣿⣯⣿⠙⣯⣿
⣿⣿⣽⣟⣿⣻⣟⣷⣿⣻⣾⣯⣿⣻⣦⠘⡵⡳⣻⣟⣯⢷⣝⢧⡹⣯⡎⢿⢮⣽⣽⣯⢿⢾⣵⡅⠊⣿⡄⠀⠄⠄⠄⠰⣿⡾⣿⡁⣿⣿
⣿⣿⣽⣯⣿⣻⣯⣿⣽⣟⣷⡿⣾⢿⣽⡧⢙⢎⢷⣽⢾⣟⢮⣗⢽⡾⣟⣽⣫⡿⣾⡷⣻⡳⣇⠀⠀⣿⡆⠀⠌⡐⠀⠨⣿⣻⣿⠄⣿⣿
⣿⣿⢷⣿⣽⣿⣽⣯⣿⣽⣟⣿⣻⣟⣷⡟⣰⠡⡳⣝⢯⣪⡎⠛⠚⢟⠿⠊⣵⡝⣯⢟⣝⢞⡇⠀⠀⣿⡆⠈⠀⠀⠈⠐⣿⣯⣿⣻⣟⣿
⣿⣿⢿⡷⣿⣾⣯⣿⢷⣿⣯⡿⣿⣽⣯⡗⢸⡫⣞⢜⡶⣻⢽⡳⣆⢀⢰⢞⡽⣻⣜⢯⣞⢯⠃⠀⠠⣿⡅⠀⢀⠈⠀⢈⣿⣷⣻⡷⣻⣿
⣿⣿⣿⣻⣿⡾⣷⡿⣿⢷⣿⣻⡿⣾⣯⡯⠤⢏⡞⣯⢢⣤⣑⣑⣉⡙⢑⣯⣪⣤⣹⡳⣝⡇⢄⠁⠠⣿⡅⠐⠀⠄⠀⠠⣿⣯⣷⣟⡿⣿
⣿⣿⣽⣟⣷⣿⣿⣻⣿⣻⣯⣿⣻⡿⣾⣗⢰⡔⠑⢭⣟⣽⣭⣍⠋⠛⡉⢙⣿⣿⣪⠗⣜⣿⠀⡓⣠⣿⣃⣠⣠⣠⣠⣠⣿⡾⣷⣽⣻⣿
⣿⣿⣽⣯⣿⣾⣯⣿⣽⣿⣽⣯⡿⣿⣽⡧⠊⠀⠀⣮⢘⢗⠿⡾⡿⡿⡿⢷⠪⢿⣷⣝⢾⣿⠁⡢⢀⠛⠿⢟⣿⢯⣟⢷⣯⢿⣞⡷⣻⣾
⣿⣿⢿⣾⣷⢿⣾⣟⣷⣿⢾⠯⡟⢛⡔⡑⠀⢠⢒⣿⣧⡳⢱⡈⠊⢈⢈⠢⠲⣢⣯⣻⣿⡯⢐⠄⡑⠌⡢⠠⡀⢉⠙⠹⠾⢯⣯⣟⣽⣿
⣿⣿⣿⠷⠿⠛⡉⡉⠔⡀⠢⠢⡁⠧⠈⠔⢀⢯⣟⣽⡿⣿⣦⡌⡈⢂⢅⣱⣵⣿⣿⣽⡷⢁⠔⡡⢈⠢⡘⠢⠐⡈⠌⢂⠐⡀⢄⠈⡌⢙
⡟⢉⠔⡠⠃⡐⡈⠠⢂⠌⠢⡁⡊⠄⠃⠄⣨⣿⣻⣞⡿⣿⣻⡿⢓⢴⣿⣿⣻⡿⣾⣯⠁⢢⢑⠠⠊⠔⡈⢈⠢⠀⡑⠀⡅⠐⠠⠑⠠⢃
⡕⢡⢊⠐⠄⠢⡠⡁⠢⡐⠡⠄⣈⠐⡁⠠⣾⣯⣿⣽⣿⣽⡟⢨⡇⡣⢹⣿⣽⣿⣻⡇⠈⡢⢀⠡⠊⠐⠌⡀⠢⡁⡈⠠⠀⠌⡀⠡⠁⡌
        """)

    # เรียกใช้งาน


if __name__ == "__main__":
    try:
        if len(sys.argv) < 2:
            # print(len(sys.argv))
            Show_title()
            sys.exit(1)
        # จัด Sys.argv
        image_path_in = sys.argv[1]
        width = (
            int(sys.argv[2])
            if len(sys.argv[2]) < 3 or 0 < int(sys.argv[2]) <= 10000
            else 100
        )
        invert_YN = (
            sys.argv[3][0]
            if (
                (sys.argv[3][0].lower() == "y" or sys.argv[3][0].lower() == "n")
                and (sys.argv[3][-1].lower() == "y" and sys.argv[3][-1].lower() != "n")
            )
            or (sys.argv[3].lower() == "yes" or sys.argv[3].lower() == "no")
            else "n"
        )
        image_path_out = (
            sys.argv[4]
            if sys.argv[4].split(".")[-1] == "txt"
            and sys.argv[4].split("/")[0].isalnum()
            else f"{sys.argv[1].split('/')[0]}/ascii_image.txt"
        )

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
    # except IndexError as Error:
    # print(f"{Error}เกิดข้อผิดพลาดเนื้องจาก Input ไม่ตรงกับการทำางานกำาหนด")
    # Show_title()
    except Exception as E:
        # print(f"Error: {type(E).__name__}, Message: {str(E)}")
        # print("\n" + f"YOU HAVE PUT THE COMMAND INCORRECTLY.".center(129, "!") + "\n")
        # print("\n" + f"Please Try Again.".center(129, "!") + "\n")
        # print(f"{E}".center(129))
        # Show_title()
        print(e)
    """
    except ValueError as E:
        print("\n" + f"YOU HAVE PUT THE COMMAND INCORRECTLY.".center(129, "!") + "\n")
        print("\n" + f"Please Try Again.".center(129, "!") + "\n")
        print(f"{E}".center(129))
        Show_title()
        """
