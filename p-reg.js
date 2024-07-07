

/*'''''''''''''''''''''''''''''''''''''''''''''
  関数名   一覧から細画面にリンクする
  引数
  返却値
  機能
  処理
'''''''''''''''''''''''''''''''''''''''''''''*/ 

  //画面の入力項目のを表示、非表示にする

  function dispItem( kind="" ){

      if( kind == "filter" )
        ar =["生年月日","お名前","メールアドレス","電話番号","郵便番号","町名・番地", "建物名（部屋番号）"];
      else if( kind == "search" )
        ar =["メールアドレス", "性別", "郵便番号","都道府県","市区町村", "町名・番地", "建物名（部屋番号）","趣味"];
      else
        ar =["お名前","生年月日","メールアドレス","性別", "電話番号","郵便番号","都道府県","市区町村", "町名・番地", "建物名（部屋番号）","趣味"];
      
      var allCls = document.querySelectorAll( '#formID *' );
      for (var i=0, len=allCls.length; i<len; i++) {
          if ( ar.includes( allCls[i].innerHTML )){
            allCls[i].style.display ="none";
            allCls[i+1].style.display = "none";
          }
          //console.log(i, allCls[i].tagName, allCls[i].innerHTML , allCls[i].name,  allCls[i].value);
      }
  }





/*'''''''''''''''''''''''''''''''''''''''''''''
  関数名

  引数
  返却値
  機能
  処理
'''''''''''''''''''''''''''''''''''''''''''''*/ 
function 登録の送信()
{
    let sendData ={

      "function":"reg",
      "info":   "",
      
      "data":{
        "name":       "",
        "birthday":   "",
        "sex":        "",
        "tel":        "",
        "email":      "",

        "postal_code":   "",
        "prefecture":   "",
        "city":         "",
        "address1":     "",
        "address2":     "",

        "hobby":        ""
      }
    }
      
    //入力域からデータを取得
    sData = getInputData( sendData );
    
    jsn = JSON.stringify( sData );
    ws.send( jsn );
}
      


//受信したメッセージの処理をする

//キャンセルボタンで、メニューに戻ります
  
function 登録の受信( rcvData ){

      let msg ="";
      if (rcvData["status"] == "OK"){
      
          dialogConfirm( "登録しました", "確認");

          登録処理();
          msg = "継続して登録できます";
      }
      else{
          //エラーメッセージ
          msg = rcvData["status"];
      }

      $("#message").html( msg );
}                




//画面の入力項目の内容を、オブジェクトに格納する

function getInputData( sendData ){

  $.each( sendData["data"], function( key,val ){

      var value = $('[name="' + key + '"]').val();

      if( key == "sex"){
        //ラジオボタンの値を取得
        value = $('[name=sex]:checked').val();
        value = (value==undefined)  ? "": value;
      }
      
      if( key == "hobby"){
        hobbys =[];
        value  ="";
        $(':checkbox[name="hobby"]:checked').each(function () {
          hobbys.push($(this).val());
          value += $(this).val() + " ";
        });
        
        value = value.trimEnd();
      }

      //console.log(key, value);
      sendData["data"][key]  =value;
  });
          
  return sendData;
}

