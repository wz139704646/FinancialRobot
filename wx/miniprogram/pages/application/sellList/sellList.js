var app = getApp()
const host = app.globalData.requestHost
Page({

  /**
   * 页面的初始数据
   */
  data: {
    StatusBar: app.globalData.StatusBar,
    CustomBar: app.globalData.CustomBar,
    sellList: [
      {
        id: 111111,
        goodid: 1,
        goodsName: "aaa",
        number: 1,
        purchasePrice: 1,
        date: '2019-07-01',
        sumprice: 111,
        status: "运",
        index: 0,
        customerName: '黄家兴'
      }, {
        id: 111111,
        goodid: 1,
        supplierid: 1,
        goodsName: "aaa",
        number: 1,
        purchasePrice: 1,
        date: '2019-07-01',
        surname: "zjj",
        sumprice: 111,
        status: "到",
        index: 1,
        customerName: '戢启瑞'
      }
    ]
  },

  /**
   * 生命周期函数--监听页面加载
   */
  onLoad: function (options) {
    let that = this
    wx.request({
      url: host+'/querySell',
      header: {
        'Content-Type': 'application/json'
      },
      method: 'POST',
      data: JSON.stringify({
        companyId: app.globalData.companyId,
      }),
      success: res => {
        // 添加拼音属性
        console.log(res)
        let list = res.data.selList
        wx.cloud.callFunction({
          name: 'convert2pinyin',
          data: {
            jsonStr: JSON.stringify(list),
            field: 'goodsName',
            pinyin: 'pinyin'
          }
        }).then( res => {
          // 存储索引列表和所有列表
          let newlist = res.result
          for(let i in newlist){
            newlist[i]['index'] = i
          }
          that.setData({
            sellList: newlist,
            allList: newlist
          })
        }).catch(err => {
          console.error(err)
          wx.showToast({
            title: '商品信息出错',
            icon: 'none'
          })
        })
      },
      fail: err1 => {
        console.error(err1)
        wx.showToast({
          title: '加载失败',
          image: '../../../imgs/fail.png'
        })
      }
    })
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

  // 查看销售详情
  toDetail(e) {
    console.log(e)
    var index = e.currentTarget.dataset.index
    wx.navigateTo({
      url: '../recordInfo/recordInfo?type=sell'+'&id=' + this.data.allbrList[index].id
    })
  },

  search: function(e){
    let searchText = e.detail.value
    if(!searchText || !this.data.allList)
      return
    searchText = searchText.toLowerCase().split(' ').join('')
    timetext = searchText.split('-').join('')
    let slist = this.data.allList
    let sellList = []
    for(var i in slist){
      let gname = slist[i].goodsName
      let cname = slist[i].customerName
      let id = slist[i].id
      let date = slist[i].date.split('-').join('')
      if(gname.toLowerCase().indexOf(searchText)!=-1
      || cname.toLowerCase().indexOf(searchText)!=-1
      || id.indexOf(searchText)!=-1
      || date.indexOf(timetext)!=-1){
        sellList.push(slist[i])
      }
    }
    this.setData({
      sellList: sellList
    })
  }
})