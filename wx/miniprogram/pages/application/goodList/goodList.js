// pages/application/goodList/goodList.js
Page({
  
  /**
   * 页面的初始数据
   */
  data: {
    goodsList: []
      
  },
  onLoad: function (options) {
    var that = this
    that.initGoodList()
  },
  initGoodList(){
    wx.request({
      url: 'http://127.0.0.1:5000/queryGoods',
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