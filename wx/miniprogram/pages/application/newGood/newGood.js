// pages/application/newGood/newGood.js
Page({

  /**
   * 页面的初始数据
   */
  data: {
    gindex: null,
    uindex: null,
    sindex: null,
    unit: ['个', 'kg', '袋', '瓶', '箱'],
    goodtype: ['食品类','服装类','鞋帽类','日用品类','家具类','家用电器类','纺织品类','五金电料类','厨具类'],
    store: ['仓库1','仓库2','仓库3']
  },
  unitChange(e) {
    console.log(e);
    this.setData({
      uindex: e.detail.value
    })
  },
  goodChange(e) {
    console.log(e);
    this.setData({
      gindex: e.detail.value
    })
  },
  storeChange(e) {
    console.log(e);
    this.setData({
      sindex: e.detail.value
    })
  },
  addsuccess(e){
    wx.showToast({
      title: 'add success',
    })
  },
  addfail(e){
    wx.showToast({
      title: 'add fail',
    })
  },
  /**
   * 用户点击右上角分享
   */
  onShareAppMessage: function () {

  }
})