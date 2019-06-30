var app = getApp()

Page({

  /**
   * 页面的初始数据
   */
  data: {
    passwd: "",
    account: "",
    accountError: "",
    namepasswdError: "",
    messagecode:"",
    state: true,
    loginText:"验证码登录"
  },

  /**
   * 生命周期函数--监听页面加载
   */
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

  accountTip: function(e){
    wx.showToast({
      title: '输入代表队账号',
      icon: "none"
    })
  },

  onAccoutChange: function(e){
    // console.log(e)
    this.setData({
      account: e.detail
    })
  },

  onNameChange: function (e) {
    // console.log(e)
    this.setData({
      name: e.detail
    })
  },

  register:function(e){
    wx.navigateTo({
      url: '../register/register'
    })
  },

  changeState:function(e){
    console.log("change state")
    if (this.data.state) {
      this.setData({
        loginText: "密码登录",
        state:false
      })
    } else {
      this.setData({
        loginText: "验证码登录",
        state:true
      })
    }
    
  },  

  login: function(e){
    console.log(e)

    wx.navigateTo({
      url: '../index/index',
    })

  //   if(this.data.account == ""){
  //     this.setData({
  //       accountError: "未输入账号"
  //     })
  //     return
  //   } else if(this.data.passwd == ""){
  //     this.setData({
  //       nameError: "未输入密码"
  //     })
  //     return
  //   }

  //   wx.request({
  //     url: app.globalData.loginUrl,
  //     data:{
  //       account: this.data.account,
  //       name: this.data.passwd
  //     },
  //     method: "POST",
  //     header: {
  //       "Content-Type": 'application/x-www-form-urlencoded'
  //     },
  //     success: res => {
  //       console.log(res)
  //       if(!res.data.flag){
  //         if(!res.data.account){
  //           this.setData({
  //             accountError: "账号错误",
  //             account: ""
  //           })
  //         } else {
  //           this.setData({
  //             nameError: "姓名错误",
  //             name: ""
  //           })
  //         }
  //       } else {
  //         app.globalData.idnum = res.data.idnum
  //         app.globalData.name = this.data.name
  //         app.globalData.account = this.data.account
  //         if(res.data.leader) {
  //           wx.redirectTo({
  //             url: '../final/final'
  //           })
  //         } else {
  //           wx.switchTab({
  //             url: '../score/score',
  //           })
  //         }
  //       }
  //     }
  //   })
  }

})