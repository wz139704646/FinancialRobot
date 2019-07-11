const app = getApp()
var inputVal = '';
const host = app.globalData.requestHost
Page({
  data: {
    StatusBar: app.globalData.StatusBar,
    CustomBar: app.globalData.CustomBar,
    brList:[],
    allbrList:[],
    searchList:[]
  },
  onLoad(options){
    var that = this
    that.getbrList()
  },
  getbrList(){
    var that = this
    wx.request({
      url: 'http://' + host + '/queryPurchase',
      data: JSON.stringify({
        companyId: "5"
      }),
      method: "POST",
      header: {
        "Content-Type": 'application/json'
      },
      success(res){
        console.log(res)
        that.setData({
          brList:res.data.result
        })
        that.initbrList()
      }
    })
  },
  initbrList() {
    var that = this
    wx.cloud.callFunction({
      name: 'convert2pinyin',
      data: {
        jsonStr: JSON.stringify(this.data.brList),
        options: {
          field: 'goodName',
          pinyin: 'pinyin',
        }
      },
      success: res => {
        console.log('添加成功')
        console.log(res)
        this.setData({
          brList: res.result
        })
        that.initIndex()
      },
      fail: err => {
        console.error('fail')
      }
    })
  },
  initIndex(){
    for (var index in this.data.brList) {
      var indexParam = "brList[" + index + "].index"
      this.setData({
        [indexParam]: index
      })
    }
    this.setData({
      brList:this.data.brList,
      allbrList:this.data.brList
    })
  },
  inputChange(e) {
    var that = this
    console.log(e.detail.value)
    inputVal = e.detail.value
    that.search()
  },
  search() {
    var that = this
    console.log("正在搜索")
    this.setData({
      brList: this.data.allbrList
    })
    if (inputVal == "") {
      console.log("无操作")
    } else {
      this.data.searchList = []
      for (let i = 0, len = this.data.brList.length; i < len; i++) {
        let j = this.data.brList[i].pinyin
        let l = this.data.brList[i].date
        if (j.indexOf(inputVal) != -1 || l.indexOf(inputVal) != -1) {
          this.data.searchList.push(this.data.brList[i])
        }
      }

      this.setData({
        brList: this.data.searchList
      });
    }
  },
  toDetail(e){
    console.log(this.data)
    console.log(e)
    var index = e.currentTarget.dataset.index
    wx.navigateTo({
      url: '../recordInfo/recordInfo?id='+this.data.allbrList[index].id
    })
  }
})