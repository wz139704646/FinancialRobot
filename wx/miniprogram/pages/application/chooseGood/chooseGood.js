const app = getApp()
const host = app.globalData.requestHost
var inputVal = ""
Page({
  data: {
    StatusBar: app.globalData.StatusBar,
    CustomBar: app.globalData.CustomBar,
    goodsList:[],
    buyList:[],
    isInlist:false,
    badge:0,
    total:0,
    curPrice:0,
    curIndex:null,
    tempNum:null,
    curId:null,
    curName:null,

    
    searchList:[]
  },


  onLoad: function (options) {
    console.log("load")
    var that = this
    var goodsList = this.data.goodsList
    this.setData({
      host: host
    })
    that.initGoodList()
  },

  initGoodList() {
    var that = this
    wx.request({
      url: 'http://' + host + '/queryGoods',
      data: JSON.stringify({
        companyId: 5
      }),
      method: "POST",
      header: {
        "Content-Type": 'application/json'
      },
      success: res => {
        var goodsList = res.data.result.goodsList
        this.setData({
          goodsList:goodsList,
          allgoodsList:goodsList
        })
        that.initNum(goodsList)
      }
    })
  },

  initNum(goodsList){
    console.log(goodsList)
    
    for (var index in goodsList) {
      var buyParam = "goodsList[" + index + "].buyNum"
      var indexParam = "goodsList[" + index + "].index"
      this.setData({
        [buyParam]: 0,
        [indexParam]:index
      })
    }
    console.log(this.data.goodsList)
  },

  changeBuyNum(){
    var that = this
    var goodsList = this.data.goodsList
    var curIndex = this.data.curIndex
    //var total = this.data.total
    var curPrice = this.data.curPrice
    var tempNum = this.data.tempNum
    var badge = this.data.badge
    var isInlist = this.data.isInlist
    var buyList = this.data.buyList
    //total = total + curPrice * tempNum
    console.log(curIndex)
    goodsList[curIndex].buyNum = tempNum
    if(isInlist){
      if(tempNum == 0){
        //从数组取出
        badge = badge - 1
       
        var bindex = 0
        for (var index in buyList) {
          console.log(buyList[index]);
          console.log(index);
          if(buyList[index].id == this.data.curId){
            bindex = index
          }
        }
        console.log(bindex)
        buyList.splice(bindex, 1)
        //console.log("buylist"+buyList)
        //console.log(buyList)
      }
    }else{
      if(tempNum > 0){
        //添加到数组
        buyList.push({
          id:this.data.curId,
          name:this.data.curName,
          buyNum:this.data.tempNum,
          price:this.data.curPrice
        })
        badge = badge + 1
      }
    }
    this.setData({
      goodsList:goodsList,
      //total:total,
      badge:badge,
      buyList:buyList
    })
    that.calTotal()
    that.hideModal()
  },
  inputChange(e){
    this.setData({
      tempNum:e.detail.value
    })
    console.log(e.detail.value)
  },
  showModal(e) {
    var modelName = this.data.modalName
    console.log(e)
    this.setData({
      modalName: e.currentTarget.dataset.target,
      curIndex: e.currentTarget.id,
      tempNum:e.currentTarget.dataset.buynum,
      curPrice:e.currentTarget.dataset.price,
      curId:e.currentTarget.dataset.id,
      curName:e.currentTarget.dataset.name
    })
    if(e.currentTarget.dataset.buynum!=0){
      this.setData({
        isInlist:true
      })
    }else{
      this.setData({
        isInlist:false
      })
    }
  },
  hideModal(e) {
    this.setData({
      modalName: null
    })
  },
  //模态框显示买的东西的列表
  showBuyList(e){
    console.log(e)
    this.setData({
      modalName:e.currentTarget.dataset.target
    })
  },
  cancelGood(e){
    console.log(e)
    var that = this
    var index = e.currentTarget.id
    var buyList = this.data.buyList
    var goodid = buyList[index].id
    console.log(goodid)
    var goodsList = this.data.goodsList
    var allgoodsList = this.data.allgoodsList
    var badge = this.data.badge
    badge = badge - 1
    buyList.splice(index,1)
  
    var bindex = 0
    var cindex = 0
    for (var index in goodsList) {
      if (goodsList[index].id == goodid) {
        bindex = goodsList[index].index
        cindex = index
      }
    }
    console.log(bindex)
    console.log(cindex)
    goodsList[cindex].buyNum = 0
    allgoodsList[bindex].buyNum = 0
    this.setData({
      goodsList:goodsList,
      badge:badge,
      buyList:buyList,
      allgoodsList:allgoodsList
    })    
    console.log(goodsList)
    that.calTotal()
  },
  calTotal(){
    var buyList = this.data.buyList
    var total = 0
    for (var index in buyList) {
       total = total + buyList[index].buyNum * buyList[index].price
    }
    this.setData({
      total:total
    })
  },
  //选择完毕
  finishChoosing(e){
    var pages = getCurrentPages();
    var currPage = pages[pages.length - 1];   //当前页面
    var prevPage = pages[pages.length - 2];  //上一个页面
    
    //直接调用上一个页面对象的setData()方法，把数据存到上一个页面中去
    prevPage.setData({
      buyList:currPage.data.buyList,
      total:currPage.data.total
    });
    wx.navigateBack({
      delta: 1
    })
  },

  sInputChange(e){
    inputVal = e.detail.value
    console.log(inputVal)
    var that = this
    that.search()
  },

  search(e){
    var that = this
    console.log("正在搜索")
    this.setData({
      goodsList: this.data.allgoodsList
    })
    if (inputVal == "") {
      console.log("无操作")
    } else {
      console.log("有参数")
      this.data.searchList = []
      var j = 0
      for (var i = 0, len = this.data.goodsList.length; i < len; i++) {
        var name = this.data.goodsList[i].name
        if (name.indexOf(inputVal) != -1 ) {
          this.data.searchList.push(this.data.goodsList[i])
          console.log("is in")
        }
      }
      console.log("setdata")
      this.setData({
        goodsList: this.data.searchList
      });
    }
  }

})