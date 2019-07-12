// import Toast from 'vant-weapp/toast/toast';

const app = getApp();
const util = require('../../utils/util.js')
var inputVal = '';
var msgList = [];
var windowWidth = wx.getSystemInfoSync().windowWidth;
var windowHeight = wx.getSystemInfoSync().windowHeight;
var keyHeight = 0;
var host = app.globalData.requestHost

/**
 * 初始化数据
 */
function initData(that) {
  inputVal = '';

  msgList = [{
    speaker: 'server',
    contentType: 'text',
    content: '欢迎使用财务机器人Fibot,请问您有什么指示'
  }
  ]
  that.setData({
    msgList,
    inputVal
  })
}

function calScrollHeight(that, keyHeight) {
  var query = wx.createSelectorQuery();
  query.select('.scrollMsg').boundingClientRect(function(rect) {
  }).exec();
}



Page({
  data: {
    inputBottom: 0,
    soundInput: false,
    recordStarted: false
  },
  /**
 * 获取聚焦
 */
  InputFocus(e) {
    keyHeight = e.detail.height
    this.setData({
      scrollHeight: (windowHeight - keyHeight - 150) + 'px'
    })
    console.log(msgList.length)
    this.setData({
      toView: 'msg-' + (msgList.length - 1),
      inputBottom: e.detail.height
    })
    calScrollHeight(this, keyHeight);
  },
  InputBlur(e) {
    this.setData({
      scrollHeight: '85vh',
      inputBottom: 0,
      toView: 'msg-' + (msgList.length - 1)
    })
  },
  InputChange(e) {
    // console.log(e)
    inputVal = e.detail.value
  },


  onLoad: function (options) {
    initData(this);
    // this.setData({
    //   cusHeadIcon: app.globalData.userInfo.avatarUrl,
    // });

  },

  onShow: function(){
    const recorder = wx.getRecorderManager()
    let that = this
    recorder.onStart(() => {
      console.log("录音开始")
      that.setData({
        recordStarted: true
      })
      // wx.showToast({
      //   title: '录音中',
      //   duration: 30000,
      //   image: '/imgs/voice.gif'
      // })

    })
    recorder.onStop(res => {
      // wx.hideToast()
      this.setData({
        recordStarted: false
      })
      this.speechRecognition(res)
    })
    recorder.onError(err => {
      console.error(err)
      that.setData({
        recordStarted: false
      })
    })
    recorder.onInterruptionBegin(inter => {
      console.log("recording interrupted")
      that.setData({
        recordStarted: false
      })
      that.recordEnds(null)
    })
  },

  sendMsg: function (e) {
    console.log("send")
    if (e.detail.value == "")
      return
    console.log("输入对话")
    msgList.push({
      speaker: 'customer',
      contentType: 'text',
      content: e.detail.value
    })
    inputVal = '';
    this.setData({
      msgList,
      inputVal,
      toView: 'msg-' + (msgList.length - 1),
      scrollHeight: '85vh'
    });

    // 处理对话，调用自然语言处理
    let date = util.getcurDateFormatString(new Date())
    console.log(date)
    wx.request({
      url: host+'/languageProcess',
      method: 'POST',
      header: {
        "Content-Type": 'application/json'
      },
      data: JSON.stringify({
        language: e.detail.value,
        companyId: app.globalData.companyId,
        time: date
      }),
      success: res => {
        console.log('process succeed')
        if(res.statusCode != 200){
          wx.showToast({
            title: '出现未知错误',
            image: '../../imgs/fail.png'
          })
          return
        }
        let data = res.data
        if(data.success){
          result = data.result
          // 将返回信息作为server方发送
          if(result && result.length>0){
            for(let idx in result){
              msgList.push({
                speaker: 'server',
                contentType: 'text',
                content: result[idx]
              })
            }
          } else {
            msgList.push({
              speaker: 'server',
              contentType: 'text',
              content: '不好意思，我听不懂你在说什么'
            })
          }
        } else {
          msgList.push({
            speaker: 'server',
            contentType: 'text',
            content: '不好意思，我听不懂你在说什么'
          })
        }
      },
      fail: err => {
        console.log('request failed')
        console.error(err)
        wx.showToast({
          title: '出现未知错误',
          image: '../../imgs/fail.png'
        })
      }
    })


  },

  sendByTapping: function(e) {
    let text = inputVal
    console.log(text)
    e.detail.value = text!=undefined ? text : ""
    // console.log(e)
    // console.log(this.sendMsg)
    this.sendMsg(e)
  },

  changeInputType: function(e) {
    let type = this.data.soundInput
    this.setData({
      soundInput: !type
    })
  },

  recordBegins: function(e) {
    const recorder = wx.getRecorderManager()
    const options = {
      duration: 30000,
      sampleRate: 8000,
      numberOfChannels: 1,
      encodeBitRate: 16000,
      format: 'mp3',
      frameSize: 50
    }
    wx.getSetting({
      success: suc => {
        console.log('get setting suc')
        if(suc.authSetting['scope.record']){
          recorder.start(options)
        } else {
          wx.authorize({
            scope: 'scope.record',
            success: () => {
              console.log('authorize suc')
            },
            fail: () => {
              console.log('authorize failed')
              wx.showToast({
                title: '获取用户授权失败, 无法录音',
                icon: 'none'
              })
            }
          })
        }
      }
    })
  },

  recordEnds: function(e) {
    if(this.data.recordStarted){
      wx.getRecorderManager().stop()
    }
  },

  speechRecognition: function (res) {
    let that = this
    console.log("录音结束")
    console.log(res)
    wx.showToast({
      title: '识别中',
      icon: 'loading',
      duration: 10000
    })
    wx.cloud.uploadFile({
      cloudPath: "tempAudio/tempaudio" + Date.parse(new Date()) + ".mp3",
      filePath: res.tempFilePath
    }).then(res => {
      console.log("call cloud function")
      wx.cloud.callFunction({
        name: 'speechRecognition',
        data: {
          record: res.fileID
        }
      }).then(result => {
        console.log(result)
        wx.hideToast()
        if (result.result.Response.Error!=undefined ||
            result.result.Response.Result==""){
          wx.showToast({
            title: '识别失败',
            image: '/imgs/fail.png',
            duration: 2000
          })
        } else {
          let msg=result.result.Response.Result
          that.sendMsg({detail:{value: msg}})
        }
        wx.cloud.deleteFile({
          fileList: [res.fileID]
        })
      })
    })
  },
})
  