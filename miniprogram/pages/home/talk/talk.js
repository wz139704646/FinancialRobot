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
    inputBottom: 0
  },
  /**
 * 获取聚焦
 */
  InputFocus(e) {
    keyHeight = e.detail.height
    this.setData({
      scrollHeight: (windowHeight - keyHeight) + 'px'
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
      scrollHeight: '100vh',
      inputBottom: 0,
      toView: 'msg-' + (msgList.length - 1)
    })
  },


  onLoad: function (options) {
    initData(this);
    // this.setData({
    //   cusHeadIcon: app.globalData.userInfo.avatarUrl,
    // });
  },

  sendMsg: function (e) {
    console.log("输入对话")
    msgList.push({
      speaker: 'customer',
      contentType: 'text',
      content: e.detail.value
    })
    inputVal = '';
    this.setData({
      msgList,
      inputVal
    });


    //这里写处理对话的代码


  }
})
  