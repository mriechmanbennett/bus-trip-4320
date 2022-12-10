"""Application entry point.""" 
from flask_wtforms_tutorial import create_app

app = create_app()



# Check if a seat is available. Returns True if available and False if not

if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)
