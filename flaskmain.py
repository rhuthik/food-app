from flask import Flask, render_template
from forms import RegistrationForm, LoginForm

app = Flask(__name__)

app.config['SECRET_KEY'] = '7976b37fadec64fb4ceae186f7533ec4'

@app.route("/", methods=['GET', 'POST'])
def reg():
    form=RegistrationForm()
    return render_template('register.html', form=form)


if __name__ == '__main__':
    app.run(debug=True)