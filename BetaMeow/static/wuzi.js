/*状态事件*/
function status1(){
      //window.location.href=window.location;
      if(isbegin){
         alert("game has begun");
         return;
      }
      document.getElementById('qizi').src="static/black.png";
   }
function status2(){
      if(isbegin){
         alert("game has begun");
         return;
      }
      document.getElementById('qizi').src="static/white.png";
   }

/* 控件事件 */
function closeFunction() {
   if (confirm("是否退出游戏？")) {
      window.close();
   } else {
      history.back();
   }
}

/* 判断输赢 */
var cnt = (function() {
   var curr ='black';
   return function() {
      var tmp = curr;
      if (curr == 'black') {
         curr = 'white';
      } else {
         curr = 'black';
      }
      return tmp;
   }
})();

var tds = document.getElementsByTagName('td');
var iswin = false; // 有没有分出胜负
var isbegin = false;
// 负责下棋，即改变单元格的背景
var xia = function() {
   // 判断是否已分出胜负
   //var color = cnt();

   if (this.style.background.indexOf('.png') >= 0) {
      alert('不能重复放置棋子！');
      return;
   }
   //x: this.cellIndex,y: this.parentElement.rowIndex
   //alert(this.cellIndex+"  "+this.parentElement.rowIndex);
    put_chess(this.parentElement.rowIndex, this.cellIndex, 1);
   this.style.background = 'url(' + document.getElementById('qizi').src + ')';
   isbegin = true;
       var win = checkWin();
    if(win == 1) {
        iswin = true;
        alert("黑棋获胜")
    }
   if (iswin) {
      alert('游戏结束!');
      return;
    }

    ai_put("five/ai", window.chess, callback)
   //xmlHttp = new XMLHttpRequest();
   //xmlHttp.onreadystatechange = callback;
   //xmlHttp.open("POST","/five/ai",true)
   //xmlHttp.send(null);
   //todo 1.according to location show qizi 2.step need know where you hit and return where ai put
   //judge.call(this, color); // 下完棋后判断胜负
}

function ai_put(hostname, chess, func){
    var data = {
        "ai_color":2,
        "data":JSON.stringify(chess)
    }
    $.post(hostname,data,function(respond,status){
        func(respond);
    })
}

function put_chess(x, y, value) {
    chess[x][y] = value;
}

function callback(responed){
    var res = JSON.parse(responed)
    //var json = responseText.parseJSON();
    console.log(res);
    if(res.sta == "succ") {
        var x = res.location[0]
        var y = res.location[1]
        //alert(getCell(x, y));
        getCell(x, y).style.background = getAnotherPic();
        put_chess(x, y, 2);
        var r = checkWin();
        if(r == 2) {
            iswin = true;
            alert("白棋获胜")
        }
    }
}

function getAnotherPic(){
   src = "static/white.png"
   //alert(document.getElementById('qizi').src)
   if(document.getElementById('qizi').src.indexOf('white') > 0){
      src = "static/black.png";
   }
   return 'url(' + src + ')';
}

function getCell(rowIndex,cellIndex){
   //return $("#chessboard").eq(rowIndex).find("td").eq(cellIndex);
   return document.getElementById("chessboard").rows[rowIndex].cells[cellIndex];
}

window.onload = function() {
   var row = 15;
   var column = 15;
   var html = "";
    window.chess = [];
    window.SIZE = 15;
   for(var i = 0;i<row;i++)
   {  
      var tr = "<tr>";
       var row_data = [];
      for(var j = 0;j<column;j++)
      {
         tr += "<td>&nbsp;</td>"
          row_data.push(0)
      }
      tr +="</tr>"
       chess.push(row_data);
      html += tr;
   }
   $("#chessboard").append(html);
   $("table").click(function(ev) {
      // 1. 下棋
      //alert(1);
      // 2. 判断胜负
      //alert(ev.target);
      xia.call(ev.target);
   });
}
function checkWin (){
    var isEmpty = false
    for(var i = 0;i<SIZE;i++){
        for(var j = 0;j<SIZE;j++){
            if(chess[i][j] == 0){
                isEmpty = true
            }else{
                var color = chess[i][j]
                if(j < SIZE-4){
                    if(color == chess[i][j+1]
                       && color == chess[i][j+2]
                       && color == chess[i][j+3]
                       && color == chess[i][j+4]){
                        return color
                    }
                }

                if(i < SIZE-4){
                    if(color == chess[i+1][j]
                       && color == chess[i+2][j]
                       && color == chess[i+3][j]
                       && color == chess[i+4][j]){
                        return color
                    }
                }
                
                if(i < SIZE-4 && j < SIZE-4){
                    if(color == chess[i+1][j+1]
                       && color == chess[i+2][j+2]
                       && color == chess[i+3][j+3]
                       && color == chess[i+4][j+4]){
                        return color
                    }
                }

                if(i >=4 && j < SIZE-4){
                    if(color == chess[i-1][j+1]
                       && color == chess[i-2][j+2]
                       && color == chess[i-3][j+3]
                       && color == chess[i-4][j+4]){
                        return color
                    }
                }
                
                
            }
        }
    }
    if(!isEmpty){
        return 0
    }
}
