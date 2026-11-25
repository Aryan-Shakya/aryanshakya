import json
import os
import re
import subprocess
import sys
import urllib.request

BASES = [os.environ["LABS_BASE"]] if os.environ.get("LABS_BASE") else [
    "https://www.aryanshakya.in",
    "https://aryanshakya.in",
]
IN_COLAB = "google.colab" in sys.modules
HEADERS = {"User-Agent": "labs-cli/1.0"}

HELP = """
  N  or  1,3  or  1-3  or  all   download lab(s)
  r N                            download (if needed) and run lab N
  v N                            preview lab N
  any text                       search by title
  l                              list all labs
  q                              quit
"""


def fetch(path):
    last = None
    for base in BASES:
        try:
            req = urllib.request.Request(base + path, headers=HEADERS)
            with urllib.request.urlopen(req, timeout=20) as r:
                return r.read()
        except Exception as e:
            last = e
    raise SystemExit("Could not reach the server: %s" % last)


def load_labs():
    return json.loads(fetch("/labs.json").decode("utf-8"))["labs"]


def show(labs, title=None):
    if title:
        print(title)
    if not labs:
        print("  (nothing found)")
        return
    for lab in labs:
        mark = "[x]" if os.path.exists(lab["file"]) else "[ ]"
        print("  %s %2d  %-52s %s" % (mark, lab["n"], lab["title"], lab["file"]))
    print("  [x] = already in this folder")


def confirm(question):
    try:
        return input(question + " [y/N] ").strip().lower() in ("y", "yes")
    except EOFError:
        return False


def download(lab, force=False):
    dest = lab["file"]
    if os.path.exists(dest) and not force:
        if not confirm("  %s already exists. Overwrite?" % dest):
            print("  skipped %s" % dest)
            return dest
    data = fetch("/dl/" + lab["file"])
    if not data.strip() or data.lstrip()[:15].lower().startswith((b"<!doctype html", b"<html")):
        print("  failed: %s did not download correctly" % dest)
        return None
    with open(dest, "wb") as f:
        f.write(data)
    print("  saved %s (%d lines)" % (dest, len(data.splitlines())))
    return dest


def run(path):
    print("  running %s ...\n" % path)
    if IN_COLAB:
        from IPython import get_ipython
        get_ipython().run_line_magic("run", path)
    else:
        if subprocess.call([sys.executable, path]) != 0:
            print("\n  if a module is missing, run:")
            print("  %s -m pip install numpy pandas matplotlib seaborn scikit-learn scipy" % sys.executable)


def view(lab, count=30):
    lines = fetch("/dl/" + lab["file"]).decode("utf-8", "replace").splitlines()
    print("  %s - %s (%d lines)\n" % (lab["file"], lab["title"], len(lines)))
    for line in lines[:count]:
        print("  | " + line)
    if len(lines) > count:
        print("  | ... %d more lines" % (len(lines) - count))


def parse_selection(text, labs):
    by_n = {lab["n"]: lab for lab in labs}
    tokens = text.lower().replace(",", " ").split()
    if tokens == ["all"]:
        return list(labs)
    chosen = []
    for tok in tokens:
        m = re.fullmatch(r"(\d+)(?:-(\d+))?", tok)
        if not m:
            return None
        a = int(m.group(1))
        b = int(m.group(2) or a)
        for k in range(min(a, b), max(a, b) + 1):
            if k not in by_n:
                print("  no lab %d" % k)
            elif by_n[k] not in chosen:
                chosen.append(by_n[k])
    return chosen


def norm(text):
    return re.sub(r"[^a-z0-9]", "", text.lower())


def search(text, labs):
    words = [norm(w) for w in text.split() if norm(w)]
    return [l for l in labs if all(w in norm(l["title"] + l["file"]) for w in words)]


def pick_one(arg, labs):
    sel = parse_selection(arg, labs) if arg else None
    if not sel:
        print("  give a lab number, e.g.  r 2")
        return None
    return sel[0]


def execute(line, labs, force=False):
    line = line.strip()
    if not line:
        show(labs)
        return True
    cmd, _, rest = line.partition(" ")
    cmd = cmd.lower()
    rest = rest.strip()
    if cmd in ("q", "quit", "exit"):
        return False
    if cmd in ("h", "help", "?"):
        print(HELP)
    elif cmd in ("l", "list", "ls"):
        show(labs)
    elif cmd in ("v", "view", "p", "preview"):
        lab = pick_one(rest, labs)
        if lab:
            view(lab)
    elif cmd in ("r", "run"):
        lab = pick_one(rest, labs)
        if lab:
            path = lab["file"] if os.path.exists(lab["file"]) and not force else download(lab, force)
            if path:
                run(path)
    elif cmd in ("g", "get", "d", "download"):
        for lab in parse_selection(rest, labs) or []:
            download(lab, force)
    elif cmd in ("s", "search", "f", "find"):
        show(search(rest, labs), "  results for '%s':" % rest)
    else:
        selection = parse_selection(line, labs)
        if selection is None:
            show(search(line, labs), "  results for '%s':" % line)
        else:
            for lab in selection:
                download(lab, force)
    return True


def main():
    args = sys.argv[1:]
    force = False
    if "-f" in args:
        force = True
        args.remove("-f")
    labs = load_labs()
    if args:
        execute(" ".join(args), labs, force)
        return
    print("\n  FAIML Labs  (%d available)  -  type h for help\n" % len(labs))
    show(labs)
    while True:
        try:
            line = input("\nlabs> ")
        except (EOFError, KeyboardInterrupt):
            print()
            return
        if not execute(line, labs, force):
            return


main()
