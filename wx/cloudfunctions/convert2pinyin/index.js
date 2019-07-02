// 云函数入口文件
const cloud = require('wx-server-sdk')
var pinyin = require("pinyin")

cloud.init()

// 云函数入口函数
exports.main = async (event, context) => {
  console.log(pinyin('123abc'))
  config = {
    style: pinyin.STYLE_NORMAL
  }
  // console.log(pinyin('中国', config).join(''))
  let array = JSON.parse(event.jsonStr)
  let options = event.options
  let field = options.field
  let py = options.pinyin
  let init = options.initial
  let ordered = options.ordered
  for(let i=0; i<array.length; i++){
    let itempy = ""
    if(field){
      itempy = pinyin(array[i][field], config).join('')
      if(py){
        array[i] = itempy
      } else {
        array[i][py] = itempy
        if(init){
          array[i][init] = 
        }
      }
    }else{
      array[i] = pinyin(array[i], config).join('')
    }
  }
}