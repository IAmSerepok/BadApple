from PIL import Image, ImageDraw, ImageFont
import random
import os
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor, as_completed


def _load_font(font_path, size):
    try:
        return ImageFont.truetype(font_path, size=size)
    except OSError:
        try:
            from matplotlib import font_manager
            p = font_manager.findfont("DejaVu Sans")
            print(f"[warn] '{font_path}' не найден, использую {p}")
            return ImageFont.truetype(p, size=size)
        except Exception:
            print("[warn] fallback на load_default")
            return ImageFont.load_default()


def _prepare_mask(mask_path, total_cols, total_rows, threshold, invert):
    mask = Image.open(mask_path).convert("L")
    mask = mask.resize((total_cols, total_rows), resample=Image.BOX)
    if invert:
        mask = Image.eval(mask, lambda p: 255 - p)
    mask_bin = mask.point(lambda p: 255 if p < threshold else 0)
    return mask_bin.load()


def render_one(
    background_img, 
    mask_mp, 
    cols, rows,
    x0, y0, w, h, dx, dy,
    step_x, step_y,
    n_blocks_x, n_blocks_y,
    font, alphabet, jitter, text_color,
    output_path,
):
    img = background_img.copy()
    draw = ImageDraw.Draw(img)

    def is_black(bi, bj, ci, cj):
        return mask_mp[bi * cols + ci, bj * rows + cj] != 0

    total = 0
    for bj in range(n_blocks_y):
        for bi in range(n_blocks_x):
            for cj in range(rows):
                for ci in range(cols):
                    if not is_black(bi, bj, ci, cj):
                        continue
                    total += 1
                    cell_x = x0 + bi * step_x + ci * (w + dx)
                    cell_y = y0 + bj * step_y + cj * (h + dy)

                    char = random.choice(alphabet)
                    bbox = draw.textbbox((0, 0), char, font=font)
                    tw = bbox[2] - bbox[0]
                    th = bbox[3] - bbox[1]
                    pos_x = cell_x + (w - tw) / 2 - bbox[0] + random.randint(-jitter, jitter)
                    pos_y = cell_y + (h - th) / 2 - bbox[1] + random.randint(-jitter, jitter)

                    draw.text((pos_x, pos_y), char, font=font, fill=text_color)

    img.convert("RGB").save(output_path, quality=95)
    return output_path, total


def process_folder(
    frames_dir,
    output_dir,
    background_path,
    font_path,
    x0, y0,
    w, h, dx, dy,
    cols, rows,
    block_dx, block_dy,
    n_blocks_x=1, n_blocks_y=1,
    threshold=128,
    invert=False,
    alphabet="АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ",
    font_size=None,
    jitter=1,
    text_color=(0, 0, 0, 255),
    max_workers=None,
    extensions=(".jpg", ".jpeg", ".png", ".bmp"),
):
    frames_dir = Path(frames_dir)
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    step_x = cols * w + (cols - 1) * dx + block_dx
    step_y = rows * h + (rows - 1) * dy + block_dy

    total_cols = n_blocks_x * cols
    total_rows = n_blocks_y * rows

    bg = Image.open(background_path).convert("RGBA")
    if font_size is None:
        font_size = int(h * 0.85)
    font = _load_font(font_path, font_size)

    files = sorted(
        p for p in frames_dir.iterdir()
        if p.suffix.lower() in extensions
    )
    if not files:
        print(f"[warn] в {frames_dir} нет картинок")
        return []

    print(f"Найдено {len(files)} кадров, запускаю параллельно…")

    def worker(path: Path):
        mp = _prepare_mask(path, total_cols, total_rows, threshold, invert)
        out_name = f"output_{path.stem}.jpg"
        out_path = output_dir / out_name
        return render_one(
            background_img=bg,
            mask_mp=mp,
            cols=cols, rows=rows,
            x0=x0, y0=y0, w=w, h=h, dx=dx, dy=dy,
            step_x=step_x, step_y=step_y,
            n_blocks_x=n_blocks_x, n_blocks_y=n_blocks_y,
            font=font, alphabet=alphabet,
            jitter=jitter, text_color=text_color,
            output_path=str(out_path),
        )

    results = []

    with ThreadPoolExecutor(max_workers=max_workers) as ex:
        futures = {ex.submit(worker, p): p for p in files}
        for i, fut in enumerate(as_completed(futures), 1):
            path = futures[fut]
            try:
                out_path, cnt = fut.result()
                results.append((out_path, cnt))
                print(f"[{i}/{len(files)}] {path.name} → {Path(out_path).name}  (клеток: {cnt})")
            except Exception as e:
                print(f"[{i}/{len(files)}] {path.name} → ОШИБКА: {e}")

    return results


if __name__ == "__main__":
    random.seed(42)

    process_folder(
        frames_dir="frames",
        output_dir="output",
        background_path="blank_1.jpg",
        font_path="Caveat-VariableFont_wght.ttf",
        x0=88, y0=449,
        w=23, h=36,
        dx=8.2, dy=10,
        cols=17, rows=5,
        block_dx=58, block_dy=26,
        n_blocks_x=2, n_blocks_y=4,
        threshold=128,
        invert=False,
        jitter=0,
        font_size=28,
        max_workers=None
    )