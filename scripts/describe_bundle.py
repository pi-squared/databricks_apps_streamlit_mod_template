"""Generate the checked-in lock, inventory, and license index from local wheels."""

import hashlib
import json
from email.parser import BytesParser
from pathlib import Path
from zipfile import ZipFile

ROOT = Path(__file__).resolve().parents[1]
packages = []
for wheel in sorted((ROOT / "vendor" / "wheels").glob("*.whl")):
    with ZipFile(wheel) as archive:
        metadata_path = next(p for p in archive.namelist() if p.endswith(".dist-info/METADATA"))
        metadata = BytesParser().parsebytes(archive.read(metadata_path))
        licenses = [p for p in archive.namelist() if any(
            word in Path(p).name.lower() for word in ("license", "licence", "copying", "notice")
        )]
    packages.append({
        "name": str(metadata["Name"]),
        "version": str(metadata["Version"]),
        "wheel": wheel.name,
        "size": wheel.stat().st_size,
        "sha256": hashlib.sha256(wheel.read_bytes()).hexdigest(),
        "license": str(metadata.get("License-Expression") or metadata.get("License") or "See wheel metadata"),
        "license_files": licenses,
        "supplemental_license_files": [
            str(path.relative_to(ROOT))
            for path in sorted((ROOT / "vendor" / "licenses" / f"{metadata['Name'].lower()}-{metadata['Version']}").glob("*"))
            if path.is_file()
        ],
    })

manifest = {
    "format": 1,
    "runtime": "CPython 3.11 / Linux x86-64 / glibc >= 2.28",
    "source_index": "https://pypi.org/simple",
    "direct_requirements": (ROOT / "requirements.in").read_text().splitlines(),
    "packages": packages,
}
(ROOT / "vendor" / "manifest.json").write_text(json.dumps(manifest, indent=2) + "\n")
lock = [
    "# Complete dependency closure for CPython 3.11 on Linux x86-64.",
    "# Optional offline pip installation; run.py does not use pip.",
    "--no-index", "--find-links vendor/wheels", "--require-hashes", "",
]
lock.extend(f"{p['name']}=={p['version']} --hash=sha256:{p['sha256']}" for p in packages)
(ROOT / "requirements.lock").write_text("\n".join(lock) + "\n")
index = [
    "# Bundled third-party packages", "",
    "The original wheel archives in `vendor/wheels/` retain their package metadata,",
    "license texts, notices, native libraries, and frontend assets unchanged.",
    "`vendor/manifest.json` records each archive's SHA-256 and license file paths.",
    "The launcher also preserves these files when unpacking its temporary cache.", "",
    "The Streamlit wheel omits a license file; its Apache 2.0 license is included",
    "separately at `vendor/licenses/streamlit-1.41.1/LICENSE`, copied unchanged from",
    "https://github.com/streamlit/streamlit/blob/1.41.1/LICENSE.", "",
    "| Package | Version | License files inside its wheel |",
    "| --- | --- | --- |",
]
for package in packages:
    files = ", ".join(f"`{p}`" for p in package["license_files"] + package["supplemental_license_files"]) or "See `.dist-info/METADATA`"
    index.append(f"| {package['name']} | {package['version']} | {files} |")
(ROOT / "THIRD_PARTY_NOTICES.md").write_text("\n".join(index) + "\n")
print(f"Inventoried {len(packages)} wheels ({sum(p['size'] for p in packages) / 1024**2:.1f} MiB).")
