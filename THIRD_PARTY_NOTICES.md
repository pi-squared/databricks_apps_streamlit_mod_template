# Bundled third-party packages

The original wheel archives in `vendor/wheels/` retain their package metadata,
license texts, notices, native libraries, and frontend assets unchanged.
`vendor/manifest.json` records each archive's SHA-256 and license file paths.
The launcher also preserves these files when unpacking its temporary cache.

The Streamlit wheel omits a license file; its Apache 2.0 license is included
separately at `vendor/licenses/streamlit-1.41.1/LICENSE`, copied unchanged from
https://github.com/streamlit/streamlit/blob/1.41.1/LICENSE.

| Package | Version | License files inside its wheel |
| --- | --- | --- |
| altair | 5.5.0 | `altair-5.5.0.dist-info/licenses/LICENSE` |
| attrs | 26.1.0 | `attrs-26.1.0.dist-info/licenses/LICENSE` |
| blinker | 1.9.0 | `blinker-1.9.0.dist-info/LICENSE.txt` |
| cachetools | 5.5.2 | `cachetools-5.5.2.dist-info/LICENSE` |
| certifi | 2026.7.22 | `certifi-2026.7.22.dist-info/licenses/LICENSE` |
| charset-normalizer | 3.5.2 | `charset_normalizer-3.5.2.dist-info/licenses/`, `charset_normalizer-3.5.2.dist-info/licenses/LICENSE` |
| click | 8.5.0 | `click-8.5.0.dist-info/licenses/LICENSE.txt` |
| gitdb | 4.0.12 | `gitdb-4.0.12.dist-info/LICENSE` |
| GitPython | 3.2.0 | `gitpython-3.2.0.dist-info/licenses/LICENSE` |
| idna | 3.20 | `idna-3.20.dist-info/licenses/LICENSE.md` |
| Jinja2 | 3.1.6 | `jinja2-3.1.6.dist-info/licenses/LICENSE.txt` |
| jsonschema | 4.26.0 | `jsonschema-4.26.0.dist-info/licenses/COPYING` |
| jsonschema-specifications | 2025.9.1 | `jsonschema_specifications-2025.9.1.dist-info/licenses/COPYING` |
| markdown-it-py | 4.2.0 | `markdown_it_py-4.2.0.dist-info/licenses/LICENSE`, `markdown_it_py-4.2.0.dist-info/licenses/LICENSE.markdown-it` |
| MarkupSafe | 3.0.4 | `markupsafe-3.0.4.dist-info/licenses/`, `markupsafe-3.0.4.dist-info/licenses/LICENSE.txt` |
| mdurl | 0.1.2 | `mdurl-0.1.2.dist-info/LICENSE` |
| narwhals | 2.26.0 | `narwhals-2.26.0.dist-info/licenses/`, `narwhals-2.26.0.dist-info/licenses/LICENSE.md` |
| numpy | 2.4.6 | `numpy/_core/include/numpy/random/LICENSE.txt`, `numpy/ma/LICENSE`, `numpy/random/LICENSE.md`, `numpy-2.4.6.dist-info/licenses/`, `numpy-2.4.6.dist-info/licenses/LICENSE.txt`, `numpy-2.4.6.dist-info/licenses/numpy/_core/include/numpy/libdivide/LICENSE.txt`, `numpy-2.4.6.dist-info/licenses/numpy/_core/src/common/pythoncapi-compat/COPYING`, `numpy-2.4.6.dist-info/licenses/numpy/_core/src/highway/LICENSE`, `numpy-2.4.6.dist-info/licenses/numpy/_core/src/multiarray/dragon4_LICENSE.txt`, `numpy-2.4.6.dist-info/licenses/numpy/_core/src/npysort/x86-simd-sort/LICENSE.md`, `numpy-2.4.6.dist-info/licenses/numpy/_core/src/umath/svml/LICENSE`, `numpy-2.4.6.dist-info/licenses/numpy/fft/pocketfft/LICENSE.md`, `numpy-2.4.6.dist-info/licenses/numpy/linalg/lapack_lite/LICENSE.txt`, `numpy-2.4.6.dist-info/licenses/numpy/ma/LICENSE`, `numpy-2.4.6.dist-info/licenses/numpy/random/LICENSE.md`, `numpy-2.4.6.dist-info/licenses/numpy/random/src/distributions/LICENSE.md`, `numpy-2.4.6.dist-info/licenses/numpy/random/src/mt19937/LICENSE.md`, `numpy-2.4.6.dist-info/licenses/numpy/random/src/pcg64/LICENSE.md`, `numpy-2.4.6.dist-info/licenses/numpy/random/src/philox/LICENSE.md`, `numpy-2.4.6.dist-info/licenses/numpy/random/src/sfc64/LICENSE.md`, `numpy-2.4.6.dist-info/licenses/numpy/random/src/splitmix64/LICENSE.md` |
| packaging | 24.2 | `packaging-24.2.dist-info/LICENSE`, `packaging-24.2.dist-info/LICENSE.APACHE`, `packaging-24.2.dist-info/LICENSE.BSD` |
| pandas | 2.3.3 | `pandas-2.3.3.dist-info/LICENSE` |
| pillow | 11.3.0 | `pillow-11.3.0.dist-info/licenses/`, `pillow-11.3.0.dist-info/licenses/LICENSE` |
| protobuf | 5.29.6 | `protobuf-5.29.6.dist-info/LICENSE` |
| pyarrow | 25.0.1 | `pyarrow-25.0.1.dist-info/licenses/`, `pyarrow-25.0.1.dist-info/licenses/LICENSE.txt`, `pyarrow-25.0.1.dist-info/licenses/NOTICE.txt` |
| pydeck | 0.9.3 | `pydeck-0.9.3.dist-info/licenses/LICENSE.txt` |
| Pygments | 2.21.0 | `pygments-2.21.0.dist-info/licenses/LICENSE` |
| python-dateutil | 2.9.0.post0 | `python_dateutil-2.9.0.post0.dist-info/LICENSE` |
| python-dotenv | 1.2.2 | `python_dotenv-1.2.2.dist-info/licenses/LICENSE` |
| pytz | 2026.5 | `pytz-2026.5.dist-info/LICENSE.txt` |
| referencing | 0.37.0 | `referencing-0.37.0.dist-info/licenses/COPYING` |
| requests | 2.34.2 | `requests-2.34.2.dist-info/licenses/LICENSE`, `requests-2.34.2.dist-info/licenses/NOTICE` |
| rich | 13.9.4 | `rich-13.9.4.dist-info/LICENSE` |
| rpds-py | 2026.9.1 | `rpds_py-2026.9.1.dist-info/licenses/LICENSE` |
| six | 1.17.0 | `six-1.17.0.dist-info/LICENSE` |
| smmap | 5.0.3 | `smmap-5.0.3.dist-info/licenses/LICENSE` |
| streamlit | 1.41.1 | `vendor/licenses/streamlit-1.41.1/LICENSE` |
| tenacity | 9.2.1 | `tenacity-9.2.1.dist-info/licenses/LICENSE` |
| toml | 0.10.2 | `toml-0.10.2.dist-info/LICENSE` |
| tornado | 6.5.10 | `tornado-6.5.10.dist-info/licenses/`, `tornado-6.5.10.dist-info/licenses/LICENSE` |
| typing_extensions | 4.16.0 | `typing_extensions-4.16.0.dist-info/licenses/LICENSE` |
| tzdata | 2026.5 | `tzdata-2026.5.dist-info/licenses/LICENSE`, `tzdata-2026.5.dist-info/licenses/licenses/LICENSE_APACHE` |
| urllib3 | 2.8.0 | `urllib3-2.8.0.dist-info/licenses/LICENSE.txt` |
| watchdog | 6.0.0 | `watchdog-6.0.0.dist-info/COPYING`, `watchdog-6.0.0.dist-info/LICENSE` |
