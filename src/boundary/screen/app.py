"""Launch shim: `python -m boundary.screen.app` → magicsquare.boundary.screen.app."""

from magicsquare.boundary.screen.app import main

if __name__ == "__main__":
    raise SystemExit(main())
