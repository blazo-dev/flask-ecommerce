from app import create_app, db

if __name__ == '__main__':
    app = create_app()

    # Ensure all tables defined in models are created in the database
    with app.app_context():
        db.create_all()
        print("Tables created successfully!")

    # Run the Flask app in debug mode
    app.run(debug=True)
