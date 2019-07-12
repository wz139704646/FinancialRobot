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
    if(!options.id || !options.back){
      wx.showToast({
        title: '获取订单信息失败！',
        icon: 'none'
      })
      return
    }
    this.setData({
      id:options.id,
      back: options.back,
      fun: options.fun
    })
    that.initInfo(options)
  },

  initInfo(e){
    var that = this
    var id = e.id
    var back = e.back 
    // 根据返回页面获取请求不同的api
    let api = back == 'sell' ? '/querySellById' : '/queryPurchaseById'
    wx.request({
      url: host + api,
      data: JSON.stringify({
        companyId: "5",
        id: id
      }),
      method: "POST",
      header: {
        "Content-Type": 'application/json'
      },
      success(res) {
        console.log(res)
        let data = res.data
        let back = that.data.back
        let list = []
        // 处理返回的同一订单的商品信息列表
        // 购货单
        if(back == 'buy'){
          list = data.result
          if(list && list.length>0){
            list[0].date = date.toString().substring(0, 10)
          } else {
            wx.showToast({
              title: '订单号错误',
              image: '../../../imgs/fail.png'
            })
            return
          }
        }
        // 销货单
        else if(back == 'sell') {
          list = data.selList
          if(list && list.length>0) {
            list[0].date = date.toString().substring(0, 10)
          } else {
            wx.showToast({
              title: '订单号错误',
              image: '../../../imgs/fail.png'
            })
            return 
          }
        } else {
          wx.showToast({
            title: '出现未知错误',
            image: '../../../imgs/fail.png'
          })
          return 
        }
        that.setData({
          buyList: list
        })
        that.calTotal(list, back)
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
  calTotal(list, back) {
    var total = 0
    if(back == 'buy') {
      for (var index in buyList) {
        total = total + list[index].number * list[index].purchasePrice
      }
    } else {
      for(var index in buyList) {
        total += list[index].sumprice
      }
    }
    this.setData({
      total: total
    })
  },
  //确认入库
  buyArrived(){

  },
  //确认出库
  sellOut(){

  }

})