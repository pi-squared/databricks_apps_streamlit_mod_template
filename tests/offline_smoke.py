"""Exercise real app pages with network calls blocked and site-packages disabled."""

import json
import os
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
import run

manifest = run.activate_bundle()
os.chdir(ROOT)
os.environ["STREAMLIT_LOGGER_LEVEL"] = "error"
from streamlit.testing.v1 import AppTest


class OfflineAppTests(unittest.TestCase):
    def setUp(self):
        self.network = patch("socket.socket.connect", side_effect=AssertionError("Network access attempted"))
        self.network.start()
        self.addCleanup(self.network.stop)

    def test_complete_bundle_and_native_libraries(self):
        run.check_bundle(manifest)

    def test_wheel_corruption_is_rejected_even_with_a_warm_cache(self):
        package = manifest["packages"][0]
        with tempfile.TemporaryDirectory() as directory:
            vendor = Path(directory)
            (vendor / "wheels").mkdir()
            (vendor / "wheels" / package["wheel"]).write_bytes(b"corrupt wheel")
            (vendor / "manifest.json").write_text(json.dumps({"packages": [package]}))
            with patch.object(run, "VENDOR", vendor):
                with self.assertRaisesRegex(RuntimeError, "Checksum mismatch"):
                    run.activate_bundle()

    def test_home_and_product_render(self):
        # Streamlit 1.41's AppTest does not provide a script cache for
        # st.navigation pages. Test the actual page scripts directly.
        app = AppTest.from_file(str(ROOT / "pages/home.py"), default_timeout=20).run()
        self.assertEqual(list(app.exception), [])
        self.assertEqual(app.title[0].value, "Home")
        app = AppTest.from_file(str(ROOT / "pages/product.py"), default_timeout=20).run()
        self.assertEqual(list(app.exception), [])
        self.assertEqual(app.header[0].value, "About")
        self.assertEqual([s.value for s in app.subheader], ["Left column", "Right column"])

    def test_greeting_and_counter(self):
        app = AppTest.from_file(str(ROOT / "pages/example.py"), default_timeout=20).run()
        self.assertEqual(list(app.exception), [])
        app.text_input[0].set_value("Offline reader").run()
        self.assertTrue(any("Hello, Offline reader!" in m.value for m in app.markdown))
        app.button[0].click().run()
        self.assertEqual(app.session_state["count"], 1)
        self.assertEqual(list(app.exception), [])

    def test_form_submission(self):
        app = AppTest.from_file(str(ROOT / "pages/form.py"), default_timeout=20).run()
        app.text_input[0].set_value("Ada")
        app.number_input[0].set_value(37)
        app.button[0].click().run()
        self.assertEqual(list(app.exception), [])
        self.assertEqual(app.success[0].value, "Hello, Ada! You are 37 years old.")


if __name__ == "__main__":
    unittest.main(verbosity=2)
