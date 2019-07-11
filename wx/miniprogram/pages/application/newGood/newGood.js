var app = getApp()
const host = app.globalData.requestHost
Page({

  /**
   * 页面的初始数据
   */
  data: {
    barcode:"",
    count:"",
    imageList: [],
    name:'',
    gindex: 0,
    uindex: 0,
    sindex: 0,
    unitInfo: ['个', 'kg', '袋', '瓶', '箱'],
    type: ['食品类','服装类','鞋帽类','日用品类','家具类','家用电器类','纺织品类','五金电料类','厨具类'],
    store: ['仓库1','仓库2','仓库3'],
    sellprice: '',
    standard: '',
    brand: ''
  },
  nameChange(e) {
    console.log(e);
    this.setData({
      name: e.detail.value
    })
  },
  sellpriceChange(e) {
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
  barcodeChange(e){
    console.log(e);
    this.setData({
      barcode: e.detail.value
    })
  },
  storeChange(e) {
    console.log(e);
    this.setData({
      sindex: e.detail.value
    })
  },
  addsuccess(e){
    var that = this
    wx.request({
      url: 'http://' + host + '/addGoods',
      data: JSON.stringify({
        companyId: "5",
        name: this.data.name,
        sellprice: this.data.sellprice,
        type: this.data.type[this.data.gindex],
        unitInfo: this.data.unitInfo[this.data.uindex],
        barcode:this.data.barcode
        
      }),
      method: "POST",
      header: {
        "Content-Type": 'application/json'
      },
      success: res => {
        wx.showToast({
          title: 'add success',
        })
        console.log(res.data)
      }
    })

  },
  addfail(e){
    wx.redirectTo({
      url: '/pages/index/index',
    })
  },
  chooseImage: function (event) {
    let that = this
    wx.chooseImage({
      count: 1,
      sizeType: ['original', 'compressed'],
      sourceType: ['album', 'camera'],
      success: res => {
        const tempFilePaths = res.tempFilePaths
        this.setData({
          imageList: tempFilePaths
        })
        console.log(res)
      },
      fail: err => {
        console.error(err)
      }
    })
  },
  previewImage: function (e) {
    var current = e.target.dataset.src
    wx.previewImage({
      current: current,
      urls: this.data.imageList
    })
  },
  upload(e){
    console.log(e.data.result.id)
    wx.uploadFile({
      url: 'http://' + host + '/pic/upload',
      filePath: this.data.imageList[0],
      name: 'goods',
      formData:{
        id:e.data.result.id
      },
      success: result => {
        console.log(result)
      }
    })
  },
  scanCode: function (event) {
    let that = this
    wx.scanCode({
      success: res => {
        // console.log(typeof(res.result))
        // 查询商品信息
        wx.request({
          url: 'http://www.mxnzp.com/api/barcode/goods/details?barcode='+res.result,
          method: 'GET',
          success: resu => {
            let info = resu.data
            console.log(info)
            // 成功返回信息
            if(info.code == 1){
              that.setData({
                name: info.data.goodsName,
                barcode: info.data.barcode,
                sellprice: info.data.price,
                standard: info.data.standard,
                brand: info.data.brand
              })
            } else if(info.code == 0){
              that.setData({
                barcode: res.result
              })
            }
          },
          fail: err => {
            console.error(err)
            that.setData({
              barcode: res.result
            })
          }
        })
      },
      fail: err1 => {
        console.error(err1)
      }
    })
  }
})