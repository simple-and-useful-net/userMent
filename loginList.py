
import tornado.web
import tornado.websocket
import tornado.ioloop

'''
使用ファイル一覧

'''

"""
    WebSoketによる通信処理 
"""    
# 現在アクセスしているクライアントのインスタンス
cl = []

# クライアントのID名
loginMembers = []


class SocketHandler(tornado.websocket.WebSocketHandler):

    def open(self):
        print("open OK")
        
        self.ID = ""

        if self not in cl:
            cl.append(self)
        
        self.sendMembers()

 
    def on_message(self, message):
        print( "message",message)

        msgClass=message[:3]
        msg     =message[3:]
        print( "msgClass", msgClass)
        print( "msg", msg)
        
        if self.ID == "" and msg != "":
          loginMembers.append(msg)
          self.ID = msg
          self.sendMembers()
        
    def on_close(self):
        print("close OK")
    
        if self in cl:
            cl.remove(self)
            loginMembers.remove(self.ID)

        self.sendMembers()

    def sendMembers(self):
          memberStr = str(loginMembers)
          memberStr = memberStr.replace( ",", "<br>" )
          memberStr = memberStr.replace( "[", "<b>ログイン中のメンバ一覧</b><br>" )
          memberStr = memberStr.replace( "]", "" )
          memberStr = memberStr.replace( "'", "" )
          for client in cl:
              client.write_message( memberStr )
              # print(memberStr)


# -----------------------------------------------
#   HTML表示
# -----------------------------------------------
class HtmlHandler(tornado.web.RequestHandler):

    def get(self):

        # self.render( "loginList.html" )

        html = """
<html>
    <head>
        <meta http-equiv="content-type" content="text/html" charset="UTF-8">
    </head>

    <body>
        ID<input id="inp" value="">
        <button onclick="startLogin()">login</button>
        <div id="msg">ログインして下さい</div>
        
        
        <script>
          var sendFunc = function(){
              sendMsg = document.getElementById("inp").value;
              ws.send( sendMsg );
          }

          var startLogin = function(){
              var ID = document.getElementById("inp").value;
              ws.send( "ID:" + ID );
          }

          ws = new WebSocket("ws://localhost:8888/websocket");

          ws.onopen = function() {
              console.log("openしました");
          }

          ws.onclose = function() {
              console.log("closeしました");
          }

          ws.onmessage = function(ev) {
              console.log("onmessage", ev.data );
              document.getElementById("msg").innerHTML = ev.data;
          }


        </script>
    </body>
</html>
"""
        self.write( html )

  


# -----------------------------------------------
# main
# -----------------------------------------------
application = tornado.web.Application(
  [
    (r"/",            HtmlHandler),
    (r"/websocket",   SocketHandler),
  ],
  debug=True
)

print("startします")
application.listen(8888)
tornado.ioloop.IOLoop.current().start()
