from io import BytesIO
from PIL import Image, ImageDraw, ImageFont, ImageOps
from telegram import Update, ReplyKeyboardMarkup, ReplyKeyboardRemove
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    ConversationHandler,
    filters,
)

import os
TOKEN = os.getenv("BOT_TOKEN")

ASK_ACTION, ASK_TEMPLATE, ASK_NAME, ASK_PHOTO = range(4)

FONT_PATH = "font.ttf"

MAIN_KEYBOARD = ReplyKeyboardMarkup(
    [
        ["Создать карточку"],
        ["Начать с начала"],
    ],
    resize_keyboard=True
)

TEMPLATES = {
    "Lifestyle Ambassador": {
        "file": "templates/lifestyle.jpg",
        "name_box": {"x": 90, "y": 900, "w": 980, "h": 360},
        "photo_circle": {"cx": 1523, "cy": 1116, "diameter": 790},
        "text_color": (0, 0, 0),
        "max_font_size": 150,
        "min_font_size": 40,
    },
    "Silver Ambassador": {
        "file": "templates/silver.jpg",
        "name_box": {"x": 220, "y": 1260, "w": 1600, "h": 160},
        "photo_circle": {"cx": 995, "cy": 506, "diameter": 737},
        "text_color": (255, 255, 255),
        "max_font_size": 120,
        "min_font_size": 40,
    },
    "Gold Ambassador": {
        "file": "templates/gold.jpg",
        "name_box": {"x": 220, "y": 1260, "w": 1600, "h": 160},
        "photo_circle": {"cx": 995, "cy": 506, "diameter": 737},
        "text_color": (255, 255, 255),
        "max_font_size": 120,
        "min_font_size": 40,
    },
    "Platinum Ambassador": {
        "file": "templates/platinum.jpg",
        "name_box": {"x": 220, "y": 1260, "w": 1600, "h": 160},
        "photo_circle": {"cx": 995, "cy": 506, "diameter": 737},
        "text_color": (255, 255, 255),
        "max_font_size": 120,
        "min_font_size": 40,
    },
    "Titanium Ambassador": {
        "file": "templates/titanium.jpg",
        "name_box": {"x": 220, "y": 1260, "w": 1600, "h": 160},
        "photo_circle": {"cx": 995, "cy": 506, "diameter": 737},
        "text_color": (255, 255, 255),
        "max_font_size": 120,
        "min_font_size": 40,
    },
    "Jade Ambassador": {
        "file": "templates/jade.jpg",
        "name_box": {"x": 220, "y": 1260, "w": 1600, "h": 160},
        "photo_circle": {"cx": 995, "cy": 506, "diameter": 737},
        "text_color": (255, 255, 255),
        "max_font_size": 120,
        "min_font_size": 40,
    },
    "Pearl Ambassador": {
        "file": "templates/pearl.jpg",
        "name_box": {"x": 220, "y": 1260, "w": 1600, "h": 160},
        "photo_circle": {"cx": 995, "cy": 506, "diameter": 737},
        "text_color": (255, 255, 255),
        "max_font_size": 120,
        "min_font_size": 40,
    },
    "Emerald Ambassador": {
        "file": "templates/emerald.jpg",
        "name_box": {"x": 220, "y": 1260, "w": 1600, "h": 160},
        "photo_circle": {"cx": 995, "cy": 506, "diameter": 737},
        "text_color": (255, 255, 255),
        "max_font_size": 120,
        "min_font_size": 40,
    },
    "Ruby Ambassador": {
        "file": "templates/ruby.jpg",
        "name_box": {"x": 220, "y": 1260, "w": 1600, "h": 160},
        "photo_circle": {"cx": 995, "cy": 506, "diameter": 737},
        "text_color": (255, 255, 255),
        "max_font_size": 120,
        "min_font_size": 40,
    },
    "Sapphire Ambassador": {
        "file": "templates/sapphire.jpg",
        "name_box": {"x": 220, "y": 1260, "w": 1600, "h": 160},
        "photo_circle": {"cx": 995, "cy": 506, "diameter": 737},
        "text_color": (255, 255, 255),
        "max_font_size": 120,
        "min_font_size": 40,
    },
    "Diamond Ambassador": {
        "file": "templates/diamond.jpg",
        "name_box": {"x": 220, "y": 1260, "w": 1600, "h": 160},
        "photo_circle": {"cx": 995, "cy": 506, "diameter": 737},
        "text_color": (255, 255, 255),
        "max_font_size": 120,
        "min_font_size": 40,
    },
    "Double Diamond Ambassador": {
        "file": "templates/doublediamond.jpg",
        "name_box": {"x": 220, "y": 1260, "w": 1600, "h": 160},
        "photo_circle": {"cx": 995, "cy": 506, "diameter": 737},
        "text_color": (255, 255, 255),
        "max_font_size": 120,
        "min_font_size": 40,
    },
    "Triple Diamond Ambassador": {
        "file": "templates/triplediamond.jpg",
        "name_box": {"x": 220, "y": 1260, "w": 1600, "h": 160},
        "photo_circle": {"cx": 995, "cy": 506, "diameter": 737},
        "text_color": (255, 255, 255),
        "max_font_size": 120,
        "min_font_size": 40,
    },
    "Blue Diamond Ambassador": {
        "file": "templates/bluediamond.jpg",
        "name_box": {"x": 220, "y": 1260, "w": 1600, "h": 160},
        "photo_circle": {"cx": 995, "cy": 506, "diameter": 737},
        "text_color": (255, 255, 255),
        "max_font_size": 120,
        "min_font_size": 40,
    },
    "Black Diamond Ambassador": {
        "file": "templates/blackdiamond.jpg",
        "name_box": {"x": 220, "y": 1260, "w": 1600, "h": 160},
        "photo_circle": {"cx": 995, "cy": 506, "diameter": 737},
        "text_color": (255, 255, 255),
        "max_font_size": 120,
        "min_font_size": 40,
    },
}


