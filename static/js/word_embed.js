import levelData from './NaerWordLevel.js'

let formSelectDiv = document.getElementById("formSelectDiv")
let senteditInput = document.getElementById("sentedit_input")
let p1 = document.getElementById("p1")
let p2 = document.getElementById("p2")
let p3 = document.getElementById("p3")
const biaoYin = document.querySelectorAll('input[name="biaoYin"]')
const resetBtn = document.getElementById('resetTextarea')
const copyBtn = document.getElementById('copyBtn')
const scrShotBtn = document.getElementById('scrShotBtn')
const scrShotBtn2 = document.getElementById('scrShotBtn2')
const scrShotBtn3 = document.getElementById('scrShotBtn3')
const scrShotBtn4 = document.getElementById('scrShotBtn4')
const resetSelectorBtn = document.getElementById('resetSelectorBtn')

formSelectDiv.addEventListener('change', changeArea)

// change事件觸發：覆寫展示句子的函式、更改詞語等級顯示
function changeArea(e) {
  if (e.target.tagName.toLowerCase() === 'select') {
    console.log(document.getElementById("formSelectDiv").childElementCount-4);
    // 用陣列儲存當前網頁select元件的展示value
    let arr = []
    // let changeTarget = document.getElementById(e.target.id)
    let changeIdNumber = e.target.id.split('-')[2]
    let changeMarkLevel = document.getElementById(`markLevel-${changeIdNumber}`)
    let changeFormSelect = document.getElementById(`form-select-${changeIdNumber}`)
    let changeLevelNum = document.getElementById(`level-num-${changeIdNumber}`)

    let word = e.target.value.split(" ")[1]
    changeMarkLevel.setAttribute('class', judgeWordLevel(word)["className"])
    changeMarkLevel.title = judgeWordLevel(word)["title"]
    changeFormSelect.title = judgeWordLevel(word)["title"]
    changeLevelNum.textContent = judgeWordLevel(word)["levelNum"]

    for (let i = 1; i <= document.getElementById("formSelectDiv").childElementCount-4; i++) {
      let formSelect = document.getElementById(`form-select-${i}`);
      let selectedString = formSelect.options[formSelect.selectedIndex].text
      //  console.log(formSelect.options[0].text)  // 可以應用在重置替換後文句
      if (i.toString() === changeIdNumber) {
        arr.push(`<span class="text-danger">${selectedString.split(" ")[1]}</span>`)
      }
      else {
        arr.push(selectedString.split(" ")[1])
      }

    }
    senteditInput.innerHTML = `${arr.join("")}`
    // sentEditBtn.click()
  }
}

function judgeWordLevel(word) {
  if (!levelData.hasOwnProperty(word)) {
    return {
      "className": "level_X",
      "title": "未收錄",
      "levelNum": "X"
    }
  }
  else {
    //* forEach遍歷分級詞語的分級
    let levelArr = levelData[word]
    let titleStrArr = []
    let levelNumArr = []
    levelArr.forEach(function (arr) {
      titleStrArr.push(arr[0] + "," + arr[1])
      levelNumArr.push(arr[0])
    })

    return {
      "className": "level_" + levelData[word][0][0],
      "title": titleStrArr.join("； "),
      "levelNum": levelNumArr.join(",")
    }
  }
}


resetBtn.addEventListener('click', function () {
  let senteditInput = document.getElementById('sentedit_input')
  senteditInput.innerText = ""
})

biaoYin.forEach((elem) =>{ elem.addEventListener('change', function(e){
    // console.log(e.target.value)
    if (e.target.value === "No"){
        senteditInput.style.fontFamily = "Microsoft JhengHei, BiauKai, DFKai-sb, sans-serif"
        senteditInput.style.fontSize = "x-large"
    }
    else if (e.target.value === "ZhuYin"){
        senteditInput.style.fontFamily = "ZY, BiauKai, Microsoft JhengHei, sans-serif"
        senteditInput.style.fontSize = "x-large"
    }
    else if (e.target.value === "PinYin"){
      senteditInput.style.fontFamily = "PY, BiauKai, Microsoft JhengHei, sans-serif"
      senteditInput.style.fontSize = "xx-large"
    }
  })
})


