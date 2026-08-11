from python_qr_project.views import create_app


# DO NOT STORE CONFIG HERE, put it in the factory.
# Some options may only apply when --debug is used.
def main():
    app = create_app()
    app.run(host="0.0.0.0", port=5000)
