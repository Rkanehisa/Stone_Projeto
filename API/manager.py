from API import app


if __name__ == '__main__':
    from API.db import db
    db.init_app(app)

    @app.before_first_request
    def create_tables():
        db.create_all()

    app.run()
