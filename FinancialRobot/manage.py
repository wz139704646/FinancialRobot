from app import create_app

app = create_app()

if __name__ == '__main__':
    app.run(debug=False)

# from flask import Flask
#
# app = Flask(__name__)
#
#
# @app.route('/')
# def index():
#     return 'Hello World'
#
#
# if __name__ == '__main__':
#     app.run(debug=True)
=======
    app.run(host='0.0.0.0', port=5000)
    # app.run()
