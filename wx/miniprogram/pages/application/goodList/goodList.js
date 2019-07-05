// pages/application/goodList/goodList.js
Page({
  
  /**
   * 页面的初始数据
   */
  data: {
    goodsList: [
      {
        name:"小马",
        category:"动物",
        price:"10000",
        amount:3,
        imgurl:"/imgs/1.jpg",
        description:"这是一只草拟吗"
      },
      {
        name: "小马",
        category: "动物",
        price: "10000",
        amount: 3,
        imgurl: "http://pic37.nipic.com/20140113/8800276_184927469000_2.png",
        description: "这是一只草拟吗"
      },
      {
        name: "小马",
        category: "动物",
        price: "10000",
        amount: 3,
        imgurl: "http://pic37.nipic.com/20140113/8800276_184927469000_2.png",
        description: "这是一只草拟吗"
      },
      {
        name: "小马",
        category: "动物",
        price: "10000",
        amount: 3,
        imgurl: "http://pic37.nipic.com/20140113/8800276_184927469000_2.png",
        description: "这是一只草拟吗"
      },
      {
        name: "小马",
        category: "动物",
        price: "10000",
        amount: 3,
        imgurl: "http://pic37.nipic.com/20140113/8800276_184927469000_2.png",
        description: "这是一只草拟吗"
      },
      {
        name: "小马",
        category: "动物",
        price: "10000",
        amount: 3,
        imgurl: "http://pic37.nipic.com/20140113/8800276_184927469000_2.png",
        description: "这是一只草拟吗"
      }
    ]
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
        // this.setData({
        //   goodsList: res.data.result.goodsList
        // })
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