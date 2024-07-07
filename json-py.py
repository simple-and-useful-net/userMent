
import json

dicData = {"name":"kobayashi\ntakeshi", "age":12, "status":True, "data":None }

# ジェイソン形式にする
jsnData = json.dumps( dicData )
print( type( jsnData ))
print( jsnData )


# Pythonデータ型にする
pyData = json.loads( jsnData )
print( type( pyData ))
print( pyData )

for dt in  pyData:
  print(dt, pyData[dt], type(pyData[dt]))
