#!/usr/bin/python3

import mysql.connector
import json
import datetime
import io,sys


# -------------------
# -------------------
class dbCls:

    # コンストラクタ
    def __init__(self):

        # 接続
        self.con = mysql.connector.connect(
            database  ='test_db',
            user      ='root',
            password  ='0311'
        )
        print("------------------------  CONNECT --------------------")
        # self.con.autocommit = True

    # デストラクタ
    def __del__(self):
        print("--------------------------インスタンス破棄OK(db close)")
        self.con.close()
        
     
    # ログイン情報テーブルの作成
    def create(self):

        try:
            sql = '''
            CREATE TABLE userInf2 (
               id       INT AUTO_INCREMENT PRIMARY KEY,
               name     VARCHAR(100),
               tel      VARCHAR(50)
                )
               '''

            cursor = self.con.cursor ()

            cursor.execute( "drop table if exists userInf2"  )
            cursor.execute( sql )
            self.con.commit()
            print( "テーブル作成OK")

        except mysql.connector.Error as e:
            self.con.rollback()
            print( "MySql error:", e.args)

        finally:
            cursor.close()




    def selectUser( self):

        try:
            # sql = "select *  from userInf2 where id = %s"
            # print("sql=",         sql)

            # cursor = self.con.cursor ( prepared=True )
            cursor = self.con.cursor ( )
            self.con.rollback()


            # cursor.execute (sql, (id,) )
            sql = "select *  from userInf2 where id = 1"
            sql = "select *  from userInf2"
            cursor.execute (sql )
            datas = cursor.fetchall()
            for line in datas:
                print( line )

        finally:
            cursor.close()

    def updateUser( self ):

        try:

          if True:
            msg =""

            cursor = self.con.cursor ()
            # sql = "update userInf2 set tel="1" + " where id =%s"
            # cursor.execute( sql, vals )

            sql = "update userInf2 set tel='abc12345' where id = 1"
            cursor.execute( sql )

            # self.con.commit()
            self.con.rollback()
            print("commit OK")
            return "OK","true"
        finally:
            cursor.close()

    def insertUser( self ):

        try:

          if True:
            msg =""

            cursor = self.con.cursor ()
            sql = 'insert into userInf2(name,tel) values("koba","110")'
            cursor.execute( sql )

            self.con.commit()

            return "OK","true"
        finally:
            cursor.close()



if __name__ == "__main__":

  db =dbCls()

  while(True):
    print()
    print( "end 終わり" )
    print( "c テーブル作成" )

    print( "i 登録" )
    print( "s select" )


    no = input("No ")
    # no = int(no)

    if no=="end":
      sys.exit()
    if no=="c":
      db.create()

    if no == "s":
      db.selectUser()

    if no == "i":
      db.insertUser()

    if no == "u":
      db.updateUser()
    


