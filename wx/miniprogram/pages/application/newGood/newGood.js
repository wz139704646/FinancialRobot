
Page({

  /**
   * 页面的初始数据
   */
  data: {
    name:'',
    gindex: null,
    uindex: null,
    sindex: null,
    unitInfo: ['个', 'kg', '袋', '瓶', '箱'],
    type: ['食品类','服装类','鞋帽类','日用品类','家具类','家用电器类','纺织品类','五金电料类','厨具类'],
    store: ['仓库1','仓库2','仓库3'],
    sellprice: 0
  },
  nameChange(e) {
    console.log(e);
    this.setData({
      name: e.detail.value
    })
  },
  sellpriceChange(e) {
    //console.log(parseFloat(e.detail.value));
    //parseFloat(e.detail.value)
    //console.log(e.detail.value)
    this.setData({
      sellprice: e.detail.value
    })
  },
  unitChange(e) {
    console.log(e);
    this.setData({
      uindex: e.detail.value
    })
  },
  goodChange(e) {
    console.log(e);
    this.setData({
      gindex: e.detail.value
    })
  },
  storeChange(e) {
    console.log(e);
    this.setData({
      sindex: e.detail.value
    })
  },
  addsuccess(e){
    wx.request({
      url: 'http://127.0.0.1:5000/addGoods',
      data: JSON.stringify({
        companyId: "5",
        name: this.data.name,
        sellprice: this.data.sellprice,
        type: this.data.type[this.data.gindex],
        unitInfo: this.data.unitInfo[this.data.uindex],

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
  addfail(e){
    wx.showToast({
      title: 'add fail',
    })
  },
})