// pages/application/buyBill/buyBill.js
Page({

  /**
   * 页面的初始数据
   */
  data: {
    date: '2018-12-25',
  },
  DateChange(e) {
    this.setData({
      date: e.detail.value
    })
  },
  addProvider(e){
    wx.navigateTo({
      url: '../supplierList/supplierList',
    })
  },
  addGoods(e){

  },
  onClick(e){
    
  }
})