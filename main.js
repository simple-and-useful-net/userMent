  //初回は接続します
  openBtn();

  //ダイアログボックス

  function dialogConfirm(msg, title) {

    return new Promise(function(resolve, reject) {

      $('#dialog').html(msg).dialog({
        //autoOpen: false,
        modal: true,
        title: title,
        buttons: {
          'OK': function() {
            $(this).dialog("close");
            //resolve();
            resolve();
          }
          //'No': function() {
            //reject();
          //}
        }
      });
    });
  }          



  nn =0;
  //var editing = true;
  var editing = false;
  
  var ChkProcMsg = {

      Vars:{
          OriginalTitle: "顧客管理",
          Interval: null,
          Proc:false
      },    
      On: function(){
              noti = " 編集中!";
              _this = this;
              if ( _this.Vars.Proc == true ){
                return;
              }
              
              
              _this.Vars.Proc = true; 
              _this.Vars.Interval = setInterval(function(){

                nn ++;
                document.title = ( _this.Vars.OriginalTitle == document.title)
                                     ? String(nn) + noti
                                     : _this.Vars.OriginalTitle;
              }, 1000);
      },
      Off: function(){
          clearInterval(this.Vars.Interval);
          document.title = this.Vars.OriginalTitle;   
          this.Vars.Proc = false;   
          nn =0;
      }
  }

    var tmID = 0;
    window.addEventListener('focus', () => {
      
      console.log('active');
      ChkProcMsg.Off();
      //$("#message").html( "編集を完了させて下さい!" );
      clearInterval(tmID);
    });


    window.addEventListener('blur', () => { 
      
      console.log('inactive');
      
      //if (false){
      if ( editing ){

        ChkProcMsg.On();
        
        $("#message").html( "編集を完了させて下さい!" );
        tmID = setInterval(function(){
            $('#message').fadeOut(500,function(){$(this).fadeIn(500)});
        },1000);

        //ダイアログ表示の場合は、コメント解除
        /*
        dialogConfirm("ボタンをクリックして、\n編集を完了させて下さい", '編集中！').then(function() {
            console.log("okokoko");
            $("#dialog").dialog("close");
        }).catch(function() {
            //alert();
        });
        */          
      }
    });


    
    

/**********************************************
  関数名
  引数
  返却値
  機能
  処理
***********************************************/
    curBtn ="";
    
    function 登録処理(){

      curBtn ="reg";
      editing = true;
      
      document.getElementById("menuReg").style.backgroundColor = "lightgray"
      document.getElementById("menuList").style.backgroundColor = null;
      document.getElementById("menuSearch").style.backgroundColor = null;

      $("#message").html( "" );
      $("#chgContent").html( regHtml );

      $(".menu").prop("disabled", true);      
      $(".menuBTN").hide();
      $("#登録BtnID").show();
      $("#キャンセルBtnID").show();
    }

    function 一覧処理(){

      curBtn ="list";
      document.getElementById("menuReg").style.backgroundColor = null;
      document.getElementById("menuList").style.backgroundColor = "lightgray"
      document.getElementById("menuSearch").style.backgroundColor = null;
      
      $("#message").html( "" );
      $("#chgContent").html( regHtml + listHtml );

      $("dl br").hide();
      $("dl dt").hide();
      $("dl dd").hide();

      $(".フィルタCLS").show();
      //性別の対応（指定なし）を表示
      $("#フィルタID").show();

      $(".menuBTN").hide();
      $("#フィルタBtnID").show();

      mkTbl( 12+1,11 );
      lastBtn();
      simpleSendMsg( "sendWorkingID" );
    }
    
    function 検索処理(){
      
      curBtn ="search";
      document.getElementById("menuReg").style.backgroundColor = null;
      document.getElementById("menuList").style.backgroundColor = null;
      document.getElementById("menuSearch").style.backgroundColor = "lightgray";

      $("#message").html( "" );
      $("#chgContent").html( regHtml );
      dispItem("search");

      $(".menuBTN").hide();
      $("#検索開始BtnID").show();
    }

    function キャンセル処理(){
      
      simpleSendMsg( "rollback" );
      editing = false;      

      $(".menu").prop("disabled", false);      
      $("#message").html( "" );

      if( curBtn == "reg" ){
        $("#chgContent").html( "" );
      }
      if( curBtn == "list" ){
          一覧処理();
      }
      if( curBtn == "searchStart"){
          検索処理();
      }
    }



    
    
