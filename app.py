from flask import Flask,render_template,request,flash,redirect,url_for
import os
import mysql.connector
import os.path
from random import random
import random
import sys
from flask_mysqldb import MySQL
import pymysql

app=Flask(__name__)
app.secret_key="123"
##############################################################
con=mysql.connector.connect(host='localhost',username='root',password='amal123'
,database='flaskdb')
cur = con.cursor()
print("images table successfuly created")
app.config['UPLOAD_FOLDER']="static/images" #the path for images folder
path = '.\\static\\images\\'
#########################################################################
@app.route("/upload",methods=['GET','POST'])
def upload():

    con=mysql.connector.connect(host='localhost',username='root',password='amal123'
,database='flaskdb')
    cur = con.cursor(dictionary=True)
    cur.execute("select * from images")
    data = cur.fetchall()
      #######################################
    if request.method=='POST':
        key= request.form['key']
        upload_image=request.files['upload_image']
        if upload_image.filename!='':
            filepath=os.path.join(app.config['UPLOAD_FOLDER'],upload_image.filename)
            upload_image.save(filepath)
            print(filepath) #in static folder path
            sizebytes = os.stat(path + upload_image.filename).st_size
            con=mysql.connector.connect(host='localhost',username='root',password='amal123'
,database='flaskdb')
            cur=con.cursor()
            cur.execute("SELECT keyy FROM images WHERE keyy = %s", [key])
            isNewKey = len(cur.fetchall()) == 0 #boolean
            if(isNewKey) :
             cur.execute("INSERT INTO images (keyy,image) VALUES(%s,%s)",(key,upload_image.filename))
             con.commit()
             flash("Image Uploaded Successfully ","success")
            else :
             cur.execute("UPDATE images SET image = %s WHERE keyy = %s", (upload_image.filename,key))
             flash("Image Updated Successfully for the already exist key","success")
             con.commit()
######################################################################
#This part in necessary to be like this, to be able to view the images immeaditly after
#uploading the images
            con=mysql.connector.connect(host='localhost',username='root',password='amal123'
,database='flaskdb')
            cur=con.cursor(dictionary=True)
            cur.execute("select * from images")
            data=cur.fetchall()
            return render_template("upload.html",data=data) #for the new uploaded images
    return render_template("upload.html",data=data) #the first if (else), to view the
    #already uploaded image
################################################################################
@app.route('/delete_record/<string:id>')
def delete_record(id):
    try:
        con=mysql.connector.connect(host='localhost',username='root',password='amal123'
,database='flaskdb')
        cur=con.cursor()
        cur.execute("delete from images where keyy=%s",[id])
        con.commit()
        flash("Record Deleted Successfully","success")
    except:
        flash("Record Deleted Failed", "danger")
    finally:
        return redirect(url_for("upload"))
#################################################################################
@app.route('/display',methods=["GET","POST"])
def display():
        if request.method == 'POST':
         con=mysql.connector.connect(host='localhost',username='root',password='amal123'
,database='flaskdb')
         cur=con.cursor()
         key= request.form.get('key')
         print('key:', key)
         cur.execute("SELECT keyy FROM images WHERE keyy = %s", [key])
         isNewKey = len(cur.fetchall()) == 0 #boolean
         if(isNewKey):
           return("No image for this key")
         else: 
            result = cur.execute("SELECT image FROM images WHERE keyy = %s ",[key]) 
            result = cur.fetchall()
            print("added to mem and displayed from db")
            return render_template("displayimage.html",image = result[0][0])
      
        else:
         return render_template("displayimage.html")
        
###############################################################################
@app.route('/keys') 
def viewkeys():
  data=get_keys()
  return render_template('keys.html',keys=data)
def get_keys():
 con=mysql.connector.connect(host='localhost',username='root',password='amal123'
,database='flaskdb')
 cur=con.cursor()
 cur.execute("SELECT keyy FROM images")
 keys=cur.fetchall()
 keys=[str(val[0]) for val in keys]
 return keys
###############################################################################

@app.route('/home')  
def home():
 return render_template('home.html')

@app.route('/')  
def viewhome():
 return render_template('home.html')
#############################################
if __name__ == '__main__':
    app.run(debug=True)
