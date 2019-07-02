// pages/storageConsole/storageConsole.js

const app = getApp()

Page({

  data: {
    StatusBar: app.globalData.StatusBar,
    CustomBar: app.globalData.CustomBar,
    account:'',
    passwd:'',
    vpasswd:'',
    messagecode:'',
    indexToast: false,
    codename:'发送验证码',
    clist: [
      {
        indexName: 'A',
        items: [
          {
            id: 0,
            name: '123',
            address: 'hhhh'
          },
          {
            id: 4,
            name: '456',
            address: 'hhhh'
          }
        ]
      },
      {
        indexName: 'B',
        items: [
          {
            id: 1,
            name: '798',
            address: 'hhhh'
          }
        ]
      },
      {
        indexName: 'C',
        items: [
          {
            id: 2,
            name: '123',
            address: 'hhhh'
          }
        ]
      },
      {
        indexName: 'D',
        items: [
          {
            id: 2,
            name: '123',
            address: 'hhhh'
          }
        ]
      },
      {
        indexName: 'E',
        items: [
          {
            id: 2,
            name: '123',
            address: 'hhhh'
          }
        ]
      },
      {
        indexName: 'F',
        items: [
          {
            id: 2,
            name: '123',
            address: 'hhhh'
          }
        ]
      }
    ]
    
  },

  calScroll: function() {
    let that = this;
    wx.createSelectorQuery().select('.indexBar-box').boundingClientRect(function (res) {
      that.setData({
        boxTop: res.top
      })
    }).exec();
    wx.createSelectorQuery().select('.indexes').boundingClientRect(function (res) {
      that.setData({
        barTop: res.top
      })
    }).exec()
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

  selectCompany: function(e) {
    // console.log(e)
    let path = e.currentTarget.dataset
    this.setData({
      company: path
    })
    this.hideModal(e)
  },

  hideModal: function(e){
    this.setData({
      modalName: null
    })
  },

  showModal(e) {
    this.setData({
      modalName: e.currentTarget.dataset.target
    })
    this.calScroll()
    
  },

  //触发全部开始选择
  tStart() {
    this.setData({
      indexToast: true
    })
  },

  //触发结束选择
  tEnd() {
    let id = this.data.listCur
      
    this.setData({
      indexToast: false,
      listCurID: id
    })
  },

  //滑动选择Item
  tMove(e) {
    let y = e.touches[0].clientY,
      offsettop = this.data.boxTop,
      that = this;
    //判断选择区域,只有在选择区才会生效
    if (y > offsettop) {
      let num = parseInt((y - offsettop) / 20);
      console.log("num:"+num)
      this.setData({
        listCur: that.data.clist[num].indexName,
      })
    };
  },

  getCur(e) {
    let id = e.target.id
    this.setData({
      indexToast: true,
      listCur: this.data.clist[e.target.id].indexName,
    })
  },

  setCur(e) {
    this.setData({
      indexToast: false,
      listCur: this.data.listCur,
    })
  },

})