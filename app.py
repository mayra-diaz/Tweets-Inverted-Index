from flask import Flask, render_template, request, redirect, url_for, Response, flash
import json
import sys
import os
import glob
from IndexHandler import IndexHandler

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

app = Flask(__name__,
            static_url_path='', 
            static_folder='frontend/static',
            template_folder='frontend/templates')
app.secret_key = b'bd2/'

indexHandler = IndexHandler()
input_files = './input_files/'

@app.route('/')
def home():
   return render_template('buscador.html')

@app.route('/consulta', methods = ['POST'])
def consulta():
   message = json.loads(request.data)
   words =  message['values']
   cantidad = message['cantidad']
   data = indexHandler.analyze_query(words,cantidad)
   response = Response(
        response=json.dumps(data),
        status=200,
        mimetype='application/json'
    )
   return response

@app.route('/upload', methods = ['POST'])
def upload():
   uploaded_files = request.files.getlist("file")

   for file in uploaded_files:
      with open(input_files+str(file.filename), "wb") as file:
         file.write(file.read())
   
   indexHandler.add(input_files)
   filelist = glob.glob(os.path.join(input_files, "*"))
   for f in filelist:
       os.remove(f)
   
   flash(u'Los datos se han cargado de manera correcta.',  'alert-success')
   return render_template('buscador.html')

if __name__ == '__main__':
   app.run()