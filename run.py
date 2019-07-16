from flaskblog import create_app

# create app with default configs
app = create_app()

if __name__ == "__main__":
    app.run(host='0.0.0.0')
