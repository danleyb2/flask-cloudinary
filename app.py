from flask import Flask,request,render_template,jsonify,g
import os
import cloudinary
import sqlite3



import cloudinary.api,cloudinary.uploader

def get_db_config(name):
    row = g.db.execute("select value from settings where name='"+name+"'").fetchone()
    return row[0]

cloudinary.config(
    cloud_name =    get_db_config('cloud_name'),# "danleyb2" 
    api_key = get_db_config('api_key'), #"944437879321554" 
    api_secret = get_db_config('api_secret')  #"LA1IetNarUth6vzQU1XlLfQANsY"
    )

app=Flask(__name__)
app.config.from_object(__name__)

app.config.update(dict(
    DATABASE=os.path.join(app.root_path, 'app_db.db'),
    SECRET_KEY='myveryuniqueappsecretkey',
    USERNAME='admin',
    PASSWORD='default'
))

def get_db():
    if not hasattr(g,'sqlite_db_conn'):
        g.sqlite_db_conn=connect_to_db()
    return g.sqlite_db_conn

def sqlite3_dict_factory(cursor,row):
    d={}
    for idx,col in enumerate(cursor.description):
        d[col[0]]=row[idx]
    return d
    
def connect_to_db():
    c=sqlite3.connect(app.config['DATABASE'])
    c.row_factory = sqlite3_dict_factory
    return c

def init_db():
    db = get_db()
    with app.open_resource('schema.sql', mode='r') as f:
        db.cursor().executescript(f.read())
    db.commit()


@app.cli.command('initdb')
def initdb_command():
    print("Initializing DB")
    init_db()
    print("Initialized DB")


app.config.from_envvar('MYAPP_SETTINGS', silent=True)

@app.route('/')
def hello_world():
    return 'Flask cloudinary.'
@app.route('/upload',methods=['GET','POST'])
def upload_photo():
    if request.method=='POST':
        f=request.files['image_file']
        img_up=cloudinary.uploader.upload(f)
        return jsonify(img_up)
    else:
        return render_template('index.html')

@app.teardown_appcontext
def close_db(error):
    if hasattr(g, 'sqlite_db'):
        g.sqlite_db.close()

if __name__=='__main__':
    app.debug=True
    app.run(
        host=os.getenv('IP','0.0.0.0'),
        port=int(os.getenv('PORT','8080'))
        )