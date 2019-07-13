// 云函数入口文件
const cloud = require('wx-server-sdk')
const got = require('got')
const cryptojs = require('crypto-js')

cloud.init()
// const db = cloud.database()
// const coll = db.collection('tempAudio')

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

  console.log("get openid")
  const { OPENID } = cloud.getWXContext()
  const secretid = "AKID97uWzGiCqrfJiqnZZMFapq33pMho4lv4"
  const secretkey = "rZ3Wmob0BBxU8YkhPt9C2qPlxBBA3o22"
  tecentApi = "https://aai.tencentcloudapi.com"
  const timestamp = Date.parse(new Date()) / 1000

  const fid = event.record
  let tempf = await cloud.getTempFileURL({
    fileList: [fid]
  })
  // await coll.add({
  //   data: {
  //     _openId: OPENID,
  //     timestamp: timestamp,
  //     file: fid
  //   }
  // })
  console.log("音频文件:"+tempf.fileList[0].tempFileURL)
  let params = {
    "Action": "SentenceRecognition",
    "EngSerViceType": "8k",
    "Nonce": Math.floor(Math.random() * timestamp + 1),
    "ProjectId": 0,
    "SecretId": secretid,
    "SourceType": 0,
    "SubServiceType": 2,
    "Timestamp": timestamp,
    "Url": tempf.fileList[0].tempFileURL,
    "UsrAudioKey": OPENID+timestamp,
    "Version": "2018-05-22",
    "VoiceFormat": "mp3"
  }
  let src = "POST" + "aai.tencentcloudapi.com/?" + paramjoin(params)
  console.log("src=" + src)
  const sign = cryptojs.enc.Base64.stringify(cryptojs.HmacSHA1(src, secretkey))
  console.log(sign)
  params["Signature"] = sign
  console.log(params)
  // console.log(json2form(params))
  // console.log(json2form(params) + "&Signature=" + sign)
  console.log("send request")
  let resp = await got(tecentApi, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/x-www-form-urlencoded'
    },
    // body: json2form(params)+"&Signature="+sign
    body: json2form(params)
  })
  console.log("response got")

  console.log(resp.body)
  
  return JSON.parse(resp.body)
}