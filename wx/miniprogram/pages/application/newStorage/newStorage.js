const app = getApp()
const host = app.globalData.requestHost
var name = ''
var phone = ''
Page({

  /**
   * 页面的初始数据
   */
  data: {

  },
  //输入值改变
  nameChange(e) {
    console.log(e.detail.value)
    name = e.detail.value
  },
  siteChange(e) {
    console.log(e.detail.value)
    site = e.detail.value
  },
  //确认添加
  addsuccess(e) {
    wx.request({
      url: 'http://' + host + '/addWarehouse',
      data: JSON.stringify({
        companyId: "5",
        name: name,
        site: site
      }),
      method: "POST",
      header: {
        "Content-Type": 'application/json'
      },
      success: res => {
        wx.showToast({
          title: 'add success',
          duration:4000
        })
        console.log(res)
        wx.redirectTo({
          url: '/pages/index/index',
        })
      }
    })
  },
  //取消添加
  addfail(e) {
    wx.redirectTo({
      url: '/pages/index/index',
    })
  },
})