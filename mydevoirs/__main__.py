from mydevoirs.main import setup_start

if __name__ == "__main__":  # pragma: no cover_all
    # covered in check_executable.py

    app = setup_start().MyDevoirsApp()
    app.init_database()
    app.run()
