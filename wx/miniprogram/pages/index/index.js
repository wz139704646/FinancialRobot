Page({
  data: {
    PageCur: 'application'
  },
  NavChange(e) {
    console.log("navigate change")
    console.log(e)
    this.setData({
      PageCur: e.currentTarget.dataset.cur
    })
  },
  onShareAppMessage() {
    return {
      title: '财务机器人',
      imageUrl: '/images/share.jpg',
      path: '/pages/login/login'
    }
  },
  NavToTalk(){
    wx.navigateTo({
      url: '/pages/talk/talk',
    })
    console.log("navigate")
  }
})