const app = getApp()
const host = app.globalData.requestHost

Page({
  data: {
    PageCur: 'application'
  },

  // 页面加载函数
  onLoad: function(options) {
    // 获取用户信息，如果没有登录则转入登录页面
    let account = app.globalData.account
    console.log("onload")
    wx.showToast({
      title: '加载中',
      icon: 'loading',
      duration: 3000
    })
    wx.getSetting({
      success: res => {
        console.log("get setting suc")
        if (res.authSetting['scope.userInfo']) {
          wx.getUserInfo({
            success: res2 => {
              console.log('get userinfo suc')
              app.globalData.userInfo = res2.userInfo
              wx.cloud.callFunction({
                name: 'login',
                data: {
                  cloudID: wx.cloud.CloudID(res2.cloudID)
                }
              }).then(suc => {
                if (!suc.result.errMsg) {
                  app.globalData.openid = suc.result.openid
                  console.log('get openid suc')
                  wx.request({
                    url: host + '/queryUser',
                    method: 'POST',
                    header: {
                      "Content-Type": 'application/json'
                    },
                    data: JSON.stringify({
                      openid: suc.result.openid
                    }),
                    success: rs => {
                      console.log('query user suc')
                      console.log(rs)
                      if (!rs.data.success) {
                        if (account == undefined) {
                          wx.redirectTo({
                            url: '../login/login',
                            complete: () => {
                              wx.hideToast()
                            }
                          })
                        }
                      }
                    },
                    fail: err1 => {
                      if (account == undefined) {
                        wx.redirectTo({
                          url: '../login/login',
                          complete: () => {
                            wx.hideToast()
                          }
                        })
                      }
                    }
                  })
                }
              }).catch(err2 => {
                console.error(err2)
                if (account == undefined) {
                  wx.redirectTo({
                    url: '../login/login',
                    complete: () => {
                      wx.hideToast()
                    }
                  })
                }
              })
            },
            fail: err => {
              if (account == undefined) {
                wx.redirectTo({
                  url: '../login/login',
                  complete: () => {
                    wx.hideToast()
                  }
                })
              }
            }
          })
        } else {
          if (account == undefined) {
            wx.redirectTo({
              url: '../login/login',
              complete: () => {
                wx.hideToast()
              }
            })
          }
        }
      },
      fail: err3 => {
        if (account == undefined) {
          wx.redirectTo({
            url: '../login/login',
            complete: () => {
              wx.hideToast()
            }
          })
        }
      }
    })
  },

  NavChange(e) {
    console.log("navigate change")
    console.log(e)
    this.setData({
      PageCur: e.currentTarget.dataset.cur
    })
  },
  onShareAppMessage() {
    return {
      title: '财务机器人',
      imageUrl: '/images/share.jpg',
      path: '/pages/login/login'
    }
  },
  NavToTalk() {
    wx.navigateTo({
      url: '/pages/talk/talk',
    })
    console.log("navigate")
  }
})