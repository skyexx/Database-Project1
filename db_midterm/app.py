from flask import Flask,request,Response,redirect,render_template,request,url_for,session,flash,Blueprint
from flask_bootstrap import Bootstrap
import cx_Oracle



app=Flask(__name__) # 透過__name__確定app檔案位置，方便找到其他構成app的檔案



# conn=cx_Oracle.connect("Group6/Group666@140.117.69.58:1521/Group6",encoding="UTF-8")
# conn=cx_Oracle.connect('Group6', 'Group666', "140.117.69.58:1521/Group6",encoding="UTF-8")

tns=cx_Oracle.makedsn('140.117.69.58',1521,'orcl')
conn=cx_Oracle.connect('Group6','Group666',tns)


@app.route('/',methods=['POST','GET'])
def login():
    if request.method=='POST':
        email=request.form['email']
        pwd=request.form['pwd'] # 抓取form.html中input text的值
        if email and pwd: # 輸入欄位不可為空
            cursor=conn.cursor()
            check_db=''' SELECT * FROM "User" WHERE EMAIL='%s' and PHONE='%s' ''' % (email,pwd)
            cursor.execute(check_db)
            cursor.close()
            test=cursor.fetchone()
            
            # return render_template('test.html',test=test)
            if test[0]==True:
                success_notify='登入成功'
                session['email']=email # 運用session存值，代表該用戶確實存在於資料庫中
                session['pwd']=pwd
                return render_template('login.html',success_notify=success_notify,failed_notify=None)
            else:
                failed_notify='查無此用戶請先註冊帳號'
                return render_template('login.html',success_notify=None,failed_notify=failed_notify)
        else:
            return render_template('login.html')
    # else:
    #     if 'user' in session:
    #         return redirect(url_for('login'))
    #     return render_template('login.html')
    return render_template('login.html')

@app.route('/flight')
def info():
    cursor=conn.cursor()
    search_flight=''' SELECT * FROM FLIGHT '''
    cursor.execute(search_flight)
    result=cursor.fetchall()
    cursor.close()
    
    return render_template('flight_info.html',result=result)

    










@app.errorhandler(404) # request錯誤的路徑
def page_not_found(error):
    return render_template('404.html'),404 

@app.errorhandler(500) # 未知的app錯誤
def interna_server_error(error):
    return render_template('500.html'),500

if __name__=='__main__':
    app.run(debug=True,threaded=True)