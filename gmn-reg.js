
regHtml = `

    <div class="reg">
    
        <dl id="formID">

          <dt id="idid">ID</dt>
          <dd><input type="text" name="id" disabled></dd>

        
          <dt>お名前</dt>
          <dd><input type="text" name="name" value="" size=30>
          </dd>

          <dt>生年月日</dt>
              <dd><input type="date" name="birthday" value="">
          </dd>

          <dt class="フィルタCLS">性別</dt>
          <dd class="フィルタCLS">
              <span id="フィルタID" style="display:none"> 
              <input type="radio" name="sex" value="" checked>指定無し
              </span>
              <input type="radio" name="sex" value="男性">男性
              <input type="radio" name="sex" value="女性">女性
          </dd>

          <dt>電話番号</dt>
          <dd><input type="text" name="tel" value="">
          </dd>

          <dt>メールアドレス</dt>
          <dd><input type="email" name="email" value="">
          </dd>

          <br>
        
          <dt>郵便番号</dt>
          <dd><input type="text" name="postal_code" value="">
          </dd>

          <dt class="フィルタCLS" >都道府県</dt>
          <dd class="フィルタCLS" >
            <select id="prefectureID" name="prefecture">
            
              <option value=""   ></option>
              <option value="北海道"     >北海道</option>
              <option value="青森県"     >青森県</option>
              <option value="東京都"     >東京都</option>
              <option value="大阪府"     >大阪府</option>
              <option value="沖縄県"     >沖縄県</option>
            </select>
          </dd>


          <dt class="フィルタCLS" >市区町村</dt>
          <dd class="フィルタCLS" ><input type="text" name="city" value="">
          </dd>
            
          <dt>町名・番地</dt>
          <dd><input type="text" name="address1" value="">
          </dd>

          <dt>建物名（部屋番号）</dt>
          <dd><input type="text" name="address2" value="">
          </dd>

          <br>
          
          <dt class="フィルタCLS" >趣味</dt>
          <dd class="フィルタCLS" ><input type="checkbox" name="hobby" value="音楽">音楽
              <input type="checkbox" name="hobby" value="アウトドア">アウトドア
              <input type="checkbox" name="hobby" value="映画">映画
          </dd>
        </dl>


      <input type="hidden" name="userid" value="">
      
      <button type="button" class="menuBTN" id="登録BtnID"      onclick="登録の送信()"      >登録</button>
      <button type="button" class="menuBTN" id="更新BtnID"      onclick="更新の送信()"      >更新</button>

      <button type="button" class="menuBTN" id="フィルタBtnID"   onclick="topBtn()"         >フィルタ</button>
      <button type="button" class="menuBTN" id="検索開始BtnID"   onclick="検索の送信()"     >検索開始</button>
      <button type="button" class="menuBTN" id="キャンセルBtnID" onclick="キャンセル処理()" >キャンセル</button>


  </div>
`;
