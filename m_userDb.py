#!/usr/bin/python3

import mysql.connector
import json
import datetime
import io,sys,os




# -------------------
# 日付型を文字列に変換
# -------------------
def chgDateFmt( obj ):
    if isinstance( obj, datetime.date):
        return obj.isoformat()







'''''''''''''''''''''''''''''''''''''''''''''
メッソ名

  引数
    
  返却値
    
  機能

  処理
      
  コメント

 
'''''''''''''''''''''''''''''''''''''''''''''


'''''''''''''''''''''''''''''''''''''''''''''
      JSON型に変換
'''''''''''''''''''''''''''''''''''''''''''''
def dumpProc( rec, prevPage, nextPage ):

    topID = 0
    lastID= 0

    recNum  = len(rec)
    if recNum != 0:
      topID = rec[0]["id"]
      lastID= rec[recNum-1]["id"]

    jData = json.dumps(rec, default=chgDateFmt)
      
    retJS ="""
    {
            "function": "list",
            "status":   "OK",
            "info":{
                    "recNum":   %d,
                    "topID":    "%s",
                    "lastID":   "%s",
                    "prevPage": %s,
                    "nextPage": %s
                    },
            "data":     %s
    }""" %( recNum, topID, lastID, prevPage, nextPage, jData)
    
    # print( "---" + retJS + "---", jData )
    return retJS



'''''''''''''''''''''''''''''''''''''''''''''

'''''''''''''''''''''''''''''''''''''''''''''


CONST_STATIC_PATH_WIN = "C:\\Users\\kobay\\test\\userMent3"
CONST_STATIC_PATH = os.getcwd()


