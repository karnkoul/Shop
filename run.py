from shop import app, initialize_db

if __name__ == "__main__":

    initialize_db()
    app.run(debug=True)