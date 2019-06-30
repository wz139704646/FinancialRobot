const app = getApp();
var inputVal = '';
var msgList = [];
var windowWidth = wx.getSystemInfoSync().windowWidth;
var windowHeight = wx.getSystemInfoSync().windowHeight;
var keyHeight = 0;

/**
 * 初始化数据
 */
function initData(that) {
  inputVal = '';

  msgList = [{
    speaker: 'server',
    contentType: 'text',
    content: '欢迎使用财务机器人,请问您有什么指示'
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
    }, res => {
      msgList.push({
        speaker: 'server',
        contentType: 'text',
        content: e.detail.value
      }),
      this.setData({
        msgList,
        toView: 'msg-' + (msgList.length - 1),
        scrollHeight: '85vh'
      })
    });


    //这里写处理对话的代码


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
    let that = this
    const recorder = wx.getRecorderManager()
    const options = {
      duration: 30000,
      sampleRate: 8000,
      numberOfChannels: 1,
      encodeBitRate: 16000,
      format: 'mp3',
      frameSize: 50
    }
    recorder.onStart(() => {
      console.log("录音开始")
      that.setData({
        recordStarted: true
      })
      wx.showToast({
        title: '录音中',
        duration: 30000,
        image: '/imgs/voice.gif'
      })
    })
    recorder.onStop(res => {
      wx.hideToast()
      this.setData({
        recordStarted: false
      })
      this.speechRecognition(res)
    })
    recorder.onError( err => {
      console.error(err)
      that.setData({
        recordStarted: false
      })
    } )
    recorder.onInterruptionBegin( inter => {
      console.log("recording interrupted")
      that.setData({
        recordStarted: false
      })
      that.recordEnds(null)
    })
    recorder.start(options)
  },

  recordEnds: function(e) {
    wx.getRecorderManager().stop()
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
  