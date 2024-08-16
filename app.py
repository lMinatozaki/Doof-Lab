from collections import Counter
from flask import Flask, request, render_template, flash, redirect, url_for
from db import examCollection, userCollection, categoryCollection, indicationCollection
from bson.objectid import ObjectId
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from random import randint
from collections import defaultdict

app = Flask(__name__, template_folder="./templates")
app.config['SECRET_KEY'] = "twiceot9"
login_manager = LoginManager()
login_manager.init_app(app)

class User(UserMixin):
    pass

@login_manager.user_loader
def load_user(user_id):
    user = userCollection.find_one({'_id': ObjectId(user_id)})
    if user:
        user_obj = User()
        user_obj.id = str(user['_id'])
        return user_obj
    return None

#Initial page
@app.route("/", methods=["GET"])
def showHome():
    return render_template("home.html.jinja")

#User login and register
@app.route("/register", methods=["GET", "POST"])
def registerF():
    if request.method ==  "POST":

        user = request.form['username']
        pw = request.form['password']

        user = {
            "username": user,
            "password": pw
        }
        
        userCollection.insert_one(user)
        return redirect(url_for('loginF'))
    return render_template('userRegister.html.jinja')

@app.route("/login", methods=["GET", "POST"])
def loginF():
    if request.method == "POST":
        username = request.form['username']
        password = request.form['password']

        user = userCollection.find_one({'username': username, 'password': password})
        if user:
            user_obj = User()
            user_obj.id = str(user['_id'])
            login_user(user_obj)
            return redirect(url_for('showMenu'))
        else:
            flash('Invalid username or password', 'error')

    return render_template("login.html.jinja")

@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for('showHome'))

#Menu render
@app.route("/menu", methods=["GET"])
@login_required
def showMenu():
    return render_template("menu.html.jinja")

#Methods related to categories (CRUD)
@app.route("/category/list", methods=["GET"])
@login_required
def listCategories():
    categories = categoryCollection.find()
    return render_template("categoryList.html.jinja", categories=categories)

@app.route("/category/create", methods=["GET", "POST"])
@login_required
def createCategory():
    if request.method ==  "POST":

        name = request.form['categoryName']
        desc = request.form['categoryDescription']

        category = {
            "name": name,
            "description": desc
        }
        categoryCollection.insert_one(category)
        return redirect(url_for('listCategories'))
    return render_template('createCategory.html.jinja')

@app.route('/category/modify/<id>', methods=['GET', 'POST'])
@login_required
def modifyCategory(id):
    oid = ObjectId(id)
    category = categoryCollection.find_one({'_id': oid})
    if request.method == "POST":
        newElement = request.form
        categoryCollection.replace_one({'_id': oid}, 
                                       {
                                            'name': newElement['categoryName'],
                                            'description': newElement['categoryDescription']})    
        return redirect(url_for('listCategories'))
    return render_template("updateCategories.html.jinja", category = category)

@app.route("/category/delete/<id>")
@login_required
def deleteCategory(id):
    oid = ObjectId(id)
    category = categoryCollection.delete_one({'_id': oid})
    categories = categoryCollection.find()
    return redirect(url_for('listCategories'))

#Methods related to indications (CRUD)
@app.route("/indication/list", methods=["GET"])
@login_required
def listIndications():
    indications = indicationCollection.find()
    return render_template("indicationList.html.jinja", indications=indications)

@app.route('/indication/create', methods=['GET', 'POST'])
@login_required
def createIndication():
    if request.method == "POST":

        desc = request.form['indicationDescription']

        indication = {
            'description' : desc 
        }

        indicationCollection.insert_one(indication)
        return redirect(url_for('listIndications'))
    return render_template("createIndication.html.jinja")

@app.route('/indication/modify/<id>', methods=['GET', 'POST'])
@login_required
def modifyIndication(id):
    oid = ObjectId(id)
    indication = indicationCollection.find_one({'_id': oid})
    if request.method == "POST":
        newElement= request.form
        indicationCollection.replace_one({'_id': oid}, 
                                         {
                                          'description': newElement['indicationDescription']})    
        return redirect(url_for('listIndications'))
    return render_template("updateIndication.html.jinja", indication=indication)

