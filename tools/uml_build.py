#!/usr/bin/env python
import argparse, os, sys, time
from pathlib import Path

def run_pyreverse(project: str, src: Path, outdir: Path):
    print("• Building class diagram via pyreverse ...")
    os.environ["PYTHONPATH"] = str(src.parent) + (os.pathsep + os.environ["PYTHONPATH"] if os.environ.get("PYTHONPATH") else "")
    outdir.mkdir(parents=True, exist_ok=True)
    cwd = os.getcwd()
    os.chdir(outdir)
    try:
        from pylint.pyreverse.main import Run
        args = [
            "--source-roots", str(src.parent),
            "-o", "puml",
            "-p", project,
            "-A",      # include ancestors
            "-S",      # include associations
            "-f", "ALL",
            str(src)
        ]
        try:
            Run(args)
        except SystemExit as e:
            if isinstance(e.code, int) and e.code != 0:
                raise
        classes = Path(f"classes_{project}.puml").resolve()
        if not classes.exists():
            raise FileNotFoundError(f"Expected {classes} from pyreverse but it was not created.")
        print(f"✓ Wrote {classes}")
        return classes
    finally:
        os.chdir(cwd)

def render_kroki(puml_file: Path, tries: int = 3, timeout: int = 30):
    import requests
    puml_file = puml_file.resolve()
    png = puml_file.with_suffix(puml_file.suffix + ".png")
    last_err = None
    for i in range(tries):
        try:
            r = requests.post("https://kroki.io/plantuml/png", data=puml_file.read_text(encoding="utf-8"), timeout=timeout)
            r.raise_for_status()
            png.write_bytes(r.content)
            print(f"✓ PNG: {png}")
            return png
        except Exception as e:
            last_err = e
            time.sleep(1.5 * (i + 1))
    raise RuntimeError(f"Kroki render failed for {puml_file}: {last_err}")

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--project", required=True)
    ap.add_argument("--src", required=True)
    ap.add_argument("--out", required=True)
    args = ap.parse_args()
    project = args.project
    src = Path(args.src).resolve()
    outdir = Path(args.out).resolve()

    classes_puml = run_pyreverse(project, src, outdir)
    try:
        render_kroki(classes_puml)
    except Exception as e:
        print(f"WARNING: PNG rendering failed ({e}).", file=sys.stderr)

    print(f"✓ UML generated successfully in: {outdir}")

if __name__ == "__main__":
    main()


