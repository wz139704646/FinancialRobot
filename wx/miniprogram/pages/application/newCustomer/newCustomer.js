// pages/application/newCustomer/newCustomer.js
var name = ''
var phone = ''
var bankaccount = ''
var bankname = ''
var ntype = ''
var nrange = ''
var tindex = null
var rindex = null
Page({

  /**
   * 页面的初始数据
   */
  data: {

    type: [1, 2, 3],
    range: [1, 2, 3]
  },
  typeChange(e) {
    this.setData({
      tindex: e.detail.value
    })

  },
  rangeChange(e) {
    this.setData({
      rindex: e.detail.value
    })
  },
  addsuccess(e) {

    wx.request({
      url: 'http://127.0.0.1:5000/addCustomer',
      data: JSON.stringify({
        companyId: 5,
        name: name,
        phone: phone,
        bankAccount: bankaccount,
        bankname: bankname
      }),
      method: "POST",
      header: {
        "Content-Type": 'application/json'
      },
      success: res => {
        wx.showToast({
          title: 'add success',
        })
        console.log(res)
      },
      fail:res => {
        console.log(res)
      }
    })
  },
  addcancel(e) {
    wx.showToast({
      title: 'add cancel',
    })
    wx.redirectTo({
      url: '/pages/application/home/home',
    })
  },
  nameChange(e) {
    console.log(e.detail.value)
    name = e.detail.value
  },
  phoneChange(e) {
    console.log(e.detail.value)
    phone = e.detail.value
  },
  bankaccountChange(e) {
    console.log(e.detail.value)
    bankaccount = e.detail.value
  },
  banknameChange(e) {
    console.log(e.detail.value)
    bankname = e.detail.value
  },
})