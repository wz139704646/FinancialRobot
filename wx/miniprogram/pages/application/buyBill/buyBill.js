var app = getApp()
const host = app.globalData.requestHost
Page({
  data: {
    date: '2019-07-10',
    type: "1",
    buyList: [],
    supplierId:0,
    id:""
  },

  DateChange(e) {
    this.setData({
      date: e.detail.value
    })
  },
  addProvider(e) {
    wx.navigateTo({
      url: '../supplierList/supplierList?type=' + this.data.type,
    })
  },
  addGoods(e) {
    wx.navigateTo({
      url: '../chooseGood/chooseGood',
    })
  },
  onClick(e) {
    console.log(e)
    this.setData({
      type:e.detail.index + 1
    })
  },
  //生成采购单
  buyBill() {
    console.log(this.data)
    console.log("生成采购单")

    wx.request({
      url: 'http://' + host + '/addPurchase',
      data: JSON.stringify({
        companyId: "5",
        purchases: this.data.buyList,
        date: this.data.date,
        supplierId: this.data.supplierId
      }),
      method: "POST",
      header: {
        "Content-Type": 'application/json'
      },
      success: res => {
        console.log(res)
        wx.showToast({
          title: '已下单',
        })
      }
    })
  },
  cancelBill(){
    wx.redirectTo({
      url: '../home/home',
    })
  }
})