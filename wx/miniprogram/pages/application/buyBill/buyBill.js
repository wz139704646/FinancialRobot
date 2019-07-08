
Page({

  /**
   * 页面的初始数据
   */
  data: {
    date: '2018-12-25',
    type: 0
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

  },
  onClick(e){
    if(type==0){
      this.setData({
        type:1
      })
    }else{
      this.setData({
        type:0
      })
      
    }
  },

})