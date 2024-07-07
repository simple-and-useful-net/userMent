import tornado.ioloop
import tornado.web
import tornado.websocket
import json
import os

import m_userDb               # DBアクセスの為の自作モジュール

CONST_STATIC_PATH_WIN = "C:\\Users\\kobay\\test\\userMent3"
CONST_STATIC_PATH = os.getcwd()
CONST_INDEX_HTML  = "main.html"

'''
使用ファイル一覧

main.py       起動するファイル
main.html     メインの HTMLファイル
main.js       メインの JSファイル
main.css      メインの cssファイル

JavaScriptファイル
gmn-reg.js   （登録）       画面変更の為のHTML文（変数で格納されている）
gmn-list.js   (一覧表示)    画面変更の為のHTML文（変数で格納されている）

JavaScriptファイル
p-reg.js    登録用
p-list.js   一覧用
p-find.js   修正用

'''

# 現在アクセスしているクライアント
cl = []
workingID =[]

"""
    WebSoketによる通信処理 
"""    
class WebSocketHandler(tornado.websocket.WebSocketHandler):

    def open(self):
        self.db = m_userDb.dbCls();
        
        print("open OK")
        if self not in cl:
            cl.append(self)
 
    def on_message(self, message):

        # 全てのブラウザに使用しているIDを返却
        def sendWorkingID():

            smsg={}
            smsg["function"] = "workingID"
            smsg["data"] = workingID
            
            message =  json.dumps(smsg)
            for client in cl:
                client.write_message(message)
            return
        
        
        rcvData = json.loads( message )
        if rcvData["function"] == "sendWorkingID":
            sendWorkingID()
            return
            
            
        result = self.db.cmdBranch( message  )
        # breakpoint()
        if self.db.curID != None:
            if self.db.curID  not in workingID:
                workingID.append(self.db.curID )
                print("append ", self.db.curID )
                print("workingID", workingID )
                sendWorkingID()

        if self.db.editOK == True:
            if self.db.curID  in workingID:
                workingID.remove(self.db.curID )
                
                print("remove ", self.db.curID )
                print("workingID", workingID )
                self.db.curID = None

                sendWorkingID()

        if result != None:
          self.write_message( result )
        # else:
          # print("error ----", message)
        
        """
        全てのブラウザに送る（messageを送る）
        
        for client in cl:
            client.write_message(message)
        """
        
    def on_close(self):
        print("close OK")
    
        if self in cl:
            cl.remove(self)


# -----------------------------------------------
#   HTML表示
# -----------------------------------------------
'''
  ブラウザで「http://localhost:8888/」すると
  ファイル名（main.html）を
  renderする
'''
class MainHandler(tornado.web.RequestHandler):

    def get(self):
        self.render( CONST_INDEX_HTML )



# -----------------------------------------------
# main
# -----------------------------------------------
"""
debug=Trueにすると編集後に、再起動がかかるので便利
breakpoint()関数によりデバッガ起動されます
"""
application = tornado.web.Application(
  [
    (r"/static/(.*)", tornado.web.StaticFileHandler, {"path": CONST_STATIC_PATH}),
    (r"/",            MainHandler),
    (r"/websocket",   WebSocketHandler),
  ],
  debug=True
)



print("startします")
application.listen(8888)
# tornado.autoreload.start()
tornado.ioloop.IOLoop.current().start()