# -------------------
#     DBアクセスのクラス
# -------------------
class dbCls:

    # コンストラクタ
    def __init__(self):

        print("CONST_STATIC_PATH", CONST_STATIC_PATH_WIN, CONST_STATIC_PATH)
        # 接続
        if CONST_STATIC_PATH_WIN == CONST_STATIC_PATH:
          print("windows 環境")
          # windows
          self.con = mysql.connector.connect(
              database  ='testdb',
              user      ='root',
              password  ='koba0311'
          )
        else:
          print("ubuntu 環境")
          self.con = mysql.connector.connect(
              database  ='testdb',
              user      ='koba',
              password  ='test01'
          )
        
        print("------------------------  CONNECT --------------------")
        self.con.autocommit = True
        self.curID = None
        self.editOK = False

    # デストラクタ
    def __del__(self):
        print("------------------------------------<br>インスタンス破棄OK(db close)<br>")
        self.con.close()
        
     
    # ログイン情報テーブルの作成
    def create(self):

        try:
            tableName = 'userInf'
            
            sql = '''
            CREATE TABLE userInf (
               id       INT AUTO_INCREMENT PRIMARY KEY,
               name     VARCHAR(100),
               email    VARCHAR(50),
               tel      VARCHAR(50),
               birthday DATE,
               sex      VARCHAR(2),
               
               postal_code  VARCHAR(10),
               prefecture   VARCHAR(50),
               city         VARCHAR(50),
               address1     VARCHAR(200),
               address2     VARCHAR(200),
               hobby        VARCHAR(50)
                ) auto_increment = 1001
               '''

            cursor = self.con.cursor ()
            cursor.execute( "drop table if exists userInf"  )

            cursor.execute( sql )
            self.con.commit()
            print( "テーブル作成OK")

        except mysql.connector.Error as e:
            self.con.rollback()
            print( "MySql error:", e.args)

        finally:
            cursor.close()


        
      
    '''''''''''''''''''''''''''''''''''''''''''''
    メッソ名
        ログイン情報テーブルにユーザIDとセッションIDを登録

      引数
        reg( self, uid, pwd ):
        uid   ユーザID
        pwd   パスワード

      返却値
        タプル ユーザID、セッションID
        
      機能
        ユーザIDとセッションIDを返却する関数
        クッキー情報がない場合は、空文字列が返る

      処理
        ・環境変数「HTTP_COOKIE」から全てのクッキー情報を取得
        ・http.cookiesモジュールのSimpleCookieのインスタンスの取得
        ・valueオブジェクトで以下のクッキーの値を取得
          ユーザID,セッションID
     
    '''''''''''''''''''''''''''''''''''''''''''''
    def reg( self, uid, pwd ):

        try:
          msg =""
          cursor = self.con.cursor ( prepared=True)
          self.con.start_transaction()

          # 「select ～　for update」を使って排他ロックする
          # 誰かが先に使われた場合は、待ち状態になる、
          # 待ち状態が続く場合はタイムアウトのエラーになります
          sql = "select *  from loginInf where uid =?  for update"
          cursor.execute (sql, (uid,))

          row = cursor.fetchone()
          if row == None:

            sql = "insert into loginInf ( uid, pwd, sid ) values (?, ?, '' )"
            cursor.execute(sql, (uid,pwd))

            self.con.commit()
            msg = "OK"

          else:
            self.con.rollback()
            msg = "NG"
            
        except mysql.connector.Error as e:
            self.con.rollback()
            msg = "MySql error:" + str( e.args )


        finally:
            cursor.close()
            return msg



    '''''''''''''''''''''''''''''''''''''''''''''
    メッソ名
        ユーザ情報をテーブルに新規登録する

      引数
        insertUser( self, jsData ):
        jsData  登録用のJSONデータ
        
      返却値
        タプル ユーザID、セッションID
        
      機能
        ユーザIDとセッションIDを返却する関数
        クッキー情報がない場合は、空文字列が返る

      処理
        ・環境変数「HTTP_COOKIE」から全てのクッキー情報を取得
        ・http.cookiesモジュールのSimpleCookieのインスタンスの取得
        ・valueオブジェクトで以下のクッキーの値を取得
          ユーザID,セッションID
     
    '''''''''''''''''''''''''''''''''''''''''''''
    def insertUser( self, jsData ):

        try:
          cursor = self.con.cursor ( prepared=True )

          if True:
            msg =""

            # データ部分を取り出す
            # copyメソッドを使うと元データを変更しない
            userData = jsData.copy()
            # for key, val in data.items():
            valString   = str( tuple( userData ) )
            valString   = valString.replace("'","")

            vals        = tuple( userData.values() )
            items       = ("?," * len(userData)).rstrip(",")

            sql = "insert into userInf %s values (%s)" %(valString, items)
            # print("sql=",         sql)
            # print("vals=",        vals)
            # print("valString=",   valString)
            # print("items=",       items)
            # print("sql=",         sql)

            cursor.execute( sql, vals )

            self.con.commit()
            msg = "OK"

          else:
            self.con.rollback()
            msg = "NG"
            
        except mysql.connector.Error as e:
            self.con.rollback()
            msg = "MySql error:" + str( e.args )


        finally:
            cursor.close()
            return msg





    '''''''''''''''''''''''''''''''''''''''''''''
    メッソ名
        検索条件にあう、ユーザ情報を取得する

      引数
        selectUser( self, jsData ):
        jsData  登録用のJSONデータ
        
      返却値
        検索したユーザの情報
        jsData  登録用のJSONデータ
        
      機能
        ユーザIDとセッションIDを返却する関数
        クッキー情報がない場合は、空文字列が返る

      処理
        ・環境変数「HTTP_COOKIE」から全てのクッキー情報を取得
        ・http.cookiesモジュールのSimpleCookieのインスタンスの取得
        ・valueオブジェクトで以下のクッキーの値を取得
          ユーザID,セッションID
          
      コメント
        JSONには、日付型が無いために、文字列型に変換する
        （isoformatを使うと文字列に変換ができます、逆に変換したい場合は、fromisoformatを使用します）
        
        あいまい検索は、パターンに「％」か「＿」を使って行う
        「％」は0文字以上の文字列とマッチして、「＿」は1文字の文字とマッチ（何でもＯＫ）します
        WHERE カラム名 LIKE パターン
        
        例として名前の名字が「山田」なら
        where name like '山田%'
        
        名字と名前の空白の数が曖昧な場合は、
        where name like '山田%太郎'

     
    '''''''''''''''''''''''''''''''''''''''''''''
    def selectUser( self, jsData ):

        try:

          if True:
            msg =""

            # データ部分を取り出す
            # copyメソッドを使うと元データを変更しない
            userData = jsData.copy()
            self.mkCond( userData )

            # print("111", jsData)
            # print("111", userData)
            # print("111", userData.values() )
            # for key, val in data.items():
            valString   = str( tuple( userData ) )
            valString   = valString.replace("'","")
            vals        = tuple( userData.values() )

            items       = ("?," * len(userData)).rstrip(",")
            
            self.con.start_transaction()
            # cursor = self.con.cursor ( prepared=True )
            cursor = self.con.cursor ( dictionary=True )


            info = self.con.get_server_info()
            print("---------- get_server_info", info)

            if info[0] == '5':
              sql = "select * from userInf where %s for update" %( self.cond )
            else:
              sql = "select * from userInf where %s for update nowait" %( self.cond )
            print("sql=",         sql)
            # print("vals=",         vals)

            cursor.execute( sql )
            res = cursor.fetchall()
            print(res)

            if ( len(res)==1 ):
              jData = json.dumps(res, default=chgDateFmt)

              cursor.close()
              return "OK",jData
            
            if ( len(res)==0 ):

              cursor.close()
              self.con.rollback()
              return "NG",0
            

            else:
              cursor.close()
              self.con.rollback()
              return "NG", str(len(res))
            
        except mysql.connector.Error as e:
            msg = "MySql error:" + str( e.args )
            print("error", e.args)
            cursor.close()
            self.con.rollback()

            if e.errno == 3572 or e.errno == 1205:
                print("error rock")
                return "ERR",'"指定ユーザは他で編集されています"'

            return "ERR",'"%s"' %msg
            



    '''''''''''''''''''''''''''''''''''''''''''''

    '''''''''''''''''''''''''''''''''''''''''''''
    def selectIdUser( self, id ):

        try:

          if True:
            msg =""

            self.con.start_transaction()
            cursor = self.con.cursor ( dictionary=True )
            # info = self.con.get_client_version()
            info = self.con.get_server_info()
            print("---------- get_server_info", info)
            """
            MySQLのバージョンがV5の場合は、nowaitがないので、使えません
            /etc/mysql/my.cnfでタイムアウト時間を1秒に設定して対応
            [mysqld]
            innodb_lock_wait_timeout = 1

MySQLモニタで確認する、通常は50秒
            
mysql> show global variables like 'innodb_lock_wait_timeout';
+--------------------------+-------+
| Variable_name            | Value |
+--------------------------+-------+
| innodb_lock_wait_timeout | 50    |
+--------------------------+-------+
1 row in set, 1 warning (0.00 sec)

            """

            if info[0] == '5':
              sql = "select *  from userInf where id = %s for update"
            else:
              sql = "select *  from userInf where id = %s for update nowait"
            # print("sql=",         sql)

            # cursor = self.con.cursor ( prepared=True )
            cursor.execute (sql, (id,) )
            res = cursor.fetchall()
            # print(res)
            
            if ( len(res)==1 ):
              jData = json.dumps(res, default=chgDateFmt)

              cursor.close()
              self.curID = id
              return "OK",jData

            else:
              cursor.close()
              self.con.rollback()
              
              return "NG", str(len(res))
            
            
        except mysql.connector.Error as e:
            msg = "MySql error:" + str( e.args )
            print("error", e.args)
            cursor.close()
            self.con.rollback()

            if e.errno == 3572 or e.errno == 1205:
                print("error rock")
                return "ERR",'"指定ユーザは他で編集されています"'

            return "ERR",'"%s"' %msg



    '''''''''''''''''''''''''''''''''''''''''''''

    '''''''''''''''''''''''''''''''''''''''''''''
    def updateUser( self, jsData ):

        try:

          if True:
            msg =""

            # データ部分を取り出す
            # copyメソッドを使うと元データを変更しない
            userData = jsData.copy()
            # print("111", jsData)
            # print("111", userData)
            # print("111", userData.values() )
            # for key, val in data.items():

            listData = list( tuple(userData) )
            listData.pop(0)
            # print("listString", listData)
            valString   = str( tuple( listData ) )
            valString   = valString.replace("('","set ")
            valString   = valString.replace("')","=%s ")
            valString   = valString.replace("',","=%s,")
            valString   = valString.replace("'","")
            # print("valstring2=",valString)


            ldata       = list( userData.values() )
            idno        = ldata.pop(0)
            ldata.append( idno )
            vals        = tuple( ldata )

            sql = "update userInf " + valString + "where id =%s"
            print("sql=",         sql)
            print("vals=",         vals)
            # cursor = self.con.cursor ( prepared=True )
            cursor = self.con.cursor ( dictionary=True )
            cursor.execute( sql, vals )

            self.con.commit()
            self.editOK = True
            # self.con.rollback()
            cursor.close()

            return "OK","true"

        except mysql.connector.Error as e:
            msg = "MySql error:" + str( e.args )
            self.con.rollback()

            cursor.close()
            return "ERR",msg





    '''''''''''''''''''''''''''''''''''''''''''''
    メッソ名
        検索条件にあう、ユーザ情報を取得する

      引数
    def listTop( self ):
    def listLast( self ):
    
    def listNext( self, lastID ):
    def listPrev( self, topID ):
    
        jsData  登録用のJSONデータ
        
      返却値
        検索したユーザの情報
        jsData  登録用のJSONデータ
        
      機能
        ユーザIDとセッションIDを返却する関数
        クッキー情報がない場合は、空文字列が返る

      処理
        ・環境変数「HTTP_COOKIE」から全てのクッキー情報を取得
        ・http.cookiesモジュールのSimpleCookieのインスタンスの取得
        ・valueオブジェクトで以下のクッキーの値を取得
          ユーザID,セッションID
          
      コメント

     
    '''''''''''''''''''''''''''''''''''''''''''''

    
    def listTop( self ):

        # 日付型を文字列に変換
        try:
          if True:
            msg =""
            # cursor = self.con.cursor ( prepared=True )
            cursor = self.con.cursor ( dictionary=True )

            cursor.execute("select * from userInf where %s order by id limit 11" %self.cond )

            res = cursor.fetchall()            
            cursor.close()
            return "OK", res
            
        except mysql.connector.Error as e:
            msg = "MySql error:" + str( e.args )

            cursor.close()
            return "ERR",msg


    def listLast( self ):

        try:
          if True:
            msg =""
            # cursor = self.con.cursor ( prepared=True )
            # self.con.commit()
            # self.con.rollback()
            # self.con.cmd_reset_connection()

            cursor = self.con.cursor ( dictionary=True )
            cursor.execute("select * from userInf where %s order by id desc limit 11" %self.cond )
            res = cursor.fetchall()

            # print("--------------- 1 >>> ",res)
            res.reverse()
            # print("--------------- 2 >>> ",res)
            cursor.close()
            return "OK", res
            
            
        except mysql.connector.Error as e:
            msg = "MySql error:" + str( e.args )

            cursor.close()
            return "ERR",msg
            
            
            
    def listNext( self, lastID, reloadPage=False ):

        try:
          if True:
            msg =""
            # cursor = self.con.cursor ( prepared=True )
            cursor = self.con.cursor ( dictionary=True )

            # print("dbg1",reloadPage)
            if reloadPage == False:
              cursor.execute("select * from userInf where %s id >  %s order by id  limit 11" %(self.cond + " and ", lastID) )
            else:
              cursor.execute("select * from userInf where %s id >= %s order by id  limit 11" %(self.cond + " and ", lastID) )
            # cursor.execute("SELECT * FROM userInf where id > 127 order by id  limit 11" )
            # print("dbg2")
            res = cursor.fetchall()
            cursor.close()
            return "OK", res
            
        except mysql.connector.Error as e:
            msg = "MySql error:" + str( e.args )

            cursor.close()
            return "ERR",msg


    def listPrev( self, topID ):

        try:
          if True:
            msg =""
            # cursor = self.con.cursor ( prepared=True )
            cursor = self.con.cursor ( dictionary=True )

            sql = "select * from userInf where %s id < %s order by id desc limit 11"  %( self.cond + " and ", topID )
            # cursor.execute("select * from userInf where %s id < %s order by id desc limit 11" %(self.cond + " and ", topID) )
            cursor.execute( sql )
            res = cursor.fetchall()
            res.reverse()
            
            cursor.close()
            return "OK", res
            
        except mysql.connector.Error as e:
            msg = "MySql error:" + str( e.args )

            cursor.close()
            return "ERR",msg

            

    # ----------------------------------
    # whereの条件を作成する
    # ----------------------------------
    def mkCond( self, dicData ):

      # self.cond = " 1 and 1 "
      # return
      # """
      cond = ""
      for key in dicData:
      
        val= dicData[key]
        
        if val != "":
          if cond != "":
            cond += " and "
          
          if key == "hobby":
              valArr = val.split(" ")
              
              con = ""
              for data in valArr:
                if con == "":
                  con += " (hobby like '%%%s%%') " %( data )
                else:
                  con += " or (hobby like '%%%s%%') " %( data )
                
              if len(valArr) > 1:
                  con = " ( " + con + " ) "
              
              cond += con
          else:
              cond += " %s = '%s' " %( key, val )
      
      if cond == "":
        cond = " 1 and 1 "
      self.cond = cond 
      print("--- cond ---(", cond, ")---")





    '''''''''''''''''''''''''''''''''''''''''''''

    '''''''''''''''''''''''''''''''''''''''''''''
    def cmdBranch( self, jsData ):

        # self.curID = None
        self.editOK = False

        '''''''''''''''''''''''''''''''''''''''''''''
            最初、最後のページへ
        '''''''''''''''''''''''''''''''''''''''''''''
        def topProc():

          st,rec = self.listTop()
          
          if st != "OK":
              return None
              
          prevPage= "false"
          nextPage= "false"

          recNum  = len(rec)
          if recNum > 0:
            if recNum >10: 
              nextPage = "true"
              recNum    = 10
              del rec[-1]
              
          return dumpProc( rec, prevPage, nextPage )
              
            
        def lastProc():

          st,rec= self.listLast( )
          if st != "OK":
              return None
          
          recNum  = len(rec)
          prevPage= "false"
          nextPage= "false"

          if recNum > 0:
            if recNum >10: 
              prevPage = "true"
              recNum    = 10
              del rec[0]
              
          return dumpProc( rec, prevPage, nextPage )




        '''''''''''''''''''''''''''''''''''''''''''''
            前ページ、次ページ
        '''''''''''''''''''''''''''''''''''''''''''''
        def nextProc( lastID ):

            st,rec= self.listNext( lastID )
            if st != "OK":
              return None

            recNum  = len(rec)
            if recNum < 10:
                return( lastProc() )

            prevPage= "true"
            nextPage= "false"

            if recNum > 0:
              if recNum >10: 
                nextPage = "true"
                recNum    = 10
                del rec[-1]

            return dumpProc( rec, prevPage, nextPage )


        '''''''''''''''''''''''''''''''''''''''''''''

        '''''''''''''''''''''''''''''''''''''''''''''
        def prevProc( topID ):

            st,rec= self.listPrev( topID )
            if st != "OK":
              return None

            recNum  = len(rec)
            if recNum < 10:
              return( topProc() )

            prevPage= "false"
            nextPage= "true"

            if recNum > 0:
              if recNum >10: 
                prevPage = "true"
                recNum    = 10
                del rec[0]

            return  dumpProc( rec, prevPage, nextPage )


        '''''''''''''''''''''''''''''''''''''''''''''
            リロード
        '''''''''''''''''''''''''''''''''''''''''''''
        def reloadProc( topID ):
            
            st,rec= self.listNext( topID, reloadPage =True  )
            if st != "OK":
              return None
            
            recNum  = len(rec)
            if recNum > 0:
              if recNum >10: 
                del rec[-1]

            # Pythonの論理型をJSONの為に、一時文字列に変換
            '''
            prevPage = "false"
            nextPage = "false"

            if prevPage:
              prevPage = "true"
              
            if nextPage:
              nextPage = "true"
            '''
            prevPage = "true" if prevPage else "false"
            nextPage = "true" if nextPage else "false"

            return dumpProc( rec, prevPage, nextPage )




        try:
            # breakpoint()
            # loadsを使ってPythonデータ型にする
            # print("**"+ jsData +"**")
            rvData    = json.loads( jsData )
            dataBody  = rvData["data"].copy()

            # HTMLファイルをリードしてブラウザへ送る
            if rvData["function"] =="html":
              fname = rvData["data"]

              # with open( "/var/www/html/books/userMent2/findBD.html" ) as f:
              # windows
              with open( "/users/kobay/test/userMent2/findBD.html", encoding="utf-8" ) as f:
                htmlData = f.read()

              id = data["id"]
              htmlData = htmlData.replace( "\n","\\n" ).replace( "\"", "'" )
              retJS ="""{
                      "function":   "html",
                      "status":     "OK",
                      "id":         "%s",
                      "data":       "%s"
                      }
              """ %( id, htmlData )
              
              # print( "htmlData ---" + retJS + "---" )
              return retJS


            '''''''''''''''''''''''''''''''''''''''''''''
              rollback
            '''''''''''''''''''''''''''''''''''''''''''''
            if rvData["function"] =="rollback":
            
                self.editOK = True
                self.con.rollback()
                return None


            '''''''''''''''''''''''''''''''''''''''''''''
              セレクトIDによる検索
            '''''''''''''''''''''''''''''''''''''''''''''
            if rvData["function"] =="selId":
              id    = rvData["id"]

              st, rec = self.selectIdUser( id )

              retJS ="""{
                      "function":   "find",
                      "status":   "%s",
                      "data":     %s
                    }""" %( st, rec )
              
              # print( "find ---" + retJS + "---" )
              return retJS


            '''''''''''''''''''''''''''''''''''''''''''''
            # 検索
            '''''''''''''''''''''''''''''''''''''''''''''
            if rvData["function"] =="find":

              st, rec = self.selectUser( dataBody )
              # print(st, rec )

              retJS ="""{
                      "function":   "find",
                      "status":     "%s",
                      "data":       %s
                    }""" %( st, rec )
              
              # print( "find ---" + retJS + "---" )
              return retJS


            
            '''''''''''''''''''''''''''''''''''''''''''''
                  登録
            '''''''''''''''''''''''''''''''''''''''''''''
            if rvData["function"] =="reg":

              st = self.insertUser( dataBody )

              if st == "OK":
                print("登録OK")
              elif st == "NG":
                print("登録済み")
              else:
                print("reg() error"+ st)

              retJS ="""{
                      "function":   "reg",
                      "status":     "%s",
                      "data":       true
                      }
              """ %( st.replace("\"","") )
              
              # print( "---" + retJS + "---" )
              return retJS



            '''''''''''''''''''''''''''''''''''''''''''''
            # データ更新
            '''''''''''''''''''''''''''''''''''''''''''''
            if rvData["function"] =="update":

              st, rec = self.updateUser( dataBody )
              # print(st, rec )

              retJS ="""{
                      "function":   "update",
                      "status":   "%s",
                      "data":     %s
                    }""" %( st, rec )
              
              # print( "update ---" + retJS + "---" )
              return retJS



            # whereの条件を作成する
            if rvData["function"] in ["top","last","next","prev"]:
                self.mkCond( dataBody )
                topID   = rvData["info"]["topID"]
                lastID  = rvData["info"]["lastID"]            
                prevPage= rvData["info"]["prevPage"]
                nextPage= rvData["info"]["nextPage"]

           
            '''-------------------------------------------
                最初、最後のページ
            --------------------------------------------'''
            if rvData["function"] =="top":
              return( topProc() )

            # 一覧表示
            if rvData["function"] =="last":
              # breakpoint()
              return( lastProc() )

            # 一覧表示
            if rvData["function"] =="reload":
              return( reloadProc( topID ) )
              
            
            # 一覧表示
            '''-------------------------------------------
              Next Page
            --------------------------------------------'''
            if rvData["function"] =="next":

              if nextPage == False:
                return None
              else:
                return( nextProc( lastID ))
              

            # 一覧表示
            '''-------------------------------------------
                  Prev Page
            --------------------------------------------'''
            if rvData["function"] =="prev":

              if prevPage == False:
                return None
              else:
                return prevProc( topID )
              
              
              
        except mysql.connector.Error as e:
            msg = "MySql error:" + str( e.args )

            return "ERR",msg