copyBtn.addEventListener('click', function () {
  // floatingTextarea.select
  if (!navigator.clipboard) {
    document.execCommand('copy')
    alert("已複製替換後文句中的文字了!")
    // console.log('舊版')
  }
  else {
    navigator.clipboard.writeText(senteditInput.textContent)
    alert("已複製替換後文句中的文字了!")
    // console.log('新版', floatingTextarea.value)
  }
})

resetSelectorBtn.addEventListener('click', function () {
    let arr = []
    if (document.getElementById("formSelectDiv").childElementCount-4 >= 1){
      for (let i = 1; i <= document.getElementById("formSelectDiv").childElementCount-4; i++) {
      let formSelect = document.getElementById(`form-select-${i}`)
      let options = formSelect.options
      // 可以應用在重置替換後文句
      arr.push(options[0].text.split(" ")[1])
      for (let j = 0; j < options.length; j++) {
          options[j].selected = options[j].defaultSelected
      }
      }
      senteditInput.innerText = `${arr.join("")}`
    }
    else{
      senteditInput.innerText = ""
    }
    
})

// *擷圖1個區塊的功能-編輯區
scrShotBtn.addEventListener('click', function () {
  senteditInput.style.borderColor = 'white'
  html2canvas(senteditInput).then(function (canvas) {
    document.body.appendChild(canvas);
    var a = document.createElement('a');
    a.href = canvas.toDataURL("image/jpeg").replace("image/jpeg", "image/octet-stream");
    a.download = '文句擷圖.jpg';
    a.click();
    document.body.removeChild(canvas)
    // document.querySelector('canvas').style.display = "none"
  })
  senteditInput.style.borderColor = '#ced4da'
})

// *擷圖1個區塊的功能-分級標記
scrShotBtn2.addEventListener('click', function () {
  this.style.display = 'none';
  html2canvas(p1).then(function (canvas) {
    document.body.appendChild(canvas);
    var a2 = document.createElement('a');
    a2.href = canvas.toDataURL("image/jpeg").replace("image/jpeg", "image/octet-stream");
    a2.download = '分級標記擷圖.jpg';
    a2.click();
    document.body.removeChild(canvas)
  })
  this.style.display = 'block';
})

// *擷圖1個區塊的功能-詞彙等級分布圓餅圖
scrShotBtn3.addEventListener('click', function () {
  this.style.display = 'none';
  html2canvas(p2).then(function (canvas) {
    document.body.appendChild(canvas);
    var a3 = document.createElement('a');
    a3.href = canvas.toDataURL("image/jpeg").replace("image/jpeg", "image/octet-stream");
    a3.download = '圓餅圖擷圖.jpg';
    a3.click();
    document.body.removeChild(canvas)
  })
  this.style.display = 'block';
})

// *擷圖1個區塊的功能-詞表
scrShotBtn4.addEventListener('click', function () {
  this.style.display = 'none';
  html2canvas(p3).then(function (canvas) {
    document.body.appendChild(canvas);
    var a4 = document.createElement('a');
    a4.href = canvas.toDataURL("image/jpeg").replace("image/jpeg", "image/octet-stream");
    a4.download = '詞表擷圖.jpg';
    a4.click();
    document.body.removeChild(canvas)
  })
  this.style.display = 'block';
})



// 取得回到頂部按鈕
let btnBackToTop = document.getElementById("btn-back-to-top");

// 當使用者下從頂端向下捲至20px時，顯示按鈕
window.onscroll = function () {
  scrollFunction();
};

function scrollFunction() {
  if (
    document.body.scrollTop > 20 ||
    document.documentElement.scrollTop > 20
  ) {
    btnBackToTop.style.display = "block";
  } else {
    btnBackToTop.style.display = "none";
  }
}

// 點擊按鈕，觸發回到頂部的事件
btnBackToTop.addEventListener("click", backToTop);

function backToTop() {
  console.log(btnBackToTop.value);
  document.body.scrollTop = 0;
  document.documentElement.scrollTop = 0;
}