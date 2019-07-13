// miniprogram/pages/finding/home/home.js
Page({

  /**
   * 页面的初始数据
   */
  data: {
    statis: [
      {
        title: '利润趋势分析',
        showMonth: false,
        showPeriod: true,
        period: [
          {
            title: '本日'
          },
          {
            title: '本月'
          },
          {
            title: '本年'
          }
        ],
        showIdx: 0
      },
      {
        title: '资产增长分析',
        showMonth: true,
        showPeriod: false
      }
    ]
  },

  /**
   * 生命周期函数--监听页面加载
   */
  onLoad: function (options) {

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

  chooseDayOrMonth: function(e) {
    // console.log(e)
    // console.log(this.data.statis)
    let stat = e.currentTarget.dataset.stat
    let per = e.currentTarget.dataset.per
    let statis = this.data.statis
    statis[stat].showIdx = per 
    this.setData({
      statis: statis
    })
  }
})