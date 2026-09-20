"""Launch the interactive thesis showcase website locally.

Usage:
    .\\venv\\Scripts\\python.exe scripts/run_website.py
"""
import http.server
import os
import socketserver
import sys
import webbrowser

PORT = 8000
ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
WEBSITE_DIR = os.path.join(ROOT_DIR, "website")


class NoCacheHandler(http.server.SimpleHTTPRequestHandler):
    def end_headers(self):
        self.send_header('Cache-Control', 'no-cache, no-store, must-revalidate')
        self.send_header('Pragma', 'no-cache')
        self.send_header('Expires', '0')
        super().end_headers()

    def log_message(self, format, *args):
        # Clean logging
        sys.stderr.write("%s - - [%s] %s\n" % (self.address_string(), self.log_date_time_string(), format % args))


def main():
    data_summary = os.path.join(WEBSITE_DIR, "data", "summary.json")
    if not os.path.exists(data_summary):
        print("[run_website] Building website data first...")
        import build_website_data
        build_website_data.export_data()

    os.chdir(WEBSITE_DIR)

    handler = NoCacheHandler
    # Allow port reuse immediately
    socketserver.TCPServer.allow_reuse_address = True

    try:
        with http.server.ThreadingHTTPServer(("", PORT), handler) as httpd:
            url = f"http://localhost:{PORT}"
            print(f"============================================================")
            print(f"  Catching Greenwashing from Space — Interactive Showcase")
            print(f"  Serving at: {url}")
            print(f"  Press Ctrl+C to stop the server.")
            print(f"============================================================")
            try:
                webbrowser.open(url)
            except Exception:
                pass
            httpd.serve_forever()
    except OSError as e:
        if "address already in use" in str(e).lower() or e.errno == 98 or e.errno == 10048:
            print(f"[run_website] Port {PORT} is already in use. Opening {url}...")
            webbrowser.open(f"http://localhost:{PORT}")
        else:
            raise


if __name__ == "__main__":
    main()
