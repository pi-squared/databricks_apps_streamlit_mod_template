"""Check a cold launcher, frontend assets, and real navigation over loopback."""

import asyncio
import os
import re
import socket
import subprocess
import sys
import tempfile
import time
from pathlib import Path
from urllib.parse import urljoin
from urllib.request import ProxyHandler, build_opener

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
import run

run.activate_bundle()
from streamlit.proto.BackMsg_pb2 import BackMsg
from streamlit.proto.ForwardMsg_pb2 import ForwardMsg
from tornado.httpclient import HTTPRequest
from tornado.websocket import websocket_connect

# Use the real launcher's main(), blocking every outbound server connection.
# -I -S also prevents fallback to packages installed outside the checkout.
SERVER = """
import socket, sys
sys.path.insert(0, sys.argv[1])
connect = socket.socket.connect
def loopback_only(self, address):
    if not isinstance(address, tuple) or address[0] not in {'127.0.0.1', '::1'}:
        raise AssertionError(f'External network access attempted: {address}')
    return connect(self, address)
socket.socket.connect = loopback_only
from run import main
sys.argv = ['run.py', '--server.address', '127.0.0.1', '--logger.level', 'error']
main()
"""


async def check_navigation(base: str) -> None:
    connection = await websocket_connect(
        HTTPRequest(base.replace("http:", "ws:") + "/_stcore/stream", headers={"Origin": base}),
        subprotocols=["streamlit"],
    )
    pages = {}
    try:
        for title, heading in [("Readme", "Home"), ("Example", "Example page"),
                               ("Product", "About"), ("Form", "Form")]:
            request = BackMsg()
            request.rerun_script.page_script_hash = pages.get(title, "")
            await connection.write_message(request.SerializeToString(), binary=True)
            headings = []
            while True:
                payload = await asyncio.wait_for(connection.read_message(), timeout=20)
                if payload is None:
                    raise AssertionError("Server closed the WebSocket before rendering the page")
                message = ForwardMsg()
                message.ParseFromString(payload)
                kind = message.WhichOneof("type")
                if kind == "navigation":
                    pages.update({page.page_name: page.page_script_hash for page in message.navigation.app_pages})
                if kind == "delta" and message.delta.HasField("new_element"):
                    element = message.delta.new_element
                    if element.HasField("exception"):
                        raise AssertionError(element.exception.message)
                    if element.HasField("heading"):
                        headings.append(element.heading.body)
                if kind == "script_finished":
                    break
            assert heading in headings, (title, headings)
        assert set(pages) == {"Readme", "Example", "Product", "Form"}, pages
    finally:
        connection.close()


def main() -> None:
    with socket.socket() as probe:
        probe.bind(("127.0.0.1", 0))
        port = probe.getsockname()[1]
    base = f"http://127.0.0.1:{port}"
    http = build_opener(ProxyHandler({}))
    with tempfile.TemporaryDirectory(prefix="template-cold-start-") as directory:
        environment = dict(os.environ, TMPDIR=directory, DATABRICKS_APP_PORT=str(port))
        environment.pop("STREAMLIT_SERVER_PORT", None)
        environment["STREAMLIT_BROWSER_GATHER_USAGE_STATS"] = "false"
        with (Path(directory) / "server.log").open("w+") as log:
            server = subprocess.Popen([sys.executable, "-I", "-S", "-c", SERVER, str(ROOT)],
                                      cwd=directory, env=environment, stdout=log, stderr=log)
            try:
                deadline = time.monotonic() + 30
                while time.monotonic() < deadline:
                    if server.poll() is not None:
                        raise AssertionError("Server exited during startup")
                    try:
                        with http.open(base + "/_stcore/health", timeout=1) as response:
                            assert response.read() == b"ok"
                        break
                    except OSError:
                        time.sleep(0.1)
                else:
                    raise AssertionError("Server did not become healthy")
                with http.open(base, timeout=5) as response:
                    html = response.read().decode()
                javascript = re.search(r'src="([^\"]+\.js)"', html)
                assert javascript is not None, "Missing bundled frontend script"
                with http.open(urljoin(base + "/", javascript[1]), timeout=5) as response:
                    assert len(response.read()) > 1000
                asyncio.run(check_navigation(base))
                print("Cold launch, health, bundled frontend, and all four navigation pages passed.")
            except BaseException:
                log.seek(0)
                print(log.read(), file=sys.stderr)
                raise
            finally:
                server.terminate()
                try:
                    server.wait(timeout=10)
                except subprocess.TimeoutExpired:
                    server.kill()
                    server.wait()


if __name__ == "__main__":
    main()
