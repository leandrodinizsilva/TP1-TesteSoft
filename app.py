from provasonline import app, db
from flask_wtf.csrf import CSRFProtect

csrf = CSRFProtect(app)

if __name__ == '__main__':
	db.create_all()
	app.run(debug=True)
	csrf.init_app(app)