/**********************************************
  関数名
  引数
  返却値
  機能
  処理
***********************************************/
var workingIdTbl = null;
    
function 作業中ID表示( rcvData ){

  var userList = document.getElementById("tbl");
  //テーブルの中身が作成されているか？
  if ( userList === null){
    console.log("userList is null");
    return;
  }
  
  //テーブル一行の着色
  for( let ix=0; ix<11; ix=ix+1){

      idData = userList.rows[ ix ].cells[ 12 ].innerHTML;
      idData = Number( idData );

      if ( workingIdTbl !== null ){
        if ( workingIdTbl.includes(idData) ){
          for( x=0; x<=11; x++){                      
                userList.rows[ ix ].cells[ x ].style.cssText = 'background-color:#ccffcc;';      
          }
        }
        else{
          for( x=0; x<=11; x++){                      
                userList.rows[ ix ].cells[ x ].style.cssText = 'background-color:white;';      
          }
        }
      }
  }                    
}




/**********************************************
  関数名
  引数
  返却値
  機能
  処理
            WebSoket　接続する
***********************************************/
function openBtn(){
    console.log('href:' + location.href);
    console.log('protocol:' + location.protocol);
    console.log('host:' + location.host);
    console.log('hostname:' + location.hostname);
    console.log('port:' + location.port);
    console.log('pathname:' + location.pathname);
    console.log('search:' + location.search);
    console.log('hash:' + location.hash);
    //ws = new WebSocket("ws://ik1-446-55369.vs.sakura.ne.jp:8888/websocket");
    ws = new WebSocket(`ws://${location.host}/websocket`);
    //ws = new WebSocket("ws://localhost:8888/websocket");

    ws.onopen = function() {
        console.log("openしました");
        
        $("#loginStatusID").html( "接続中" );
        $("#loginStatusID").css("color","greenyellow");
    };
    ws.onclose = function() {
       console.log("closeしました");
        $("#loginStatusID").html( "未接続" );
       ws =null;
    };
    
    //メッセージ受信
    ws.onmessage = function(ev) {
    
        rcvObj = JSON.parse( ev.data );

        if( rcvObj["function"] =="reg" ){
          登録の受信( rcvObj );
        }
        else if ( rcvObj["function"] =="update" ){
          更新の受信( rcvObj );
        }
        else if ( rcvObj["function"] =="list" ){
          一覧の受信( rcvObj );
        }
        else if ( rcvObj["function"] =="find" ){
          検索結果の受信( rcvObj );
        }

        else if ( rcvObj["function"] =="workingID" ){
          workingIdTbl = rcvObj["data"];
          //console.log( "workingID", workingIdTbl );
          作業中ID表示();
        }
        else{
          alert("main.js openBtn rcvObj[function]エラー ");
        }

    }
}

/*  
'''''''''''''''''''''''''''''''''''''''''''''
  関数名
            ＷｅｂSoketを切断する
    
  引数
            function closeBtn()

  返却値
  機能
  処理
'''''''''''''''''''''''''''''''''''''''''''''
*/                     
function closeBtn(){
    $("#loginStatusID").css("color","pink");
    if(　ws === null ){
        console.log("close　しています");  
    }
    else{
        ws.close();
        console.log("close させます");                            
    }
}                                    

//ロールバック、
//作業中の顧客情報の取得

function simpleSendMsg( msg ){

  let json ={
      "function":msg,
      "data":{}
  }

  jsnStr = JSON.stringify( json );
  ws.send( jsnStr  );
}


