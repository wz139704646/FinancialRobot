var app = getApp()
const host = app.globalData.requestHost
const util = require('../../../utils/util.js')

const initPage = function (page) {
  let date = util.getcurDateFormatString(new Date())
  // 清除buyInfo缓存
  wx.removeStorage({
    key: 'buyInfo',
    success: function (res) {
      console.log('清理buyInfo缓存:')
      console.log(res)
    },
    fail: err => {
      console.log('清理buyInfo缓存失败:')
      console.error(err)
    }
  })
  // 设置日期属性
  page.setData({
    date: date
  })
}

Page({
  data: {
    date: '2019-07-10',
    type: "1",
    buyList: [],
    supplierId:0,
    id:""
  },

  onLoad: function(options) {
    initPage(this)
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
    try {
      wx.setStorageSync('buyInfo',
        {
          list: this.data.buyList,
          total: this.data.total
        })
    } catch (e) { console.error(e) }
    wx.navigateTo({
      url: '../chooseGood/chooseGood?back=buy',
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