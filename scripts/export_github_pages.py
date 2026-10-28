#!/usr/bin/env python3
"""Export the local owner catalog as a sanitized GitHub Pages data file."""
import json
import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SOURCE = ROOT / "backend" / "data" / "catalog.json"
UPLOADS = ROOT / "backend" / "uploads"
PUBLIC = ROOT / "frontend"

def main():
    data = json.loads(SOURCE.read_text(encoding="utf-8"))
    fields = ("id", "name", "material", "description", "category", "price", "available", "color", "swatch", "metal", "symbol", "photo")
    items = []
    for item in data.get("items", []):
        public_item = {key: item.get(key) for key in fields if key in item}
        photo = public_item.get("photo")
        if photo and photo.startswith("/uploads/"):
            filename = Path(photo).name
            source = UPLOADS / filename
            if source.is_file():
                (PUBLIC / "uploads").mkdir(exist_ok=True)
                shutil.copy2(source, PUBLIC / "uploads" / filename)
                public_item["photo"] = "uploads/" + filename
        items.append(public_item)
    sizes = [size for size in data.get("sizes", []) if size.get("available", True)]
    output = {"items": items, "sizes": sizes, "whatsapp": data.get("whatsapp", "")}
    (PUBLIC / "catalog.json").write_text(json.dumps(output, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print("GitHub Pages catalog exported.")

if __name__ == "__main__":
    main()
