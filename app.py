from flask import Flask, request, redirect, url_for, render_template
from flask_sqlalchemy import SQLAlchemy

app: Flask = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///memo.sqlite"
db:SQLAlchemy = SQLAlchemy(app)

class MemoItem(db.Model):
    id: int = db.Column(db.Integer, primary_key=True)
    title: str = db.Column(db.Text, nullable=False)
    body: str = db.Column(db.Text, nullable=True)
    
#データベースの初期化
with app.app_context():
    db.create_all()

#メモ一覧を表示
@app.route("/")
def index():
    items = MemoItem.query.order_by(MemoItem.title).all()
    items.insert(0, {"id":0, "title":"✒️新規作成", "body":""})
    return render_template("list.html", items=items)

#メモ編集画面
@app.route("/memo/<int:id>", methods=["GET", "POST"])
def memo():
    it = MemoItem.query.get(id)
    if id ==0 or it is None:
        it = MemoItem(title="__無題__", body="")
        
    if request.method == "POST":
        it.title = request.form.get("title","__無題__")
        it.body = request.form.get("body","")
        
        if it.title =="":
            return "タイトルは空にできません"
        
        if id == 0:
            db.session.add(it)
        db.session.commit()
        return redirect(url_for("index"))
    return render_template("memo.html", it=it)

if __name__ == "__main__":
    app.run(debug=True, port=8888)
 
