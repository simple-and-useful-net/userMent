import tornado.web
import tornado.websocket
import tornado.ioloop
import pprint


'''

プロセスを検索してPIDを見つける

>tasklist |grep python
python.exe                   14044 Console                    1     25,876 K

プロセスの削除

>taskkill /F /PID 14044
成功: PID 14044 のプロセスは強制終了されました。

'''


"""
    WebSoketによる通信処理 
"""    
class SocketHandler(tornado.websocket.WebSocketHandler):

    def open(self):
        print("open OK")
        
    def on_message(self, message):
        print( "ブラウザからのメッセージ:",message)
        
        # ここでブラウザに送ります
        self.write_message( "おはよう御座います" )

    def on_close(self):
        print("close OK")


# 現在アクセスしているクライアント
clients = []


"""
    WebSoketによる通信処理 
"""    
class SocketHandler2(tornado.websocket.WebSocketHandler):

    def open(self):
        print("\nopen OK")

        pprint.pprint(clients)
        if self not in clients:
            clients.append(self)

        print("append後")
        pprint.pprint(clients)
 
    def on_message(self, message):
        print( "\nmsg OK",message)

        for no,cl in enumerate(clients):
            cl.write_message( "%dさん、%s" %( no+1, message ) )
            
    def on_close(self):
        print("\nclose OK")

        pprint.pprint(clients)
        if self in clients:
            clients.remove(self)

        print("remove後")
        pprint.pprint(clients)

    

# -----------------------------------------------
#   HTML表示
# -----------------------------------------------
'''
  ブラウザで「http://localhost:8888/」すると
  ファイル名（main.html）を
  renderする
'''
class HtmlIndexHandler(tornado.web.RequestHandler):

    def get(self):
        self.write("""
          hello!
          漢字です
        """)

class HtmlHandler(tornado.web.RequestHandler):

    def get(self):
        self.render( "basic.html" )
        '''
        self.write("""
          <html>
              <head>
                  <meta http-equiv="content-type" content="text/html" charset="UTF-8">
              </head>


              <body>
                  <h1>トルネードの基本</h1>

                  <script>
                    ws = new WebSocket("ws://localhost:8888/websocket");

                    ws.onopen = function() {
                        console.log("openしました");
                        ws.send("おはよう");
                    }

                    ws.onclose = function() {
                        console.log("closeしました");
                    }

                    ws.onmessage = function(ev) {
                        console.log("サーバからのメッセージ:", ev.data );
                    }
                  </script>
              </body>
          </html>
        """)
        '''


# -----------------------------------------------
# main
# -----------------------------------------------
"""
debug=Trueにすると編集後に、再起動がかかるので便利
breakpoint()関数によりデバッガ起動されます
"""

application = tornado.web.Application(
  [
    (r"/",              HtmlIndexHandler),
    (r"/test",            HtmlHandler),
    (r"/websocket",   SocketHandler),
    # (r"/websocket",   SocketHandler2),
  ],
  debug=True
  # debug=False
)


print("startします")
application.listen(8888)
tornado.ioloop.IOLoop.current().start()
