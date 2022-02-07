from MUC_app import app
from MUC_app.controllers import users_controller, makers_controller, cars_controller


if __name__ == '__main__':
    app.run(debug=True)