def split_name(text):
    parts = text.strip().split()
    if len(parts) <= 1:
        return text
    return f"{parts[0]}\n{' '.join(parts[1:])}"

def split_lifestyle_name(text):
    parts = text.strip().split()

    if len(parts) <= 1:
        return text

    lower_parts = [p.lower() for p in parts]

    # Случай: "Имя и Имя Фамилия"
    if "и" in lower_parts:
        i_index = lower_parts.index("и")

        first_name = " ".join(parts[:i_index])
        second_name = " ".join(parts[i_index + 1:-1])
        surname = parts[-1]

        names_length = len(first_name.replace(" ", "")) + len(second_name.replace(" ", ""))

        if first_name and second_name and surname:
            if names_length <= 12:
                return f"{first_name} и {second_name}\n{surname}"
            else:
                return f"{first_name}\nи {second_name}\n{surname}"

    return split_name(text)


def fit_text(draw, text, font_path, box_w, box_h, max_size, min_size):
    for size in range(max_size, min_size - 1, -4):
        font = ImageFont.truetype(font_path, size)
        bbox = draw.multiline_textbbox((0, 0), text, font=font, spacing=10)
        text_w = bbox[2] - bbox[0]
        text_h = bbox[3] - bbox[1]

        if text_w <= box_w and text_h <= box_h:
            return font

    return ImageFont.truetype(font_path, min_size)


def make_circle(photo, diameter):
    photo = ImageOps.fit(
        photo,
        (diameter, diameter),
        method=Image.Resampling.LANCZOS,
        centering=(0.5, 0.5)
    )

    mask = Image.new("L", (diameter, diameter), 0)
    draw = ImageDraw.Draw(mask)
    draw.ellipse((0, 0, diameter, diameter), fill=255)

    result = Image.new("RGBA", (diameter, diameter), (0, 0, 0, 0))
    result.paste(photo.convert("RGBA"), (0, 0), mask)

    return result


def render_card(template_name, name, photo_bytes):
    settings = TEMPLATES[template_name]

    template = Image.open(settings["file"]).convert("RGBA")
    draw = ImageDraw.Draw(template)

    # Фото
    photo = Image.open(BytesIO(photo_bytes)).convert("RGB")
    circle = settings["photo_circle"]
    avatar = make_circle(photo, circle["diameter"])

    x_photo = circle["cx"] - circle["diameter"] // 2
    y_photo = circle["cy"] - circle["diameter"] // 2

    template.paste(avatar, (x_photo, y_photo), avatar)

    # Имя
    box = settings["name_box"]
    if template_name in ["Silver Ambassador", "Gold Ambassador", "Platinum Ambassador", "Titanium Ambassador", "Jade Ambassador", "Pearl Ambassador", "Emerald Ambassador", "Ruby Ambassador", "Sapphire Ambassador", "Diamond Ambassador", "Double Diamond Ambassador", "Triple Diamond Ambassador", "Blue Diamond Ambassador", "Black Diamond Ambassador"]:
        prepared_name = name.strip()
    else:
        if template_name == "Lifestyle Ambassador":
            prepared_name = split_lifestyle_name(name)
        elif template_name in ["Silver Ambassador", "Gold Ambassador", "Platinum Ambassador", "Titanium Ambassador", "Jade Ambassador", "Pearl Ambassador", "Emerald Ambassador", "Ruby Ambassador", "Sapphire Ambassador", "Diamond Ambassador", "Double Diamond Ambassador", "Triple Diamond Ambassador", "Blue Diamond Ambassador", "Black Diamond Ambassador"]:
            prepared_name = name.strip()
        else:
            prepared_name = split_name(name)

    font = fit_text(
        draw=draw,
        text=prepared_name,
        font_path=FONT_PATH,
        box_w=box["w"],
        box_h=box["h"],
        max_size=settings["max_font_size"],
        min_size=settings["min_font_size"],
    )

    bbox = draw.multiline_textbbox((0, 0), prepared_name, font=font, spacing=10)
    text_w = bbox[2] - bbox[0]
    text_h = bbox[3] - bbox[1]

    x_text = box["x"] + (box["w"] - text_w) // 2
    y_text = box["y"] + (box["h"] - text_h) // 2

    draw.multiline_text(
        (x_text, y_text),
        prepared_name,
        font=font,
        fill=settings["text_color"],
        spacing=10,
        align="center",
    )

    output = BytesIO()
    output.name = "result.jpg"

    # JPEG не поддерживает прозрачность, поэтому переводим в RGB
    final_image = template.convert("RGB")
    final_image.save(output, format="JPEG", quality=88, optimize=True, progressive=True)

    output.seek(0)

    return output


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):

    await update.message.reply_text(
        "Привет 👋\n\n"
        "Я помогу сделать карточку по шаблону.\n\n"
        "📸 Важно по фото:\n"
        "— лицо лучше поставить по центру\n"
        "— не слишком далеко\n"
        "— без сильных обрезаний головы и плеч\n\n"
        "Для начала, нажми кнопку ниже:",
        reply_markup=MAIN_KEYBOARD
    )

    return ASK_ACTION


