from flask import Flask

from views import home_view
from views import sample_view
from views import waybill_view


def create_app():
    app = Flask(__name__)

    app.register_blueprint(home_view.bp)
    app.register_blueprint(sample_view.bp)
    app.register_blueprint(waybill_view.bp)

    return app


if __name__ == "__main__":
    create_app().run()
