// miniprogram/pages/audiotest.js
Page({

  /**
   * 页面的初始数据
   */
  data: {

  },

  /**
   * 生命周期函数--监听页面加载
   */
  onLoad: function (options) {

  },

  /**
   * 生命周期函数--监听页面初次渲染完成
   */
  onReady: function () {

  },

  /**
   * 生命周期函数--监听页面显示
   */
  onShow: function () {

  },

  /**
   * 生命周期函数--监听页面隐藏
   */
  onHide: function () {

  },

  /**
   * 生命周期函数--监听页面卸载
   */
  onUnload: function () {

  },

  /**
   * 页面相关事件处理函数--监听用户下拉动作
   */
  onPullDownRefresh: function () {

  },

  /**
   * 页面上拉触底事件的处理函数
   */
  onReachBottom: function () {

  },

  /**
   * 用户点击右上角分享
   */
  onShareAppMessage: function () {

  },

  speechRecognition: function (res) {
    console.log("录音结束")
    console.log(res)
    wx.cloud.uploadFile({
      cloudPath: "tempAudio/tempaudio" + Date.parse(new Date()) + ".mp3",
      filePath: res.tempFilePath
    }).then( res => {
      console.log("call cloud function")
      wx.cloud.callFunction({
        name: 'speechRecognition',
        data: {
          record: res.fileID
        }
      }).then(result => {
        console.log(result)
        wx.cloud.deleteFile({
          fileList: [res.fileID]
        })
      })
    } )
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
    recorder.onStart(() => {
      console.log("录音开始")
    })
    recorder.onStop(res=> {
      this.speechRecognition(res)
    })
    recorder.start(options)
  },

  recordEnds: function(e){
    wx.getRecorderManager().stop()
  }
})