import json
import pathlib
import re

root = pathlib.Path(__file__).resolve().parent.parent
labs = []

for path in sorted((root / "dl").glob("2323l*.py")):
    m = re.fullmatch(r"2323l(\d+)\.py", path.name)
    if not m:
        continue
    text = path.read_text(encoding="utf-8")
    first = text.splitlines()[0] if text else ""
    t = re.match(r"#\s*LAB\s*(\d+)\s*:\s*(.+)", first)
    title = t.group(2).strip() if t else path.stem
    labs.append({"n": int(m.group(1)), "title": title, "file": path.name, "lines": len(text.splitlines())})

labs.sort(key=lambda x: x["n"])
(root / "labs.json").write_text(json.dumps({"labs": labs}, indent=2) + "\n", encoding="utf-8")
print(f"labs.json: {len(labs)} lab(s)")
for lab in labs:
    print(f"  {lab['n']}: {lab['title']} ({lab['file']})")
