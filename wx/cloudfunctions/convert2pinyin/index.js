// 云函数入口文件
const cloud = require('wx-server-sdk')
var pinyin = require("pinyin")

cloud.init()

// 云函数入口函数
exports.main = async(event, context) => {
  // console.log(pinyin('123abc'))
  config = {
    style: pinyin.STYLE_NORMAL
  }
  // console.log(pinyin('中国', config).join(''))
  let array = JSON.parse(event.jsonStr)
  console.log(typeof(array))
  let options = event.options
  let field = options ? options.field : undefined
  let py = options ? options.pinyin : undefined
  let init = options ? options.initial : undefined
  let ordered = options ? options.ordered : undefined
  for (let i = 0; i < array.length; i++) {
    let itempy = ""
    if (field) {
      itempy = pinyin(array[i][field], config).join('')
      if (py) {
        array[i][py] = itempy
        if (init) {
          array[i][init] = itempy.charAt(0).toUpperCase()
        }
      } else {
        array[i] = itempy
      }
    } else {
      array[i] = pinyin(array[i], config).join('')
    }
  }
  if (field && py && ordered) {
    if(ordered == 'desc'){
      console.log('降序')
      array.sort((a, b) => a[py] > b[py] ? -1 : a[py] < b[py] ? 1 : 0)
    } else{
      console.log('升序')
      array.sort((a, b) => a[py] < b[py] ? -1 : a[py] > b[py] ? 1 : 0)
    }
  } else if(ordered) {
    if (ordered == 'desc'){
      array.sort()
    } else{
      array.sort()
    }
  }
  return array
}