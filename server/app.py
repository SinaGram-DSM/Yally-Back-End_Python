from server.setapp import create_app

if __name__ == '__main__':

    from server.model import Base, engine
    Base.metadata.create_all(engine)

    app = create_app()
    app.run(debug=True)
