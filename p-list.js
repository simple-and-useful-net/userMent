
var msg={ 
      "function": "",
      "status":   "",
      
      "info":   {
        "topID":  "",
        "lastID": "",
        "nextPage": "",
        "prevPage": "",
      },
 
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






/*'''''''''''''''''''''''''''''''''''''''''''''
  関数名   一覧から細画面にリンクする
  引数
  返却値
  機能
  処理
'''''''''''''''''''''''''''''''''''''''''''''*/ 
function linkFunc( id ){

    msg["function"] = "selId";
    msg["id"]       = id;

    ws.send( JSON.stringify( msg ) );
}



/*'''''''''''''''''''''''''''''''''''''''''''''
  関数名   一覧のテーブル作成
  引数
  返却値
  機能
  処理
'''''''''''''''''''''''''''''''''''''''''''''*/ 
function mkTbl( x,y ){


      var tblbody = document.getElementsByTagName("table")[0];
      //var body = document.getElementsByTagName("body")[0];
      //let tbl = document.createElement("table");
      //tbl.id = "tbl"
      //let tbl1 = document.getElementById("tbl");

      let tbl = document.getElementById('tbl');
      let tr = document.getElementById('listTrID');
      //let tr  = document.getElementsByTagName("tr"); 
      
      if (  tr !== null ){ 
          return;
      }
      

      //行追加
      
      function addLine(){

          let tr = document.createElement("tr"); 
          tr.id="listTrID";
          
          for(let i=0;i<x;i++){
              let td = document.createElement("td");
              tr.appendChild(td);
          }

          tbl.appendChild(tr);  
      }

      for(let i=0;i<y;i++){
      
          addLine();
      }

      //tbl.setAttribute("border","1");
      //tblbody.appendChild(tbl);
}


/*'''''''''''''''''''''''''''''''''''''''''''''
  関数名   
  *       HTMLテーブルに値を設定
  引数
  返却値
  機能
  処理
'''''''''''''''''''''''''''''''''''''''''''''*/ 
var arSize   =[
    50,200,150,150,100,50,
    80,80,180,180,180,180,    //住所
    100
  ]

function clrTable( idName, maxRows, maxCells ){

  var userList = document.getElementById( idName );
  for( i=0; i< maxRows; i++){                            

      for( ct=0; ct< maxCells; ct++){                      
          // セルサイズ指定
          size = arSize[ct];
          //userList.rows[i+1].cells[ ct ].style.cssText = 'font-size: 16px; color: gray;';              
          userList.rows[i+1].cells[ ct ].style.display ="";
          userList.rows[i+1].cells[ ct ].style.cssText  = 'font-size: 12px;';              
          userList.rows[i+1].cells[ ct ].style.width       = String(size)+"px";
          userList.rows[i+1].cells[ ct ].innerHTML= "";
      }
  }                    
}

var dispMode ="A";

function listDisp1( ){

    dispMode ="J";
    var userList = document.getElementById("tbl");

    for( let ix=0; ix<11; ix=ix+1){                            

        userList.rows[ ix ].cells[ 12 ].style.display ="none";
        for( x=2; x<=5; x++){                      
              userList.rows[ ix ].cells[ x ].style.display ="none";
        }
        for( x=6; x<=11; x++){                      
              userList.rows[ ix ].cells[ x ].style.display ="";
              userList.rows[ ix ].cells[ x ].style.cssText = 'font-size: 14px;';      
              size = arSize[ x ];
              userList.rows[ ix ].cells[ x ].style.width   = String(size)+"px";
        }
    }                    
}

function listDisp2( ){

    dispMode ="R";
    var userList = document.getElementById("tbl");

    for( let ix=0; ix< 11; ix++){                            

        userList.rows[ ix ].cells[ 12 ].style.display ="none";
        for( x=2; x<=5; x++){                      
              userList.rows[ ix ].cells[ x ].style.display ="";
              userList.rows[ ix ].cells[ x ].style.cssText = 'font-size: 14px;';              
              size = arSize[ x ];
              userList.rows[ ix ].cells[ x ].style.width   = String(size)+"px";
        }
        for( x=6; x<=11; x++){                      
              userList.rows[ ix ].cells[ x ].style.display ="none";
        }
    }                    
}
function listDisp3( ){

    dispMode ="A";
    var userList = document.getElementById("tbl");

    for( let ix=0; ix< 11; ix++){                            

        userList.rows[ ix ].cells[ 12 ].style.display ="none";
        for( x=2; x<=11; x++){                      
              userList.rows[ ix ].cells[ x ].style.display ="";
              userList.rows[ ix ].cells[ x ].style.cssText = 'font-size: 12px;';              
              size = arSize[ x ];
              userList.rows[ ix ].cells[ x ].style.width   = String(size)+"px";
        }
    }                    
}


function setTable( jsData ){


    var userList = document.getElementById("tbl");
    var head =["ID", "名前", "メール","電話", "誕生日", 
        "性別","郵便番号","都道府県","市区町村","町名・番地","町名・番地","趣味"];

    clrTable("tbl", 10,12+1);

    ct = 0;
    for( key in head){                      

        userList.rows[0].cells[ ct ].innerHTML= "<b><center>" + head[key] + "</center></b>"; 
        ct ++;
    }

    data = jsData["data"];

    for( i=0; i< data.length; i++){                            

        rec = data[i];
        ct =0;                        
        for( key in rec){                      
            // userList.rows[i].cells[ ct ].innerHTML= String(i)+ "|" +String(ct);
            //if( key =="sex" ){
                //break
            //}
            //ここで、詳細画面のボタンを作成
            if( ct==0 ){
              btn = "<button type='button' onclick='linkFunc(" + rec[ key ]  +")'>" + rec[ key ] + "</button>";
              userList.rows[i+1].cells[ ct ].innerHTML= btn;
            }
            else{
                userList.rows[i+1].cells[ ct ].innerHTML= rec[ key ];
            }
            ct ++;
            userList.rows[i+1].cells[ ct ].innerHTML= rec[ "id" ];
            //alert(ct);
        }
    }                    

  if( dispMode == "A")  listDisp3();
  if( dispMode == "R")  listDisp2();
  if( dispMode == "J")  listDisp1();
}



  
          
/*************************************************
  関数名   ボタン処理
  引数
  返却値
  機能
  処理
**************************************************/

  function topBtn(){
      //$("#myContents").empty();
      //document.getElementById("my0").style.display ="block";
      //document.getElementById("tbl").style.display ="block";
      //document.getElementById("message").style.display ="block";

      msg = getInputData(msg);
      msg["function"] = "top";
      ws.send( JSON.stringify( msg ) );
  }

  function lastBtn(){

      console.log("lastBtn before",msg);

      msg = getInputData(msg);
      msg["function"] = "last";
      
      ws.send( JSON.stringify( msg ) );
      console.log("lastBtn after",msg);
      //sendProc();
  }

  function nextBtn(){

      console.log("next-msg===",msg);

      msg = getInputData(msg);
      msg["function"] = "next";
      ws.send( JSON.stringify( msg ) );
  }

  function prevBtn(){

      console.log("prev-msg===",msg);

      msg = getInputData(msg);
      msg["function"] = "prev";
      ws.send( JSON.stringify( msg ) );
  }

  function reloadPage(){

      msg = getInputData(msg);
      msg["function"] = "reload";
      console.log("reload >>> ",msg);
      //ws.send( JSON.stringify( msg ) );
  }



  var sData ="";
  function sendProc(){

      if( ws.readyState !==1 ){
          console.log( "readyState error", ws.readyState);
          setTimeout(sendProc, 1000);
          return;
      }
    
       ws.send( sData );
       console.log("送信しました", sData);                        
  } 


         
  

/*'''''''''''''''''''''''''''''''''''''''''''''
  関数名   受信
  引数
  返却値
  機能
  処理
'''''''''''''''''''''''''''''''''''''''''''''*/ 
  function 一覧の受信( rcvData )
  {
          //データが０県の場合
    if (rcvData === null){
      $('#top').prop( 'disabled', true  );
      $('#last').prop( 'disabled', true  );
      $('#prev').prop( 'disabled', true  );
      $('#next').prop( 'disabled', true  );
    
      $('#message').html("登録されていません！");
      return;
    }
    
    else{
        setTable( rcvData );
        作業中ID表示();
        //console.log("受信データ=", msg);
        
        msg["info"]["nextPage"] = rcvData["info"]["nextPage"];
        msg["info"]["prevPage"] = rcvData["info"]["prevPage"];
        msg["info"]["topID"] = rcvData["info"]["topID"];
        msg["info"]["lastID"] = rcvData["info"]["lastID"];
        
        console.log("--------- rcvData -", msg["info"]    );
        console.log("msg=", msg["info"]    );
        console.log("nextPage=", msg["info"]["nextPage"]    );
        console.log("prevPage=", msg["info"]["prevPage"]    );
        
        $('#top' ).prop( 'disabled', false   );
        $('#last').prop( 'disabled', false   );
        $('#next').prop( 'disabled', !rcvData["info"]["nextPage"]   );
        $('#prev').prop( 'disabled', !rcvData["info"]["prevPage"]   );
        if(  rcvData["info"]["nextPage"]== false ){
            
          if(  rcvData["info"]["prevPage"]== false ){
            $('#top' ).prop( 'disabled', true   );
            $('#last').prop( 'disabled', true   );
            $('#message').html("次の頁はありません");
          }
          else{
            $('#last').prop( 'disabled', true   );
            $('#message').html("最終の頁です");
          }
        }
        else{

          if(  rcvData["info"]["prevPage"]== false ){
            $('#top').prop( 'disabled', true   );
            $('#message').html("最初の頁です");
          }
          else{
            $('#message').html("前後の頁はあります");
          }
       }   
    }
  }      

