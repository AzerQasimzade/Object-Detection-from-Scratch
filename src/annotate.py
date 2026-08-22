
from pathlib import Path
import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk

BASE_DIR = Path(__file__).resolve().parent.parent
FRAMES_DIR = BASE_DIR / "data" / "frames"
LABELS_DIR = BASE_DIR / "data" / "labels"

LABELS_DIR.mkdir(parents=True, exist_ok=True)

images = sorted(
    list(FRAMES_DIR.glob("*.jpg")) +
    list(FRAMES_DIR.glob("*.jpeg")) +
    list(FRAMES_DIR.glob("*.png"))
)

if not images:
    raise RuntimeError("No images found in data/frames")

current_index = 0
boxes = []
start_x = None
start_y = None
temp_rectangle = None

root = tk.Tk()
root.title("Car Annotation Tool")
root.geometry("1300x850")

top_frame = tk.Frame(root)
top_frame.pack(fill="x", padx=10, pady=5)

info_label = tk.Label(top_frame, text="", font=("Arial", 12))
info_label.pack(side="left")

canvas = tk.Canvas(root, bg="black")
canvas.pack(fill="both", expand=True, padx=10, pady=5)

button_frame = tk.Frame(root)
button_frame.pack(pady=8)


def load_image():
    global boxes, start_x, start_y, temp_rectangle

    boxes = []
    start_x = None
    start_y = None
    temp_rectangle = None

    image_path = images[current_index]
    image = Image.open(image_path)

    # Keep the image inside the available canvas area
    max_width = 1200
    max_height = 700

    scale = min(
        max_width / image.width,
        max_height / image.height,
        1
    )

    display_width = int(image.width * scale)
    display_height = int(image.height * scale)

    image = image.resize((display_width, display_height))

    photo = ImageTk.PhotoImage(image)

    canvas.delete("all")
    canvas.config(
        width=display_width,
        height=display_height,
        scrollregion=(0, 0, display_width, display_height)
    )

    canvas.image = photo
    canvas.create_image(0, 0, anchor="nw", image=photo)

    root.image_scale = scale
    root.original_width = Image.open(image_path).width
    root.original_height = Image.open(image_path).height

    info_label.config(
        text=f"{current_index + 1}/{len(images)}  |  {image_path.name}  |  Boxes: 0"
    )


def mouse_down(event):
    global start_x, start_y, temp_rectangle

    start_x = event.x
    start_y = event.y

    temp_rectangle = canvas.create_rectangle(
        start_x,
        start_y,
        start_x,
        start_y,
        outline="red",
        width=2
    )


def mouse_drag(event):
    if temp_rectangle is not None:
        canvas.coords(
            temp_rectangle,
            start_x,
            start_y,
            event.x,
            event.y
        )


def mouse_up(event):
    global start_x, start_y, temp_rectangle

    if start_x is None or start_y is None:
        return

    x1 = min(start_x, event.x)
    y1 = min(start_y, event.y)
    x2 = max(start_x, event.x)
    y2 = max(start_y, event.y)

    width = x2 - x1
    height = y2 - y1

    if width < 5 or height < 5:
        canvas.delete(temp_rectangle)
        temp_rectangle = None
        start_x = None
        start_y = None
        return

    boxes.append((x1, y1, x2, y2))

    canvas.itemconfig(temp_rectangle, outline="lime")

    temp_rectangle = None
    start_x = None
    start_y = None

    update_info()


def update_info():
    info_label.config(
        text=f"{current_index + 1}/{len(images)}  |  "
             f"{images[current_index].name}  |  "
             f"Boxes: {len(boxes)}"
    )


def undo_box():
    if boxes:
        boxes.pop()
        canvas.delete("all")
        redraw()
        update_info()


def redraw():
    image_path = images[current_index]
    image = Image.open(image_path)

    scale = root.image_scale

    display_width = int(image.width * scale)
    display_height = int(image.height * scale)

    image = image.resize((display_width, display_height))
    photo = ImageTk.PhotoImage(image)

    canvas.delete("all")
    canvas.image = photo
    canvas.create_image(0, 0, anchor="nw", image=photo)

    for box in boxes:
        canvas.create_rectangle(
            *box,
            outline="lime",
            width=2
        )


def save_labels():
    if not boxes:
        messagebox.showwarning(
            "No boxes",
            "Draw at least one bounding box around a car."
        )
        return

    image_path = images[current_index]
    label_path = LABELS_DIR / f"{image_path.stem}.txt"

    scale = root.image_scale

    lines = []

    for x1, y1, x2, y2 in boxes:

        # Convert display coordinates to original image coordinates
        x1_original = x1 / scale
        y1_original = y1 / scale
        x2_original = x2 / scale
        y2_original = y2 / scale

        # YOLO normalized coordinates
        x_center = ((x1_original + x2_original) / 2) / root.original_width
        y_center = ((y1_original + y2_original) / 2) / root.original_height

        width = (x2_original - x1_original) / root.original_width
        height = (y2_original - y1_original) / root.original_height

        lines.append(
            f"0 {x_center:.6f} {y_center:.6f} "
            f"{width:.6f} {height:.6f}"
        )

    label_path.write_text(
        "\n".join(lines),
        encoding="utf-8"
    )

    info_label.config(
        text=f"{current_index + 1}/{len(images)}  |  "
             f"{image_path.name}  |  "
             f"Saved: {label_path.name}  |  "
             f"Boxes: {len(boxes)}"
    )


def next_image():
    global current_index

    save_labels()

    if current_index < len(images) - 1:
        current_index += 1
        load_image()


def previous_image():
    global current_index

    if current_index > 0:
        current_index -= 1
        load_image()


def skip_image():
    global current_index

    if current_index < len(images) - 1:
        current_index += 1
        load_image()


canvas.bind("<ButtonPress-1>", mouse_down)
canvas.bind("<B1-Motion>", mouse_drag)
canvas.bind("<ButtonRelease-1>", mouse_up)

tk.Button(
    button_frame,
    text="Previous",
    command=previous_image,
    width=12
).pack(side="left", padx=5)

tk.Button(
    button_frame,
    text="Undo",
    command=undo_box,
    width=12
).pack(side="left", padx=5)

tk.Button(
    button_frame,
    text="SAVE",
    command=save_labels,
    width=12
).pack(side="left", padx=5)

tk.Button(
    button_frame,
    text="Skip",
    command=skip_image,
    width=12
).pack(side="left", padx=5)

tk.Button(
    button_frame,
    text="Next",
    command=next_image,
    width=12
).pack(side="left", padx=5)

load_image()

root.mainloop()
