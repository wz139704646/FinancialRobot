var app = getApp()
const util = require('../../utils/util.js')

Page({

  /**
   * 页面的初始数据
   */
  data: {
    passwd: "",
    account: "",
    accountError: "",
    passwdError: "",
    messagecode:"",
    state: true,
    loginText:"验证码登录"
  },

  /**
   * 生命周期函数
   * <view class="DrawerClose {{modalName=='viewModal'?'show':''}}" bindtap="hideModal">
			<text class="cuIcon-pullright"></text>
		</view>
		<scroll-view scroll-y class="DrawerWindow {{modalName=='viewModal'?'show':''}}">
			<view class="cu-list menu card-menu margin-top-xl margin-bottom-xl shadow-lg">
				<view class="cu-item arrow" wx:for="{{20}}" wx:key="index">
					<view class="content">
						<text class="cuIcon-github text-grey"></text>
						<text class="text-grey">{{index +1}}</text>
					</view>
				</view>
			</view>
		</scroll-view>
    
    <view class="DrawerClose {{modalName=='viewModal'?'show':''}}" bindtap="hideModal">
			<text class="cuIcon-pullright"></text>
		</view>
		<scroll-view scroll-y class="DrawerWindow {{modalName=='viewModal'?'show':''}}">
			<view class="cu-list menu card-menu margin-top-xl margin-bottom-xl shadow-lg">
				<view class="cu-item arrow" wx:for="{{20}}" wx:key="index">
					<view class="content">
						<text class="cuIcon-github text-grey"></text>
						<text class="text-grey">{{index +1}}</text>
					</view>
				</view>
			</view>
		</scroll-view>
    
    
    
    
    --监听页面加载
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
      title: '输入手机号',
      icon: "none"
    })
  },

  onAccoutChange: function(e){
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
    if(this.data.account == ""){
      this.setData({
        accountError: "未输入账号",
        passwdError: ""
      })
      return
    } else if(this.data.passwd == ""){
      this.setData({
        accountError: "",
        passwdError: "未输入密码"
      })
      return
    }

    let account = this.data.account
    let pwd = this.data.passwd
    // console.log('original text: '+pwd)
    console.log("account: "+account)
    let crypted = util.encryptPasswd(this.data.passwd)
    console.log("crypted pwd: " + crypted)

    wx.request({
      url: 'http://192.168.137.132:5000/login',
      data: JSON.stringify({
        account: account,
        passwd: crypted,
        type: 0
      }),
      method: "POST",
      header: {
        "Content-Type": 'application/json'
      },
      success: res => {
        console.log(res)
        wx.navigateTo({
          url: '../index/index',
        })
        // if(!res.data.flag){
        //   if(!res.data.account){
        //     this.setData({
        //       accountError: "账号错误",
        //       account: ""
        //     })
        //   } else {
        //     this.setData({
        //       nameError: "姓名错误",
        //       name: ""
        //     })
        //   }
        // } else {
        //   app.globalData.idnum = res.data.idnum
        //   app.globalData.name = this.data.name
        //   app.globalData.account = this.data.account
        //   if(res.data.leader) {
        //     wx.redirectTo({
        //       url: '../final/final'
        //     })
        //   } else {
        //     wx.switchTab({
        //       url: '../score/score',
        //     })
        //   }
        // }
      }
    })
  }

})