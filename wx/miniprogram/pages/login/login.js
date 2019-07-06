var app = getApp()
const util = require('../../utils/util.js')

Page({
  data: {
    passwd: "",
    account: "",
    accountError: "",
    passwdError: "",
    messagecode: "",
    state: true,
    loginText: "验证码登录"
  },

  onLoad: function (options) {
    console.log()
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

  accountTip: function (e) {
    wx.showToast({
      title: '输入手机号',
      icon: "none"
    })
  },

  onAccoutChange: function (e) {
    // console.log(e)
    this.setData({
      account: e.detail
    })
  },

  onPwdChange: function (e) {
    // console.log(e)
    this.setData({
      passwd: e.detail
    })
  },

  register: function (e) {
    wx.navigateTo({
      url: '../register/register'
    })
  },

  changeState: function (e) {
    console.log("change state")
    if (this.data.state) {
      this.setData({
        loginText: "密码登录",
        state: false
      })
    } else {
      this.setData({
        loginText: "验证码登录",
        state: true
      })
    }

  },

  login: function (e) {
    let state = this.data.state
    if (this.data.account == "") {
      this.setData({
        accountError: "未输入账号",
        passwdError: ""
      })
      return
    } else if ((state && this.data.passwd == "") ||
      (!state && this.data.messagecode == "")) {
      if (state) {
        this.setData({
          accountError: "",
          passwdError: "未输入密码"
        })
        return
      } else {
        this.setData({
          accountError: "",
          codeError: "未输入短信验证码"
        })
        return
      }
    }

    let account = this.data.account
    let pwd = state ? this.data.passwd : this.data.messagecode
    // console.log('original text: '+pwd)
    // console.log("account: " + account)
    pwd = util.encryptPasswd(this.data.passwd)
    // console.log("crypted pwd: " + crypted)

    wx.request({
      url: 'http://127.0.0.1:5000/login',
      data: JSON.stringify({
        account: account,
        passwd: pwd,
        type: 0
      }),
      method: "POST",
      header: {
        "Content-Type": 'application/json'
      },
      success: res => {
        console.log(res)
        let succ = res.data.success
        if(!succ){
          wx.showToast({
            title: res.data.errMsg,
            icon: 'none'
          })
          this.setData({
            accountError: "",
            passwdError: "",
            codeError: ""
          })
        } else{
          app.globalData.companyId = res.data.companyId
          app.globalData.position = res.data.position
          wx.redirectTo({
            url: '../index/index',
          })
        }
        
      }
    })
  }

})