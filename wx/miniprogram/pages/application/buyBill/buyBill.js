
Page({

  /**
   * 页面的初始数据
   */
  data: {
    date: '2018-12-25',
    type: "1",
    buyList:[],

  },
  DateChange(e) {
    this.setData({
      date: e.detail.value
    })
  },
  addProvider(e){
    wx.navigateTo({
      url: '../supplierList/supplierList?type=' + this.data.type,
    })
  },
  addGoods(e){
    wx.navigateTo({
      url: '../chooseGood/chooseGood',
    })
  },
  onClick(e){
    if(this.data.type=="1"){
      this.setData({
        type:"2"
      })
    }else{
      this.setData({
        type:"1"
      })
      
    }
  },

})