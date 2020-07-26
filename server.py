

from waitress import serve

from gpscheckin.wsgi import application

if __name__ == '__main__':
    serve(application, port='8081')
