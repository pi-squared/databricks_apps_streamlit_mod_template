"""Run the app using only the standard library and the checked-in wheels."""

import hashlib
import json
import os
import platform
import shutil
import sys
import tempfile
from pathlib import Path, PurePosixPath
from zipfile import ZipFile

ROOT = Path(__file__).resolve().parent
VENDOR = ROOT / "vendor"


def activate_bundle() -> dict:
    """Verify and unpack this bundle, then make its packages importable."""
    if sys.implementation.name != "cpython" or sys.version_info[:2] != (3, 11):
        raise RuntimeError("This bundle requires CPython 3.11. Run: python3.11 run.py")
    if sys.platform != "linux" or platform.machine() != "x86_64":
        raise RuntimeError("This bundle requires Linux x86-64 (the Databricks Apps runtime).")
    libc, version = platform.libc_ver()
    if libc != "glibc" or tuple(map(int, version.split(".")[:2])) < (2, 28):
        raise RuntimeError("This bundle requires glibc 2.28 or newer; Ubuntu 22.04 is supported.")
    if not sys.flags.isolated or not sys.flags.no_site:
        raise RuntimeError("Bundle activation requires isolated Python: python3.11 -I -S ...")

    manifest_bytes = (VENDOR / "manifest.json").read_bytes()
    manifest = json.loads(manifest_bytes)
    for package in manifest["packages"]:
        wheel = VENDOR / "wheels" / package["wheel"]
        if wheel.name != package["wheel"]:
            raise RuntimeError("Invalid wheel path in the bundle manifest.")
        with wheel.open("rb") as source:
            digest = hashlib.file_digest(source, "sha256").hexdigest()
        if digest != package["sha256"]:
            raise RuntimeError(f"Checksum mismatch: {wheel.name}. Restore it from Git.")

    # Native extensions need real files. Cache only unpacked copies; the original
    # wheels, metadata, frontend assets and licenses remain in the Git checkout.
    fingerprint = hashlib.sha256(b"bundle-cache-v1\n" + manifest_bytes).hexdigest()
    cache = Path(tempfile.gettempdir()) / f"streamlit-template-{os.getuid()}"
    cache.mkdir(mode=0o700, parents=True, exist_ok=True)
    packages = cache / fingerprint
    import fcntl

    with (cache / "extract.lock").open("a") as lock:
        fcntl.flock(lock, fcntl.LOCK_EX)
        if not packages.exists():
            staging = Path(tempfile.mkdtemp(prefix="unpack-", dir=cache))
            try:
                for package in manifest["packages"]:
                    with ZipFile(VENDOR / "wheels" / package["wheel"]) as archive:
                        for member in archive.infolist():
                            path = PurePosixPath(member.filename)
                            if path.is_absolute() or ".." in path.parts:
                                raise RuntimeError(f"Invalid wheel member: {member.filename}")
                            # This launcher calls Streamlit's Python entry point;
                            # it does not need generated console-script wrappers.
                            if path.parts[0].endswith(".data"):
                                scheme = path.parts[1]
                                if scheme in {"purelib", "platlib"}:
                                    path = PurePosixPath(*path.parts[2:])
                                else:
                                    path = PurePosixPath("wheel-data", *path.parts)
                            destination = staging.joinpath(*path.parts)
                            if member.is_dir():
                                destination.mkdir(parents=True, exist_ok=True)
                            else:
                                destination.parent.mkdir(parents=True, exist_ok=True)
                                with archive.open(member) as source, destination.open("wb") as output:
                                    shutil.copyfileobj(source, output)
                staging.rename(packages)
            finally:
                if staging.exists():
                    shutil.rmtree(staging)

    # -I -S excludes user/global site-packages and ignores PYTHONPATH. Only this
    # checkout, this verified dependency bundle, and Python's stdlib are used.
    sys.path[:0] = [str(packages), str(ROOT)]
    # Streamlit otherwise mistakes unpacked wheels outside site-packages for a
    # development source tree and expects an unbundled frontend development server.
    os.environ.setdefault("STREAMLIT_GLOBAL_DEVELOPMENT_MODE", "false")
    return manifest


def check_bundle(manifest: dict) -> None:
    """Check dependency closure, wheel compatibility, and native imports offline."""
    from importlib.metadata import distribution
    from packaging.requirements import Requirement
    from packaging.tags import sys_tags
    from packaging.utils import canonicalize_name, parse_wheel_filename

    versions = {canonicalize_name(p["name"]): p["version"] for p in manifest["packages"]}
    supported = set(sys_tags())
    for package in manifest["packages"]:
        if not parse_wheel_filename(package["wheel"])[3] & supported:
            raise RuntimeError(f"Incompatible wheel: {package['wheel']}")
        metadata = distribution(package["name"])
        if metadata.version != package["version"]:
            raise RuntimeError(f"Unexpected installed version of {package['name']}")
        for dependency in metadata.requires or []:
            requirement = Requirement(dependency)
            if requirement.marker and not requirement.marker.evaluate({"extra": ""}):
                continue
            version = versions.get(canonicalize_name(requirement.name))
            if version is None or version not in requirement.specifier:
                raise RuntimeError(f"Missing or incompatible dependency: {dependency}")

    import dotenv
    import numpy
    import pandas
    import pyarrow
    import streamlit
    from PIL import Image

    assert pandas.DataFrame({"value": numpy.arange(3)}).shape == (3, 1)
    assert pyarrow.array([1, 2, 3]).to_pylist() == [1, 2, 3]
    with Image.open(ROOT / "assets" / "logo.png") as image:
        image.load()
    print(f"Verified {len(versions)} bundled packages; Streamlit {streamlit.__version__}.")


def main() -> None:
    if not sys.flags.isolated or not sys.flags.no_site:
        os.execv(sys.executable, [sys.executable, "-I", "-S", str(ROOT / "run.py"), *sys.argv[1:]])
    try:
        manifest = activate_bundle()
        if sys.argv[1:] == ["--check"]:
            check_bundle(manifest)
            return
    except (OSError, RuntimeError, ValueError) as error:
        raise SystemExit(f"Cannot start the bundled app: {error}") from error

    os.chdir(ROOT)
    os.environ.setdefault("STREAMLIT_BROWSER_GATHER_USAGE_STATS", "false")
    os.environ.setdefault("STREAMLIT_SERVER_HEADLESS", "true")
    os.environ.setdefault("STREAMLIT_SERVER_ADDRESS", "0.0.0.0")
    os.environ.setdefault("STREAMLIT_SERVER_PORT", os.environ.get("DATABRICKS_APP_PORT", "8501"))
    from streamlit.web.cli import main as streamlit_main

    sys.argv = ["streamlit", "run", str(ROOT / "app.py"), *sys.argv[1:]]
    streamlit_main()


if __name__ == "__main__":
    main()
