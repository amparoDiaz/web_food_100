from flask import Flask, render_template, request
from werkzeug import secure_filename
import os
from flask import  redirect, url_for
from flask import send_from_directory
from classify import classify


UPLOAD_FOLDER = '../web_food_100'
ALLOWED_EXTENSIONS = set([ 'jpg'])

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
#app.config['STATIC_FOLDER'] = UPLOAD_FOLDER

@app.route('/shutdown', methods=['POST'])
def shutdown():
    shutdown_server()
    return 'Server shutting down...'

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS


@app.route('/uploads/result<filename>')
def uploaded_file(filename):

    return '''<div style="float:left; margin-right: 40px;">''' +classify('static/' +filename) + '''</div><div style="float:rigth; margin-right: 10px;">''' +   '''</p><img style="width:304px;height:228px; margin-top: 100px;" src="'''+ url_for('static', filename=filename)+ '''" /></div>'''



@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
	
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
	
        # if user does not select file, browser also
        # submit a empty part without filename
        if file.filename == '':
	  	flash('No selected file')
            	return redirect(request.url)

        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
	    print filename
            file.save(os.path.join(app.config['UPLOAD_FOLDER']+ "/static", filename))
            return redirect(url_for('uploaded_file',
                                    filename=filename))
    return '''
    <!doctype html>
    <title>Upload new Image</title>
 	<h1>Food Recogition</h1>
    <h3>Upload new Image </h3>
    <form action="" method=post enctype=multipart/form-data>
      <p><input type=file name=file>          	
	<input type=submit value=Classify> or
	<input type=submit value=Capture>
    </form>
    '''
if __name__ == '__main__':
   app.run(debug = True)
