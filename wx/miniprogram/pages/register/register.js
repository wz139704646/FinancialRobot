// pages/storageConsole/storageConsole.js

const app = getApp()

Page({

  data: {
    account:'',
    passwd:'',
    vpasswd:'',
    messagecode:'',
    codename:'发送验证码'
    
  },

  accountTip: function (e) {
    wx.showToast({
      title: '输入手机号',
      icon: "none"
    })
  },

  //获取input输入框的值
  getAccountValue: function (e) {
    this.setData({
      account: e.detail
    })
    //console.log(e)
    //console.log(this.data.account)
  },
  getPasswdValue: function (e) {
    this.setData({
      passwd: e.detail
    })
    //console.log(this.data.passwd)
  },
  getVpasswdValue: function (e) {
    this.setData({
      vpasswd: e.detail
    })
    //console.log(this.data.vpasswd)
  },
  getMessagecodeValue: function (e) {
    this.setData({
      messagecode: e.detail.value
    })
    //console.log(this.data.messagecode)
  },
  getCode: function () {
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
        data: {},
        //'url': 接口地址,
        success(res) {
          console.log(res.data.data)
          _this.setData({
            iscode: res.data.data
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
  //获取验证码
  getVerificationCode() {
    this.getCode();
    var _this = this
    _this.setData({
      disabled: true
    })
  },
  //提交表单信息
  register: function () {
    var myreg = /^(14[0-9]|13[0-9]|15[0-9]|17[0-9]|18[0-9])\d{8}$/;
    if (this.data.account == "") {
      wx.showToast({
        title: '手机号不能为空',
        icon: 'none',
        duration: 1000
      })
      return false;
    }
    if (this.data.passwd == "") {
      wx.showToast({
        title: '密码不能为空',
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
    } else if (this.data.passwd != this.data.vpasswd){
      wx.showToast({
        title: '确认密码与密码内容不一致',
        icon: 'none',
        duration: 1000
      })
      return false;
    }
    if (this.data.code == "") {
      wx.showToast({
        title: '验证码不能为空',
        icon: 'none',
        duration: 1000
      })
      return false;
    } else if (this.data.code != this.data.iscode) {
      wx.showToast({
        title: '验证码错误',
        icon: 'none',
        duration: 1000
      })
      return false;
    } else {
      // wx.setStorageSync('account', this.data.account);
      // wx.setStorageSync('passwd', this.data.passwd);
      // wx.redirectTo({
      //   url: '../add/add',
      // })
    }
  },

})