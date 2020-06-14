import sys


def main():
    mode = sys.argv[1]
    if mode == "mock-dataset":
        from src.batch_loader.data import mock_dataset
        n_rows = int(sys.argv[2])
        mock_dataset(n_rows)
    elif mode == "batch":
        from src.batch_loader import main
        main()
    elif mode == "server":
        from src.server import create_app
        app = create_app()
        app.run(host="0.0.0.0", port=5000, debug=True)


if __name__ == "__main__":
    main()
