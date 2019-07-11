var app = getApp()
const host = app.globalData.requestHost
var name = ''
var phone = ''
var bankaccount = ''
var bankname = ''
var taxpayernumber = ''
var site = ''

Page({
  data: {
    type:["批发"]
  },

  addsuccess(e) {
    wx.request({
      url: 'http://' + host + '/addSupplier',
      data: JSON.stringify({
        companyId: "5",
        name: name,
        phone: phone,
        bankaccount: bankaccount,
        bankname: bankname,
        taxpayerNumber:taxpayernumber,
        site:site

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
      }
    })
  },
  addfail(e) {
    wx.redirectTo({
      url: '/pages/index/index',
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
  taxpayernumberChange(e) {
    console.log(e.detail.value)
    taxpayernumber = e.detail.value
  },
  siteChange(e) {
    console.log(e.detail.value)
    site = e.detail.value
  },
  typeChange(e) {
    this.setData({
      tindex: e.detail.value
    })

  },
})