@app.route("/indication/delete/<id>")
@login_required
def deleteIndication(id):
    oid = ObjectId(id)
    indication = indicationCollection.delete_one({'_id': oid})
    indications = indicationCollection.find()
    return redirect(url_for('listIndications'))

#Base methods of exam (CRUD)
@app.route("/exam/catalog", methods=["GET"])
@login_required
def listExams():
    categoryFilter = request.args.get('category')
    sampleTypeFilter = request.args.get('sampleType')

    if categoryFilter:
        filteredExams = examCollection.find({'category': categoryFilter})
    else:
        filteredExams = examCollection.find()

    if sampleTypeFilter:
        filteredExams = [exam for exam in filteredExams if exam['sampleType'] == sampleTypeFilter]

    categories = categoryCollection.find()
    return render_template("catalog.html.jinja", exams=filteredExams, categories=categories)

@app.route("/exam/create", methods=["GET", "POST"])
@login_required
def createExam():
    if request.method ==  "POST":
        
        examID = "E" + str(randint(1000, 5000))
        name = request.form['name']
        category = request.form['category']
        sampleType = request.form['sampleType']
        price = request.form['price']
        indication = request.form['indication']

        if price is None or not price.isdigit():
            flash("Price must be a valid numeric value.", "error")

        price = float(price)

        exam = {
            'examID': examID,
            'name' : name,
            'category' : category,
            'sampleType' : sampleType,
            'price' : price,
            'indication' : indication
        }

        examCollection.insert_one(exam)
        return redirect(url_for('listExams'))
    categories = categoryCollection.find()
    exams = examCollection.find()
    indications = indicationCollection.find()
    return render_template('createExam.html.jinja', categories=categories, exams=exams, indications=indications)

@app.route("/exam/modify/<id>", methods=["GET", "POST"])
@login_required
def modifyExam(id):
    oid = ObjectId(id)
    exam = examCollection.find_one({'_id': oid})
    if request.method == "POST":
        newElement = request.form
        exam = examCollection.replace_one({'_id': oid}, 
                                          {
                                            'name': newElement['name'],
                                            'category': newElement['category'],
                                            'sampleType' : newElement['sampleType'],
                                            'price' : newElement['price'],
                                            'indication' : newElement['indication']
                                          })
        return redirect(url_for('listExams'))
    categories = categoryCollection.find()
    indications = indicationCollection.find()
    return render_template("updateExams.html.jinja", exam=exam, categories=categories, indications=indications) 

@app.route("/exam/delete/<id>")
@login_required
def deleteExam(id):
    oid = ObjectId(id)
    exam = examCollection.delete_one({'_id': oid})
    exams = examCollection.find()
    return redirect(url_for('listExams'))

@app.route("/exam/details/<id>", methods=["GET"])
@login_required
def getExamDetails(id):
    oid = ObjectId(id)
    exam = examCollection.find_one({'_id': oid})
    return render_template("examDetails.html.jinja", exam=exam)

#Report method
@app.route("/report", methods=["GET"])
def viewReport():
    exams = examCollection.find()

    #Method for counting all the exam categories
    categoryCount = Counter(exam['category'] for exam in examCollection.find())

    #Method for obtaining the most common exam indication
    indications = [exam['indication'] for exam in exams] 
    indicationCount = {}
    for indication in indications:
        if indication in indicationCount:
            indicationCount[indication] += 1
        else:
            indicationCount[indication] = 1
    #
    mostCommonIndication = max(indicationCount, key=indicationCount.get)

    #Method for getting the price intervals and counting each interval
    priceIntervals = {
        '1 - 100 bs': 0,
        '101 - 200 bs': 0,
        '201 - 300 bs': 0,
        '301 - 500 bs': 0,
        '501+ bs': 0
    }

    for exam in examCollection.find():
        price = float(exam['price'])
        if price <= 100:
            priceIntervals['1 - 100 bs'] += 1
        elif price <= 200:
            priceIntervals['101 - 200 bs'] += 1
        elif price <= 300:
            priceIntervals['201 - 300 bs'] += 1
        elif price <= 500:
            priceIntervals['301 - 500 bs'] += 1
        else:
            priceIntervals['501+ bs'] += 1
    
    return render_template("report.html.jinja", categoryCount=categoryCount, mostCommonIndication=mostCommonIndication, priceIntervals=priceIntervals)

if __name__=='__main__':
    app.run(debug=True)