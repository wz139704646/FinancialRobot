var app = getApp()
const host = app.globalData.requestHost
Page({
  data: {
    date: '2019-07-10',
    listdate:'2019-07-10',
    type: "1",
    buyList: [],
    supplierId:0,
    id:"",
    brList:[]
  },
  onLoad(options){
    // if(options.data.type == 2){
    //   this.setData({
    //     type:2,
    //     id:options.data.id
    //   })
    // }
  },
  DateChange(e) {
    this.setData({
      date: e.detail.value
    })
  },
  addProvider(e) {
    wx.navigateTo({
      url: '../supplierList/supplierList?type=' + this.data.type,
    })
  },
  addGoods(e) {
    wx.navigateTo({
      url: '../chooseGood/chooseGood',
    })
  },
  onClick(e) {
    console.log(e)
    this.setData({
      type:e.detail.index + 1
    })
  },
  inputChange(e) {
    var that = this
    console.log(e.detail.value)
    this.setData({
      id:e.detail.value
    })
    that.searchid()
  },
  //生成采购单
  buyBill() {
    console.log(this.data)
    console.log("生成采购单")

    wx.request({
      url: 'http://' + host + '/addPurchase',
      data: JSON.stringify({
        companyId: "5",
        buyList: this.data.buyList,
        date: this.data.date,
        supplierId: this.data.supplierId
      }),
      method: "POST",
      header: {
        "Content-Type": 'application/json'
      },
      success: res => {
        console.log(res)
        wx.showToast({
          title: '已下单',
        })
      }
    })
  },
  searchid(){
    wx.request({
      url: 'http://' + host + '/queryPurchase',
      data: JSON.stringify({
        companyId: "5"
      }),
      success(res) {
        console.log(res) 
        var brList = res.data.result.brList
        this.setData({
          brList: brList
        })
        var brgoodList = []
        var lid = brList[0].id
        var j=0
        for(var i = 0,len=brList.length;i<len;i++){
          for(var j=0;j<brgoodList.length;j++){
            if(brList[i].id==brgoodList[j].id){
              
            }
          }
        }
      }
    })
  },
  listDateChange(e) {
    this.setData({
      listdate: e.detail.value
    })
  },


})