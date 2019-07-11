const app = getApp()
const host = app.globalData.requestHost
Page({
  data: {

    goodsList: []
      
  },
  onLoad: function (options) {
    var that = this
    that.initGoodList()
    this.setData({
      host:host
    })
  },
  initGoodList(){
    wx.request({
      url: 'http://' + host + '/queryGoods',
      data: JSON.stringify({
        companyId:5
      }),
      method: "POST",
      header: {
        "Content-Type": 'application/json'
      },
      success: res => {
        console.log(res)
        console.log(res.data.result.goodsList)
        this.setData({
          goodsList: res.data.result.goodsList
        })
      }
    })
  },
  navigateToGoodInfo(e){
    console.log(e)
  },
  navigateToGoodAnalyse(e){
    console.log(e)
  }
  
})