# -------------------------------
#         main
#　(コマンドラインから)
# 単体でテストする場合
# -------------------------------
def main():

  jdata ="""{                                                         
      "function":   "reg",
      "info":   {
        "topID":  "",
        "lastID": "",
        "nextPage": "",
        "prevPage": "",
      },
      "data":       {                                                  
                    "name":         "koba",                         
                    "birthday":     "2022-03-12",                   
                    "tel":          "090-8877-1011",                
                    "email":        "a@bbb",                        
                    "postal_code":  "123-1234",                     
                    "city":         "千葉県",
                    "address1":     "市川市緑区",
                    "address2":     "マンション２０１",
                    "sex":          "女性",
                    "prefecture":   "青森県",
                    "hobby":        "アウトドア 映画"
                    }
  }
  """


  svInfo  ="{}"
  svNo    ="top"

  db =dbCls()

  while(True):
    print()
    print( "end 終わり" )
    print( "c テーブル作成" )
    print( "t many data" )
    print( "i 登録" )
    print( "s select" )

    print( "top last next prev" )
    print()

    no = input("No ")
    # no = int(no)
    if no == "":
      no = svNo
    else:
      svNo =no    
    
    if no=="end":
      sys.exit()

    if no=="c":
      db.create()

    # uid = input("ユーザID")
    # pwd = input("password")
    # sid = input("セッションID")

    # 登録テスト
    if no=="i":
        
      st = db.cmdBranch( jdata )

      if st == "OK":
        print("登録OK")
      elif st == "NG":
        print("登録済み")
      else:
        print("reg() error"+ str(st))

    # 検索
    if no=="s":
      
      jsSelect ="""{                                                         
          "function":   "sel",                                              
          "data":       {                                                  
                        "name":         "%山田%"
                        }
      }
      """

      name = input("name")
      data = json.loads(jsSelect)
      data["data"]["name"]  = "%" + name + "%"

      st = db.cmdBranch( json.dumps(data)  )
        

    jdata ="""
        {                                                         
          "function":   "%s",                                        
          "info":       %s,
          "data":       
              {                                                  
                  "name":         "",                         
                  "birthday":     "",                   
                  "tel":          "",                
                  "email":        "",                        
                  "postal_code":  "",                     
                  "address1":     "",
                  "address2":     "",
                  "sex":          "",
                  "prefecture":   "",
                  "hobby":        ""
              }
        }
        """ %( no, svInfo )

    st =None
    # list
    if no=="top":
      
          
      st = db.cmdBranch( jdata  )
 
     # list
    if no=="last":
      

      st = db.cmdBranch( jdata  )

    # list
    if no=="next":
      
      st = db.cmdBranch( jdata  )
        

    # list
    if no=="prev":
      
      st = db.cmdBranch( jdata  )


    if st !=None:
      data  = json.loads(st)
      svInfoJS= data["info"].copy()
      svInfo  = json.dumps(svInfoJS)

      print("start")
      print(data["status"])
      print(data["info"])
      print("end")
    else:
      print("OVER----------------------------------")


    if no== "t":
        import random


        jsData = json.loads(jdata)

        for i in range(1,11):
          jsData["data"]["name"]        = "山田 %d郎"          %i
          jsData["data"]["email"]       = "guest%02d@ya.com"   %i     
          jsData["data"]["tel"]         = "070-0000-%04d"      %i

          sexs        = ["男性", "女性"]
          n = random.randint(0,1)
          jsData["data"]["sex"]         = sexs[n]
          
          jsData["data"]["birthday"]    = "2022-09-%02d"       %i
          
          jsData["data"]["postal_code"] = "123-%04d"          %i
          jsData["data"]["city"]        = '三鷹市'
          jsData["data"]["address1"]    = '関町１－３３－５'
          jsData["data"]["address2"]    = '山田荘 %03d'        %i
          
          prefectures = ["北海道",
"青森県",
"岩手県",
"宮城県",
"秋田県",
"山形県",
"福島県",
"茨城県",
"栃木県",
"群馬県",
"埼玉県",
"千葉県",
"東京都",
"神奈川県",
"新潟県",
"富山県",
"石川県",
"福井県",
"山梨県",
"長野県",
"岐阜県",
"静岡県",
"愛知県",
"三重県",
"滋賀県",
"京都府",
"大阪府",
"兵庫県",
"奈良県",
"和歌山県",
"鳥取県",
"島根県",
"岡山県",
"広島県",
"山口県",
"徳島県",
"香川県",
"愛媛県",
"高知県",
"福岡県",
"佐賀県",
"長崎県",
"熊本県",
"大分県",
"宮崎県",
"鹿児島県",
"沖縄"]
          n = random.randint(0, 46)
          jsData["data"]["prefecture"]    = prefectures[n]

          n = random.randint(0, 4)
          hobby       = ['音楽','映画']
          if n==0:
              jsData["data"]["hobby"] = "音楽 映画"
          if n==1:
              jsData["data"]["hobby"] = "音楽 アウトドア"
          if n==2:
              jsData["data"]["hobby"] = "映画"
          if n==3:
              jsData["data"]["hobby"] = "アウトドア 音楽"
          if n==4:
              jsData["data"]["hobby"] = "音楽 映画 アウトドア"

          # jsData2 = json.dumps(jsData["data"])
          db.insertUser( jsData["data"] )


if __name__ == "__main__":
    
    main()



