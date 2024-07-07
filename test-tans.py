#!/usr/bin/python3

import mysql.connector
import datetime
import io,sys
import time
# 接続
con = mysql.connector.connect(
      database  ='test_db',
      user      ='root',
      password  ='0311'
)
print("------------------------  CONNECT --------------------")
# self.con.autocommit = True


print( "1", con.in_transaction )
cursor = con.cursor ( )

con.start_transaction()
print( "2", con.in_transaction )

sql = "select *  from userInf2 where id = 2 for update nowait"
print( "3", con.in_transaction )

cursor.execute (sql )
print( "4", con.in_transaction )

datas = cursor.fetchall()
for line in datas:
    print( line )

print( "a", con.in_transaction )
cursor.close()
print( "b", con.in_transaction )

cursor = con.cursor ( )
print( "c", con.in_transaction )


sql = "update userInf2 set tel='a' where id = 2"
cursor.execute( sql )

print( "5", con.in_transaction )

time.sleep(5);
# con.commit()
# con.rollback()
print( "6", con.in_transaction )

print("commit OK")
            

            
cursor.close()
print( "7", con.in_transaction )
con.close()
print( "8", con.in_transaction )
print("--------------------------インスタンス破棄OK(db close)")

