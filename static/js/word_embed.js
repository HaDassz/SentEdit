import levelData from './NaerWordLevel.js'

//const {selectorCnt} = require('./tools.js')
let formSelectDiv = document.getElementById("formSelectDiv")
let selectorCnt = formSelectDiv.childElementCount 
let senteditInput = document.getElementById("sentedit_input")
const biaoYin = document.querySelectorAll('input[name="biaoYin"]')
const resetBtn = document.getElementById('resetTextarea')
const copyBtn = document.getElementById('copyBtn')
const scrShotBtn = document.getElementById('scrShotBtn')
const resetSelectorBtn = document.getElementById('resetSelectorBtn')
// let defaultDisplayStr = ""
// console.log("詞語數量：", selectorCnt)

// 初始化展示原本句子，以及呈現各詞語的等級
function initformSelectDiv(){
  for (let i = 1; i <= document.getElementById("formSelectDiv").childElementCount-4; i++) {
  // let selectedOpt = document.getElementById(`form-select-${i}`).querySelector(".selectedOpt")
  let markLevel = document.getElementById(`markLevel-${i}`)
  let formSelect = document.getElementById(`form-select-${i}`)
  let levelNum = document.getElementById(`level-num-${i}`)

  // 填入文字修改區初始字串
  // let word = selectedOpt.textContent.split(" ")[1]
  // defaultDisplayStr += word
  markLevel.setAttribute('class', judgeWordLevel(word)["className"])
  markLevel.title = judgeWordLevel(word)["title"]
  formSelect.title = judgeWordLevel(word)["title"]
  levelNum.innerHTML = `${judgeWordLevel(word)["levelNum"]}<br>`
  // arr.push(formSelect.options[formSelect.selectedIndex].text);
  }
}

if (selectorCnt !== 0){
  initformSelectDiv()
}


// floatingTextarea.textContent = defaultDisplayStr


formSelectDiv.addEventListener('change', changeArea)

// change事件觸發：覆寫展示句子的函式、更改詞語等級顯示
function changeArea(e) {
  if (e.target.tagName.toLowerCase() === 'select') {
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

    //! 這邊要再修改(110/10/18應該完成了,變色高亮功能完成)
    for (let i = 1; i <= document.getElementById("formSelectDiv").childElementCount-4; i++) {
      console.log(document.getElementById("formSelectDiv").childElementCount);
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

    // console.log("事件目標值：", e.target.value)
    // console.log("選項陣列值：", arr.join(""))
    senteditInput.innerHTML = `${arr.join("")}`
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

// *擷圖1個區塊的功能
scrShotBtn.addEventListener('click', function () {
  html2canvas(floatingTextarea).then(function (canvas) {
    document.body.appendChild(canvas);
    var a = document.createElement('a');
    a.href = canvas.toDataURL("image/jpeg").replace("image/jpeg", "image/octet-stream");
    a.download = '文句擷圖.jpg';
    a.click();
    document.querySelector('canvas').style.display = "none"
  })
})

resetSelectorBtn.addEventListener('click', function () {
  let arr = []
  for (let i = 1; i <= selectorCnt; i++) {
    let formSelect = document.getElementById(`form-select-${i}`)
    let options = formSelect.options
    // 可以應用在重置替換後文句
    arr.push(options[0].text.split(" ")[1])
    for (let j = 0; j < options.length; j++) {
      options[j].selected = options[j].defaultSelected
    }
  }
  floatingTextarea.textContent = `${arr.join("")}`
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
  document.body.scrollTop = 0;
  document.documentElement.scrollTop = 0;
}
