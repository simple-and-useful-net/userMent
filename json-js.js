// オブジェクトの配列を準備
data = [ 123, "東京\n大阪", true, null, [1,2], {"name":"山田"} ];
console.log(data);
console.log( typeof( data ) );

// ジェイソン形式にする
jsData = JSON.stringify( data );
console.log( jsData );
console.log( typeof( jsData ) );

// JavaScriptのデータ型にする
javaStData = JSON.parse( jsData );
console.log( javaStData );
console.log( typeof( javaStData ) );

for( key in javaStData){
  val = javaStData[key];
  console.log( key, val, typeof(val));
}
