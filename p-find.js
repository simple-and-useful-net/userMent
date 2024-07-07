

    
/**********************************************
  関数名
  引数
  返却値
  機能
  処理
***********************************************/
function 検索の送信(){

    curBtn = "searchStart";

    let sendData ={
      "function":"find",
      
      "data":{
        "name":       "",
        "birthday":   "",
        "tel":        ""
      }
    }

    getInputData( sendData );
    jsn = JSON.stringify( sendData );
    //console.log("json data:", jsn)
    ws.send( jsn );
}


//修正画面を表示      

function 検索結果の受信( rcvData ){

    var msg ="";
    
    //$(".menu").hide();
    if( rcvData["status"] == "NG" ){

        if( rcvData["data"] == 0){
          msg = "取得データがありません";
        }
        else{
          msg = "データが複数あります";
        }

        $("#message").html( msg );
        return;
    }
    //他のブラウザでの作業不可のMSG
    else if( rcvData["status"] == "ERR" ){
        msg = rcvData["data"]
        dialogConfirm( msg, "確認");

        $("#message").html( msg );
        return;
    }
    
    
    
    $("#chgContent").html( regHtml );
    dispRcvData( rcvData["data"][0] );
    
    //登録、変更中にフォーカス移動があった場合のフラグ
    editing = true;        
    $("#message").html( "取得しました" );

    $(".menu").prop("disabled", true);      
    $(".menuBTN").hide();
    $("#更新BtnID").show();
    $("#キャンセルBtnID").show();
}
  

/**********************************************
  関数名
  引数
  返却値
  機能
  処理
    ユーザ更新(更新ボタンが押されたら)

***********************************************/
function 更新の送信(){

    let updateData ={
      "function":"update",
      
      "data":{
        "id":         "123",
        "name":       "小林　太郎",
        "birthday":   "2022-01-02",
        "sex":        "女性",
        "tel":        "080-8873-1011",
        "email":      "koba@yahoo.com",
  
        "postal_code":   "123-1234",
        "prefecture":   "東京都",
        "city":         "千葉県",
        "address1":     "新田",
        "address2":     "３－１９－２",

        "hobby":        "音楽 映画"
      }
    }

    getInputData( updateData );
    jsn = JSON.stringify( updateData );
    ws.send( jsn  );
}


  
    
function 更新の受信( rcvData ){

      let msg ="";
      
      //フォーカスがアウトをウィンドウ用
      editing = false;      

      if( rcvData["status"] == "OK" ){

        $(".menu").prop("disabled", false); //ヘッドメニュー表示
              
        if( curBtn == "list")
          一覧処理();
        if( curBtn == "searchStart")
          検索処理();
        
        msg = "更新しました";
        dialogConfirm( msg, "確認");
      }
      else{
        msg = "エラーが発生しました";
      }
  
      $("#message").html( msg );
      return;
}




  //受信データを表示します（入力域に設定）
  //オブジェクトのプロパティ名でループ

    //ラジオボタンとチェックボックスは、配列を指定する
    //$('input:radio[name="sex"]').val( ["MAN"] );
    //$('[name="hobby"]').val([ "Game", "music"])
    // チェックボックスは内部では文字列で格納（項目は空白で区切られる）
    // 例）hobbyString = "TV music";

  
  function dispRcvData( rData ){

      for( key in rData ) {

        value = rData[ key ];

        if( key =="sex" ){
          $('input:radio[name="sex"]').val( [value] );
        }
        else if( key =="hobby" ){
          hobbyString = value
          hobbyAry    = hobbyString.split(' ');
          $('[name="hobby"]').val( hobbyAry )
        }
        else{
            //通常の入力域
            $('[name="' + key + '"]').val( value );
        }
      }
  }
  

