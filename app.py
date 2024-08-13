from flask import Flask, request, render_template, flash, redirect, url_for, session
from db import examCollection, userCollection, categoryCollection
from bson.objectid import ObjectId

app = Flask(__name__, template_folder="./templates")
app.config['SECRET_KEY'] = "twiceot9"

#Initial page
@app.route("/", methods=["GET"])
def login():
    return render_template("login.html.jinja")

#User login and register
@app.route("/userRegister", methods=["GET"])
def register():
    return render_template("userRegister.html.jinja")

#Menu render
@app.route("/menu", methods=["GET"])
def showMenu():
    return render_template("menu.html.jinja")

#Methods related to categories (CRUD)
@app.route("/categories/list", methods=["GET"])
def listCategories():
    categories = categoryCollection.find()
    return render_template("categoryList.html.jinja", categories=categories)

@app.route("/categories/create", methods=["GET", "POST"])
def createCategoryF():
    if request.method ==  "POST":

        name = request.form['categoryName']
        desc = request.form['categoryDescription']

        category = {
            "name": name,
            "description": desc
        }
        categoryCollection.insert_one(category)
        return render_template('categoryList.html.jinja', category=category)
    return render_template('createCategory.html.jinja')

#Base methods of exam (CRUD), not finished
@app.route("/exam/list", methods=["GET"])
def exams():
    exams = examCollection.find()
    return render_template("createExam.html.jinja", exams=exams)

@app.route("/exam/create", methods=["GET", "POST"])
def createExamF():
    if request.method ==  "POST":
        
        name = request.form['name']
        category = request.form['category']
        sampleType = request.form['sampleType']
        price = request.form['price']
        instructions = request.form['instructions']

        exam = {
            'name' : name,
            'category' : category,
            'sampleType' : sampleType,
            'price' : price,
            'instructions' : instructions
        }

        examCollection.insert_one(exam)
        exams = examCollection.find()
        return render_template('examList.html.jinja', exams=exams)
    return render_template('createExam.html.jinja')

@app.route("/exam/modify/<id>", methods=["GET", "POST"])
def modifyExamF(id):
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
                                            'instructions' : newElement['instructions']
                                          })
        return redirect(url_for('listExams'))
    return render_template("updateExams.html.jinja", exam=exam) 

@app.route("/exam/delete/<id>")
def deleteExamF(id):
    oid = ObjectId(id)
    exam = examCollection.delete_one({'_id': oid})
    exams = examCollection.find()
    return render_template("examList.html.jinja", exams=exams)

if __name__=='__main__':
    app.run(debug=True)