async def create_card(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = ReplyKeyboardMarkup(
        [["Lifestyle Ambassador"], ["Silver Ambassador"], ["Gold Ambassador"], ["Platinum Ambassador"], ["Titanium Ambassador"], ["Jade Ambassador"], ["Pearl Ambassador"], ["Emerald Ambassador"], ["Ruby Ambassador"], ["Sapphire Ambassador"], ["Diamond Ambassador"], ["Double Diamond Ambassador"], ["Triple Diamond Ambassador"], ["Blue Diamond Ambassador"], ["Black Diamond Ambassador"]],
        resize_keyboard=True
    )

    await update.message.reply_text(
        "Выбери шаблон:",
        reply_markup=keyboard
    )

    return ASK_TEMPLATE


async def choose_template(update: Update, context: ContextTypes.DEFAULT_TYPE):
    template_name = update.message.text

    if template_name not in TEMPLATES:
        await update.message.reply_text("Пожалуйста, выбери шаблон кнопкой.")
        return ASK_TEMPLATE

    context.user_data["template_name"] = template_name

    await update.message.reply_text(
        "Напиши имя и фамилию",
        reply_markup=MAIN_KEYBOARD
    )

    return ASK_NAME


async def get_name(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["name"] = update.message.text.strip()

    await update.message.reply_text("Отправь фото")

    return ASK_PHOTO


async def get_photo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    name = context.user_data["name"]
    template_name = context.user_data["template_name"]

    await update.message.reply_text("⏳ Делаю карточку, подожди немного...")
    
    photo = update.message.photo[-1]
    file = await photo.get_file()
    photo_bytes = await file.download_as_bytearray()

    # Сжимаем фото перед обработкой
    img = Image.open(BytesIO(photo_bytes)).convert("RGB")
    img.thumbnail((1200, 1200))

buffer = BytesIO()
img.save(buffer, format="JPEG", quality=85)
photo_bytes = buffer.getvalue()

    result = render_card(template_name, name, photo_bytes)

    await update.message.reply_document(
        document=result,
        filename="result.jpg",
        read_timeout=120,
        write_timeout=120,
        connect_timeout=60,
    )

    await update.message.reply_text(
        "Готово. Можно создать ещё одну карточку.",
        reply_markup=MAIN_KEYBOARD
    )

    return ASK_ACTION


def main():
    app = (
        ApplicationBuilder()
        .token(TOKEN)
        .connect_timeout(60)
        .read_timeout(60)
        .write_timeout(60)
        .pool_timeout(60)
        .build()
    )

    conv = ConversationHandler(
        entry_points=[CommandHandler("start", start)],
        states={
            ASK_ACTION: [
                MessageHandler(filters.Regex("^Начать с начала$"), start),
                MessageHandler(filters.Regex("^Создать карточку$"), create_card),
            ],
            ASK_TEMPLATE: [
                MessageHandler(filters.Regex("^Начать с начала$"), start),
                MessageHandler(filters.TEXT & ~filters.COMMAND, choose_template),
            ],
            ASK_NAME: [
                MessageHandler(filters.Regex("^Начать с начала$"), start),
                MessageHandler(filters.TEXT & ~filters.COMMAND, get_name),
            ],
            ASK_PHOTO: [
                MessageHandler(filters.Regex("^Начать с начала$"), start),
                MessageHandler(filters.PHOTO, get_photo),
            ],
        },
        
        fallbacks=[
            CommandHandler("start", start),
            MessageHandler(filters.Regex("^Начать с начала$"), start),
        ],
    )

    app.add_handler(conv)
    app.run_polling()


if __name__ == "__main__":
    main()
