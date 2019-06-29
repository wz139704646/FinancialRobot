const cloud = require('wx-server-sdk')
const got = require('got')
const crypto = require('crypto')


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
  console.log("get openid")
  const { OPENID } = cloud.getWXContext()
  const secretid = "AKID97uWzGiCqrfJiqnZZMFapq33pMho4lv4"
  const secretkey = "rZ3Wmob0BBxU8YkhPt9C2qPlxBBA3o22"
  tecentApi = "https://aai.tencentcloudapi.com"

  const timestamp = Date.parse(new Date()) / 1000
  let params = {
    'Action': 'DescribeInstances',
    'InstanceIds.0': 'ins-09dx96dg',
    'Limit': 20,
    'Nonce': 11886,
    'Offset': 0,
    'Region': 'ap-guangzhou',
    'SecretId': 'AKIDz8krbsJ5yKBZQpn74WFkmLPx3EXAMPLE',
    'Timestamp': 1465185768,
    'Version': '2017-03-12',
  }
  let src = "GET" + "cvm.tencentcloudapi.com/?" + paramjoin(params)
  console.log("src=" + src)
  console.log("equal?:"+(src =="GETcvm.tencentcloudapi.com/?Action=DescribeInstances&InstanceIds.0=ins-09dx96dg&Limit=20&Nonce=11886&Offset=0&Region=ap-guangzhou&SecretId=AKIDz8krbsJ5yKBZQpn74WFkmLPx3EXAMPLE&Timestamp=1465185768&Version=2017-03-12"))
  const sign = crypto.createHmac('sha1', src, "Gu5t9xGARNpq86cd98joQYCN3EXAMPLE").digest().toString('base64')
  console.log("Signature:"+sign)
  params["Signature"] = sign
  console.log(params)
  console.log(json2form(params))
  // console.log(json2form(params) + "&Signature=" + sign)
  // console.log("send request")
  // let resp = await got(tecentApi, {
  //   method: 'POST',
  //   headers: {
  //     'Content-Type': 'application/x-www-form-urlencoded'
  //   },
  //   //body: json2form(params)+"&Signature="+sign
  //   body: json2form(params)
  // })
  // console.log("response got")

  // console.log(resp.body)

  // return resp.body
  return
}