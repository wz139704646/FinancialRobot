Page({
  data: {
    PageCur: 'home'
  },
  NavChange(e) {
    console.log("navigate change")
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
})