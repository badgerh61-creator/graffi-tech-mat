from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

OUT = Path(__file__).resolve().parents[1] / "static" / "decals"
OUT.mkdir(parents=True, exist_ok=True)

W = H = 1024

def save(img, name):
    p = OUT / name
    img.save(p, "PNG")
    print("wrote:", p)

def racing_stripe():
    img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)

    for i, col in enumerate([(220, 0, 0, 255), (20, 20, 20, 230), (235, 235, 235, 240)]):
        offset = i * 60
        pts = [
            (150 + offset, 150),
            (900, 350 + offset // 2),
            (850, 450 + offset // 2),
            (100 + offset, 250),
        ]
        d.polygon(pts, fill=col)

    return img

def flame():
    img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)

    center = (550, 450)
    for r, col in [
        (330, (255, 80, 0, 220)),
        (260, (255, 160, 0, 210)),
        (180, (255, 230, 60, 200)),
    ]:
        bbox = [center[0] - r, center[1] - r, center[0] + r, center[1] + r]
        d.ellipse(bbox, fill=col)

    d.polygon([(250, 540), (520, 610), (430, 820)], fill=(255, 90, 0, 190))
    d.polygon([(310, 565), (510, 620), (450, 760)], fill=(255, 190, 0, 180))
    return img

def number7():
    img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)

    d.polygon(
        [
            (180, 180),
            (860, 180),
            (860, 280),
            (520, 280),
            (860, 880),
            (720, 880),
            (420, 320),
            (180, 320),
        ],
        fill=(255, 255, 255, 255),
    )

    d.polygon(
        [
            (160, 200),
            (840, 200),
            (840, 260),
            (520, 260),
            (840, 860),
            (760, 860),
            (440, 300),
            (160, 300),
        ],
        fill=(20, 20, 20, 160),
    )

    d.line([(200, 200), (820, 200)], fill=(220, 0, 0, 220), width=18)
    return img

def logo_badge():
    img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)

    d.ellipse([80, 80, 944, 944], fill=(10, 10, 10, 220))
    d.ellipse([130, 130, 894, 894], outline=(220, 0, 0, 230), width=18)
    d.ellipse([165, 165, 859, 859], outline=(240, 240, 240, 200), width=8)

    try:
        font = ImageFont.truetype("DejaVuSans-Bold.ttf", 86)
        font2 = ImageFont.truetype("DejaVuSans-Bold.ttf", 58)
        d.text((210, 420), "GRAFFI", font=font, fill=(240, 240, 240, 245))
        d.text((260, 520), "TECH MAT", font=font2, fill=(220, 0, 0, 235))
    except Exception:
        d.rectangle([220, 440, 820, 520], fill=(240, 240, 240, 240))
        d.rectangle([260, 540, 780, 600], fill=(220, 0, 0, 230))

    return img

if __name__ == "__main__":
    save(racing_stripe(), "racing_stripe.png")
    save(flame(), "flame.png")
    save(number7(), "number_7.png")
    save(logo_badge(), "graffi_tech_mat_badge.png")
