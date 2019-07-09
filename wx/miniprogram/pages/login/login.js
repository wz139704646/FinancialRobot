var app = getApp()
const util = require('../../utils/util.js')
const host = app.globalData.requestHost

Page({
  data: {
    passwd: "",
    account: "",
    accountError: "",
    passwdError: "",
    messagecode: "",
    state: true,
    loginText: "验证码登录",
    disabled: false,
  },

  onLoad: function (options) {
    // wx.showToast({
    //   title: '加载中',
    //   icon:'loading',
    //   duration: 3000
    // })
    // wx.getSetting({
    //   success: res => {
    //     if(res.authSetting['scope.userInfo']) {
    //       wx.getUserInfo({
    //         success: res => {
    //           app.globalData.userInfo = res.userInfo
    //           wx.cloud.callFunction({
    //             name: 'login',
    //             data: {
    //               cloudID: wx.cloud.CloudID(res.cloudID)
    //             }
    //           }).then(suc => {
    //             if(!suc.result.errMsg){
    //               app.globalData.openid = suc.result.openid
    //               wx.request({
    //                 url: 'http://'+host+'/queryUser',
    //                 method: 'POST',
    //                 header: {
    //                   "Content-Type": 'application/json'
    //                 },
    //                 data: JSON.stringify({
    //                   openid: suc.result.openid
    //                 }),
    //                 success: rs => {
    //                   console.log(rs)
    //                   if(rs.data.success){
    //                     wx.redirectTo({
    //                       url: '../index/index',
    //                       complete: ()=>{
    //                         wx.hideToast()
    //                       }
    //                     })
    //                   }
    //                 }
    //               })
    //             }
    //           })
    //         },
    //         fail: err => {
    //           wx.hideToast()
    //         }
    //       })
    //     }
    //   }
    // })  
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

  // 输入验证码时
  setCode: function(e){
    this.setData({
      messagecode: e.detail
    })
  },

  // 发送验证码
  sendCode: function(e){
    var _this = this;
    var myreg = /^(14[0-9]|13[0-9]|15[0-9]|17[0-9]|18[0-9])\d{8}$$/;
    if (this.data.account == "") {
      wx.showToast({
        title: '手机号不能为空',
        icon: 'none',
        duration: 1000
      })
      return false;
    } else if (!myreg.test(this.data.account)) {
      wx.showToast({
        title: '请输入正确的手机号',
        icon: 'none',
        duration: 1000
      })
      return false;
    } else {
      wx.request({
        data: JSON.stringify({
          account: _this.data.account,
          type: 0
        }),
        method: 'POST',
        url: 'http://' + host + '/getVerification',
        success(res) {
          console.log(res.data)
          if (!res.data.success) {
            wx.showToast({
              title: res.data.errMsg,
              icon: 'none',
              duration: 1000
            })
            return
          }
          _this.setData({
            iscode: res.data.result.code,
            disabled: true
          })
          var num = 61;
          var timer = setInterval(function () {
            num--;
            if (num <= 0) {
              clearInterval(timer);
              _this.setData({
                codename: '重新发送',
                disabled: false
              })

            } else {
              _this.setData({
                codename: num + "s"
              })
            }
          }, 1000)
        }
      })

    }
  },


  login: function (e) {
    let state = this.data.state
    var myreg = /^(14[0-9]|13[0-9]|15[0-9]|17[0-9]|18[0-9])\d{8}$/;
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
          passwdError: "未输入密码",
          codeError: ''
        })
        return
      } else {
        this.setData({
          accountError: "",
          codeError: "未输入短信验证码",
          passwdError: ''
        })
        return
      }
    } else if (!myreg.test(this.data.account)){
      this.setData({
        accountError: '手机号错误',
        passwdError: '',
        codeError: ''
      })
    }

    let account = this.data.account
    let pwd = state ? this.data.passwd : this.data.messagecode
    // console.log('original text: '+pwd)
    // console.log("account: " + account)
    if(state){
      pwd = util.encryptPasswd(this.data.passwd)
    }
    // console.log("crypted pwd: " + crypted)
    wx.request({
      url: 'http://'+host+'/login',
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
          return 
        } else{
          app.globalData.companyId = res.data.companyId
          app.globalData.position = res.data.position
          app.globalData.account = account
          wx.authorize({
            scope: 'scope.userInfo',
            success: () => {
              wx.showLoading({
                title: '加载中',
                mask: true
              })
              wx.getUserInfo({
                success: resu => {
                  app.globalData.userInfo = resu.userInfo
                  wx.cloud.callFunction({
                    name: 'login',
                    data: {
                      cloudID: wx.cloud.CloudID(resu.cloudID)
                    }
                  }).then(suc => {
                    wx.showToast({
                      title: '登录中',
                      icon: 'loading',
                      duration: 1000
                    })
                    if (!suc.result.errMsg) {
                      app.globalData.openid = suc.result.openid
                      wx.request({
                        url: 'http://'+host+'/bindUserWx',
                        method: 'POST',
                        header: {
                          "Content-Type": 'application/json'
                        },
                        data: JSON.stringify({
                          account: account,
                          openid: suc.result.openid
                        }),
                        success: rs => {
                          if (rs.data.success) {
                            wx.hideLoading()
                            wx.showToast({
                              title: '添加成功',
                              icon: 'success',
                              duration: 1000
                            })
                          }
                        }
                      })
                    }
                  })
                }
              })
            },
            fail: () => {
              wx.showLoading({
                title: '加载中',
                mask: true
              })
            },
            complete: () => {
              wx.redirectTo({
                url: '../index/index',
                complete: ()=>{
                  wx.hideLoading()
                }
              })
            }
          })
        }
        
      }
    })
  }

})