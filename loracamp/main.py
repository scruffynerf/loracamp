import argparse
from pathlib import Path
from .engine import LoraCampEngine

def main():
    parser = argparse.ArgumentParser(description="LoraCamp: Static Site Generator for Models")
    parser.add_argument("catalog", type=str, help="Path to your model catalog directory")
    parser.add_argument("--build", action="store_true", help="Build the site")
    parser.add_argument("--preview", action="store_true", help="Start a local web server to preview the site")
    parser.add_argument("--port", type=int, default=8000, help="Port to use for the local web server")
    parser.add_argument("--cdn-url", type=str, help="Optional CDN URL for large files")
    parser.add_argument("--output", type=str, default=".", help="Output directory (default: current)")
    parser.add_argument(
        "--include", action="append", dest="include_patterns", metavar="PATTERN",
        help="Only process paths containing this pattern (can be used multiple times)"
    )
    parser.add_argument(
        "--exclude", action="append", dest="exclude_patterns", metavar="PATTERN",
        help="Skip paths containing this pattern (can be used multiple times)"
    )

    args = parser.parse_args()

    catalog_path = Path(args.catalog).resolve()
    output_path = Path(args.output).resolve()
    
    if args.build or args.preview:
        if args.build:
            engine = LoraCampEngine(
                catalog_dir=catalog_path,
                output_dir=output_path,
                cdn_url=args.cdn_url,
                include_patterns=args.include_patterns,
                exclude_patterns=args.exclude_patterns,
            )
            engine.build()
            
        if args.preview:
            import os
            import http.server
            import socketserver
            
            # The engine builds into output_dir / "yoursite"
            serve_dir = output_path / "yoursite"
            if not serve_dir.exists():
                print(f"Error: Preview directory {serve_dir} does not exist. Did you forget to --build?")
                return
                
            os.chdir(serve_dir)
            Handler = http.server.SimpleHTTPRequestHandler
            
            class TCPServer(socketserver.TCPServer):
                allow_reuse_address = True
                
            with TCPServer(("", args.port), Handler) as httpd:
                print(f"Serving preview at http://localhost:{args.port}/")
                print("Press Ctrl+C to stop.")
                try:
                    httpd.serve_forever()
                except KeyboardInterrupt:
                    print("\nStopping server.")
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
