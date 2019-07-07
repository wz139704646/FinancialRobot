// pages/storageConsole/storageConsole.js

const app = getApp()
const util = require("../../utils/util.js")
const host = app.globalData.requestHost
const port = app.globalData.requestPort

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
    
  },

  divide2Sections: function(list) {
    let cl = []
    console.log(list)
    for(let i=0; i<list.length; i++) {
      if(cl.length == 0){
        cl = [{
          indexName: list[i].init,
          items: [list[i]]
        }]
      } else {
        if(cl[cl.length-1].indexName < list[i].init){
          cl.push({
            indexName: list[i].init,
            items: [list[i]]
          })
        } else{
          cl[cl.length-1].items.push(list[i])
        }
      }
    }
    return cl
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
        data: JSON.stringify({
          account: _this.data.account,
          type: 1
        }),
        method: 'POST',
        url: 'http://'+host+':'+port+'/getVerification',
        success(res) {
          console.log(res.data)
          if(!res.data.success){
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

  setCodeInput: function (e) {
    this.setData({
      messagecode: e.detail
    })
  },

  //获取验证码
  getVerificationCode() {
    this.getCode();
    var _this = this
  },
  //提交表单信息
  register: function () {
    let that = this
    let path = that.data.company
    var myreg = /^(14[0-9]|13[0-9]|15[0-9]|17[0-9]|18[0-9])\d{8}$/;
    if (!path) {
      wx.showToast({
        title: '公司不能为空',
        icon: 'none',
        duration: 1000
      })
      return false
    }
    else if (this.data.account == "") {
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
    if (this.data.messagecode == "") {
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
      let com = that.data.clist[path.section].items[path.row]
      let pwd = util.encryptPasswd(that.data.passwd)
      console.log(com)
      console.log({
        companyId: com.id,
        account: that.data.account,
        passwd: pwd,
        verification: that.data.messagecode
      })
      wx.request({
        url: 'http://'+host+':'+port+'/userRegister',
        data: JSON.stringify({
          companyId: com.id,
          account: that.data.account,
          passwd: pwd,
          verification: that.data.messagecode
        }),
        method: 'POST',
        header: {
          "Content-Type": 'application/json'
        },
        success: res => {
          let resp = res.data
          if(resp.success){
            app.globalData.companyId = com.id
            app.globalData.account = that.data.account
            wx.authorize({
              scope: 'scope.userInfo',
              success: () => {
                wx.getUserInfo({
                  success: rs => {
                    app.globalData.userInfo = rs.userInfo
                    wx.cloud.callFunction({
                      name: 'login',
                      data: {
                        cloudID: wx.cloud.CloudID(rs.cloudID)
                      }
                    }).then(suc => {
                      if (!suc.result.errMsg) {
                        app.globalData.openid = suc.result.openid
                        wx.request({
                          url: 'http://'+host+':'+port+'/bindUserWx',
                          method: 'POST',
                          header: {
                            "Content-Type": 'application/json'
                          },
                          success: rs => {
                            if (rs.data.success) {
                              wx.showToast({
                                title: '添加成功',
                                icon: 'success'
                              })
                            }
                          }
                        })
                      }
                    })
                  }
                })
              },
              complete: () => {
                wx.redirectTo({
                  url: '../index/index',
                })
              }
            })
          } else {
            wx.showToast({
              title: resp.errMsg,
              icon: 'none',
              duration: 1000
            })
          }
        },
        fail: err => {
          console.error(err)
          wx.showToast({
            title: '出现未知错误',
            icon: 'none',
            duration: 1000
          })
        }
      })
    }
  },

  selectCompany: function(e) {
    // console.log(e)
    let path = e.currentTarget.dataset
    console.log(typeof(path.section))
    console.log(typeof(path.row))
    this.setData({
      company: path
    })
    this.hideModal(e)
  },

  hideModal: function(e){
    this.setData({
      modalName: null
    }, res => {
      wx.hideToast()
    })
  },

  showModal(e) {
    let that = this
    wx.request({
      url: 'http://'+host+':'+port+'/query_Company',
      method: 'GET',
      success: res => {
        console.log(res)
        let coms = res.data.result
        wx.cloud.callFunction({
          name: 'convert2pinyin',
          data: {
            jsonStr: JSON.stringify(coms),
            options: {
              field: 'name',
              pinyin: 'pinyin',
              initial: 'init',
              ordered: 'asc'
            }
          }
        }).then( result => {
          console.log(result)
          let cl = that.divide2Sections(result.result)
          this.setData({
            clist: cl,
            sclist: cl
          }, _res => {
            wx.hideToast()
          })
        })
      }
    })
    this.setData({
      modalName: e.currentTarget.dataset.target
    })
    wx.showToast({
      title: '加载中',
      icon: 'loading',
      duration: 5000
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

  search: function(e) {
    let searchText = e.detail.value
    let slist = this.data.sclist
    let clist = []
    for(let i=0; i<slist.length; i++){
      let items = []
      for(let j=0; j<slist[i].items.length; j++){
        let name = slist[i].items[j].name
        let pinyin = slist[i].items[j].pinyin
        if ((name && name.indexOf(searchText) != -1)  || 
        (pinyin && pinyin.indexOf(searchText) != -1) ) {
          items.push(slist[i].items[j])
        }
      }
      if(items.length != 0){
        clist.push({
          indexName: slist[i].indexName,
          items: items
        })
      }
    }
    this.setData({
      clist: clist
    })
  }

})