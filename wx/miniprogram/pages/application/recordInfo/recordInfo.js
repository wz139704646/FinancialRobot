const app = getApp()
const host = app.globalData.requestHost
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
    var that = this 
    console.log(options)
    this.setData({
      id:options.id
    })
    that.initInfo(options)
  },

  initInfo(e){
    var that = this
    wx.request({
      url: 'http://' + host + '/queryPurchase',
      data: JSON.stringify({
        companyId: "5",
        id: e.id
      }),
      method: "POST",
      header: {
        "Content-Type": 'application/json'
      },
      success(res) {
        console.log(res)
        var date = res.data.result[0].date
        res.data.result[0].date = date.toString().substring(0,10) 
        console.log(date)
        that.setData({
          buyList: res.data.result
        })
        that.calTotal(res)
      },
      
    })
  },

  delBill(e){
    wx.request({
      url: 'http://' + host + '/delBuy',
      data: JSON.stringify({
        companyId: "5",
        id:this.data.id

      }),
      method: "POST",
      header: {
        "Content-Type": 'application/json'
      },
      success: res => {
        console.log(res)
        wx.showToast({
          title: '订单已删除',
          duration:4000
        })
        var pages = getCurrentPages();
        var currPage = pages[pages.length - 1];   //当前页面
        var prevPage = pages[pages.length - 2];  //上一个页面

        //直接调用上一个页面对象的setData()方法，把数据存到上一个页面中去
        prevPage.setData({
          brList: res.data.result.brList
        });
        wx.navigateBack({
          delta: 1
        })
      },
      fail:res=>{
        console.log("删除失败")
      }
    })
  },
  backToList(e){
    console.log(e)
    wx.navigateBack({
      delta:1
    })
  },
  calTotal(e) {
    console.log(e.data.result)
    var buyList = e.data.result
    var total = 0
    for (var index in buyList) {
      total = total + buyList[index].number * buyList[index].purchasePrice
    }
    this.setData({
      total: total
    })
  },

})