const cloud = require('wx-server-sdk')
const cryptojs = require('crypto-js')


cloud.init()

const json2form = json => {
  var str = []
  for (var p in json) {
    str.push(encodeURIComponent(p) + "=" + encodeURIComponent(json[p]))
  }
  return str.sort().join("&")
}

const paramjoin = json => {
  var str = []
  for (var p in json) {
    str.push(p + "=" + json[p])
  }
  return str.sort().join("&")
}
// 云函数入口函数
exports.main = async (event, context) => {
  const sign = cryptojs.enc.Base64.stringify(cryptojs.SHA1('123456'))
  console.log(sign)
}