from app import create_app

app, mongo = create_app()
app.secret_key = "123456abc"
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
    # app.run()
