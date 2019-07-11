// pages/application/sellBill/sellBill.js
const app = getApp()
const util = require('../../../utils/util.js')
const host = app.globalData.requestHost

const initPage = function(page){
  let date = util.getcurDateFormatString(new Date())
  // 清除buyInfo缓存
  wx.removeStorage({
    key: 'buyInfo',
    success: function(res) {
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

  /**
   * 页面的初始数据
   */
  data: {
  },

  /**
   * 生命周期函数--监听页面加载
   */
  onLoad: function (options) {
    initPage(this)
  },

  /**
   * 生命周期函数--监听页面初次渲染完成
   */
  onReady: function () {

  },

  /**
   * 生命周期函数--监听页面显示
   */
  onShow: function () {

  },

  /**
   * 生命周期函数--监听页面隐藏
   */
  onHide: function () {

  },

  /**
   * 生命周期函数--监听页面卸载
   */
  onUnload: function () {

  },

  /**
   * 页面相关事件处理函数--监听用户下拉动作
   */
  onPullDownRefresh: function () {

  },

  /**
   * 页面上拉触底事件的处理函数
   */
  onReachBottom: function () {

  },

  /**
   * 用户点击右上角分享
   */
  onShareAppMessage: function () {

  },

  DateChange(e) {
    this.setData({
      date: e.detail.value
    })
  },

  addCustomer: function(e) {
    wx.navigateTo({
      url: '../customerList/customerList',
    })
  },

  addGoods: function(e) {
    // 缓存记录已买的商品
    try { 
      wx.setStorageSync('buyInfo', 
      {
        list: this.data.buyList,
        total: this.data.total
      })
    } catch(e) {console.error(e)}
    wx.navigateTo({
      url: '../chooseGood/chooseGood',
    })
  },

  submitBill: function(e) {
    let that = this
    wx.request({
      url: host+'/addSell',
      method: 'POST',
      header: {
        "Content-Type": 'application/json'
      },
      data: JSON.stringify({
        companyId: app.globalData.companyId,
        customerId: that.data.customer.id,
        date: that.data.date,
        sumprice: that.data.total,
        // goodsList: 
      }),
      success: res => {
        console.log(res)
      }
    })
  },

  cancelBill() {
    wx.redirectTo({
      url: '../home/home',
    })
  }
})