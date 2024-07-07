import tornado.web
import tornado.websocket
import tornado.ioloop
import pprint




"""
    WebSoketによる通信処理 
"""    
# -----------------------------------------------
#   HTML表示
# -----------------------------------------------
'''
  ブラウザで「http://localhost:8888/」すると
  ファイル名（main.html）を
  renderする
'''
class mainPage(tornado.web.RequestHandler):

    def get(self):
        self.write("""
<html>    
    <head>
        <meta http-equiv="content-type" content="text/html" charset="UTF-8">
    </head>


    <body>
          <h1>顧客管理</h1>
          
          <a href="/reg?title=とうろく">登録</a>
          <a href="/list">一覧</a>
    </body>
</html>    
        """)

class regPage(tornado.web.RequestHandler):

    def get(self):
        title = self.get_argument('title', '指定なし')    
        self.render( "regPage.html", TTL = title  )

class listPage(tornado.web.RequestHandler):

    def get(self):
      name = self.get_argument('title', 'World')        
      self.render( "listPage.html" )


# -----------------------------------------------
# main
# -----------------------------------------------
"""
debug=Trueにすると編集後に、再起動がかかるので便利
breakpoint()関数によりデバッガ起動されます
"""

application = tornado.web.Application(
  [
    (r"/",              mainPage  ),
    (r"/reg",           regPage  ),
    (r"/list",          listPage  ),
  ],
  debug=True
  # debug=False
)


print("startします")
application.listen(8888)
tornado.ioloop.IOLoop.current().start()
