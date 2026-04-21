from __future__ import annotations

from pathlib import Path

from PIL import Image, ImageOps

FRAME_SIZE = 16
SCALE = 8
SCALED_SIZE = (FRAME_SIZE * SCALE, FRAME_SIZE * SCALE)

ANIMATION_MAP: dict[str, tuple[int, int]] = {
    "rest_stand": (0, 8),
    "rest_sit": (1, 8),
    "rest_lie": (2, 5),
    "rest_special": (3, 10),
    "walk_down": (4, 4),
    "walk_up": (5, 4),
    "walk_right": (6, 6),
    "walk_left": (7, 6),
    "walk_left_d": (8, 5),
    "walk_right_d": (9, 5),
    "walk_right_up": (10, 5),
    "walk_left_up": (11, 5),
    "sleep_1_l": (12, 2),
    "sleep_1_r": (13, 2),
    "sleep_2_l": (14, 2),
    "sleep_2_r": (15, 2),
    "sleep_3_l": (16, 2),
    "sleep_3_r": (17, 2),
    "sleep_4_l": (18, 2),
    "sleep_4_r": (19, 2),
    "eat_down": (20, 7),
    "eat_up": (21, 7),
    "eat_left": (22, 6),
    "eat_right": (23, 6),
    "eat_right_d": (24, 6),
    "eat_left_d": (25, 6),
    "eat_right_up": (26, 6),
    "eat_left_up": (27, 6),
    "meow_sit": (28, 3),
    "meow_stand": (29, 2),
    "meow_sit2": (30, 2),
    "meow_lie": (31, 3),
    "yawn_sit": (32, 6),
    "yawn_stand": (33, 6),
    "yawn_sit2": (34, 6),
    "yawn_lie": (35, 5),
    "wash_sit": (36, 6),
    "wash_stand": (37, 5),
    "wash_lie": (38, 5),
    "scratch_l": (39, 8),
    "scratch_r": (40, 8),
    "hiss_l": (41, 2),
    "hiss_r": (42, 2),
    "dead": (43, 1),
    "paw_att_down": (44, 7),
    "paw_att_up": (45, 7),
    "paw_att_left": (46, 5),
    "paw_att_right": (47, 5),
    "paw_att_right_d": (48, 6),
    "paw_att_left_d": (49, 6),
    "paw_att_right_up": (50, 5),
    "paw_att_left_up": (51, 5),
    "hind_legs": (52, 2),
}

_FRAMES_BY_ANIMATION: dict[str, list[Image.Image]] = {}


def _fit_to_canvas(frame: Image.Image) -> Image.Image:
    bbox = frame.getbbox()
    if bbox:
        content = frame.crop(bbox)
    else:
        content = frame.copy()

    if content.width <= 0 or content.height <= 0:
        return Image.new("RGBA", SCALED_SIZE, (0, 0, 0, 0))

    scale = min(SCALED_SIZE[0] / content.width, SCALED_SIZE[1] / content.height)
    scaled_width = max(1, int(round(content.width * scale)))
    scaled_height = max(1, int(round(content.height * scale)))
    scaled_content = content.resize((scaled_width, scaled_height), Image.NEAREST)

    canvas = Image.new("RGBA", SCALED_SIZE, (0, 0, 0, 0))
    paste_x = (SCALED_SIZE[0] - scaled_content.width) // 2
    paste_y = SCALED_SIZE[1] - scaled_content.height
    canvas.paste(scaled_content, (paste_x, paste_y))
    return canvas


def _normalize_frame(frame: Image.Image) -> Image.Image:
    return frame.resize(SCALED_SIZE, Image.NEAREST)


def _normalize_and_align(frame: Image.Image) -> Image.Image:
    scaled = frame.resize(SCALED_SIZE, Image.NEAREST)
    bbox = scaled.getbbox()
    if not bbox:
        return scaled
    content = scaled.crop(bbox)
    canvas = Image.new("RGBA", SCALED_SIZE, (0, 0, 0, 0))
    paste_x = (SCALED_SIZE[0] - content.width) // 2
    paste_y = SCALED_SIZE[1] - content.height
    canvas.paste(content, (paste_x, paste_y))
    return canvas


def _load_strip(path: Path) -> list[Image.Image]:
    strip = Image.open(path).convert("RGBA")
    frame_size = strip.height
    if frame_size <= 0:
        return []

    frame_count = strip.width // frame_size
    frames: list[Image.Image] = []
    for col in range(frame_count):
        frame = strip.crop((col * frame_size, 0, (col + 1) * frame_size, frame_size))
        frames.append(_normalize_and_align(frame))
    return frames


def _repeat_frames(frames: list[Image.Image], count: int) -> list[Image.Image]:
    if not frames:
        empty = Image.new("RGBA", SCALED_SIZE, (0, 0, 0, 0))
        return [empty.copy() for _ in range(max(1, count))]
    return [frames[i % len(frames)].copy() for i in range(count)]


