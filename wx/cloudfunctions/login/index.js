// 云函数入口文件
const cloud = require('wx-server-sdk')

cloud.init()

// 云函数入口函数
exports.main = async (event, context) => {
  const wxContext = cloud.getWXContext()
  let cloudID = event.cloudID
  if(!cloudID.errCode){
    return {
      openid: wxContext.OPENID,
      appid: wxContext.APPID,
      unionid: wxContext.UNIONID,
    }
  } else {
    return {
      errMsg: 'cloudID非法或过期'
    }
  }
}