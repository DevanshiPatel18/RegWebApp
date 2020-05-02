from flask import Flask,jsonify,request,render_template
from flask_pymongo import PyMongo
from bson.json_util import dumps, ObjectId
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = "secretkey" 
app.config['MONGO_URI'] = "mongodb://devanshi:I%40mavengers18@cluster0-shard-00-00-zvcda.mongodb.net:27017,cluster0-shard-00-01-zvcda.mongodb.net:27017,cluster0-shard-00-02-zvcda.mongodb.net:27017/name?ssl=true&replicaSet=Cluster0-shard-0&authSource=admin&retryWrites=true&w=majority"

mongo = PyMongo(app)

@app.route('/')
def gotoIndex() :
   return render_template("homepage.html")


@app.route('/homepage')
def homepage():
    return render_template("homepage.html")
@app.route('/login')
def log():
    return render_template("login.html")

@app.route('/login',methods=['POST','GET'])
def myLogin():
    _name=request.form['uname']
    _pwd=request.form['pwd']
    if mongo.db.password.find({"name":(_name)}).count() > 0 :
        passval = mongo.db.password.find({"name":(_name)},{"passsword" : 1})
        for val in passval :
            pval=val["passsword"]
        if check_password_hash(pval,_pwd) :
           return render_template("show.html",user=_name)
        else:
           return  render_template("error.html")
    else:
        return render_template("error.html")

@app.route("/show")
def myShow() :
    return render_template("show.html")

@app.route("/signup")
def mySignup() :
    return render_template("signup.html")

@app.route("/signup",methods=['POST','GET'])
def add():
    _name=request.form['uname']
    _pwd=request.form['pwd']
    _pwdc=request.form['pwdc']

    if _pwd == _pwdc and request.method=='POST':
        _hashed= generate_password_hash(_pwd)
        id =mongo.db.password.insert({'name': (_name),'passsword': (_hashed)})
        return render_template('login.html')
    else :
        return render_template("error.html")
    

if  __name__ == "__main__" :
    app.run(debug=True)