def _load_2d_pack(folder: Path) -> dict[str, list[Image.Image]]:
    idle = _load_strip(folder / "idle.png")
    walk = _load_strip(folder / "walk.png")
    run = _load_strip(folder / "run.png")
    jump = _load_strip(folder / "jump.png")
    attack = _load_strip(folder / "attack.png")

    base_idle = idle or walk or run or jump or attack
    base_walk = walk or run or idle or jump or attack
    base_run = run or walk or idle or jump or attack
    base_jump = jump or walk or idle or run or attack
    base_attack = attack or run or walk or jump or idle

    frames_by_animation: dict[str, list[Image.Image]] = {}
    for animation_name, (_, num_frames) in ANIMATION_MAP.items():
        if animation_name.startswith("walk"):
            source = base_walk
        elif animation_name.startswith("paw_att"):
            source = base_attack
        elif animation_name.startswith("eat"):
            source = base_run
        elif animation_name.startswith("yawn") or animation_name.startswith("meow"):
            source = base_jump
        else:
            source = base_idle

        if "left" in animation_name or animation_name.endswith("_l"):
            source = [ImageOps.mirror(frame) for frame in source]

        frames_by_animation[animation_name] = _repeat_frames(source, num_frames)

    return frames_by_animation


def _load_single_model(image: Image.Image) -> dict[str, list[Image.Image]]:
    base_frame = _fit_to_canvas(image)
    mirrored_frame = ImageOps.mirror(base_frame)
    frames_by_animation: dict[str, list[Image.Image]] = {}

    for animation_name, (_, num_frames) in ANIMATION_MAP.items():
        template = mirrored_frame if "left" in animation_name or animation_name.endswith("_l") else base_frame
        frames_by_animation[animation_name] = [template.copy() for _ in range(max(1, num_frames))]

    return frames_by_animation


def load_sprite_sheet(path: str) -> dict[str, list[Image.Image]]:
    global _FRAMES_BY_ANIMATION

    input_path = Path(path)
    if input_path.is_dir():
        pack_frames = _load_2d_pack(input_path)
        _FRAMES_BY_ANIMATION = pack_frames
        return pack_frames

    image = Image.open(path).convert("RGBA")
    max_row = max(row for row, _ in ANIMATION_MAP.values())
    max_frames_in_row = max(num_frames for _, num_frames in ANIMATION_MAP.values())
    required_width = max_frames_in_row * FRAME_SIZE
    required_height = (max_row + 1) * FRAME_SIZE

    # Newer templates may provide a single rendered cat image instead of a classic 16x16 spritesheet.
    if image.width < required_width or image.height < required_height:
        frames_by_animation = _load_single_model(image)
        _FRAMES_BY_ANIMATION = frames_by_animation
        return frames_by_animation

    frames_by_animation: dict[str, list[Image.Image]] = {}

    for animation_name, (row, num_frames) in ANIMATION_MAP.items():
        raw_frames: list[Image.Image] = []
        bboxes: list[tuple[int, int, int, int] | None] = []

        for col in range(num_frames):
            raw_frame = image.crop(
                (
                    col * FRAME_SIZE,
                    row * FRAME_SIZE,
                    col * FRAME_SIZE + FRAME_SIZE,
                    row * FRAME_SIZE + FRAME_SIZE,
                )
            )
            raw_frames.append(raw_frame)
            bboxes.append(raw_frame.getbbox())

        valid_bboxes = [bbox for bbox in bboxes if bbox is not None]
        if valid_bboxes:
            max_content_width = max(bbox[2] - bbox[0] for bbox in valid_bboxes)
            max_content_height = max(bbox[3] - bbox[1] for bbox in valid_bboxes)
        else:
            max_content_width = FRAME_SIZE
            max_content_height = FRAME_SIZE

        frames: list[Image.Image] = []
        for raw_frame, bbox in zip(raw_frames, bboxes):
            normalized_content = Image.new(
                "RGBA", (max_content_width, max_content_height), (0, 0, 0, 0)
            )
            if bbox:
                content = raw_frame.crop(bbox)
                content_x = (max_content_width - content.width) // 2
                content_y = max_content_height - content.height
                normalized_content.paste(content, (content_x, content_y))

            scaled_content = normalized_content.resize(
                (max_content_width * SCALE, max_content_height * SCALE),
                Image.NEAREST,
            )

            canvas = Image.new("RGBA", SCALED_SIZE, (0, 0, 0, 0))
            paste_x = (SCALED_SIZE[0] - scaled_content.width) // 2
            paste_y = SCALED_SIZE[1] - scaled_content.height
            canvas.paste(scaled_content, (paste_x, paste_y))
            frames.append(canvas)

        frames_by_animation[animation_name] = frames

    _FRAMES_BY_ANIMATION = frames_by_animation
    return frames_by_animation


def get_frames(anim_name: str) -> list[Image.Image]:
    if anim_name not in _FRAMES_BY_ANIMATION:
        raise KeyError(anim_name)
    return _FRAMES_BY_ANIMATION[anim_name]


if __name__ == "__main__":
    default_sheet = Path(__file__).resolve().parents[1] / "cat animation" / "cat.png"
    all_frames = load_sprite_sheet(str(default_sheet))

    for name, frames in all_frames.items():
        print(f"{name}: {len(frames)} frames")
