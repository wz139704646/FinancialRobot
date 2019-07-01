// pages/application/newSupplier/newSupplier.js
Page({

  /**
   * 页面的初始数据
   */
  data: {

  },

  addsuccess(e) {
    wx.showToast({
      title: 'add success',
    })
  },
  addfail(e) {
    wx.showToast({
      title: 'add fail',
    })
  },
})