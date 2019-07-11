var app = getApp()
const host = app.globalData.requestHost
var inputVal = '';

Page({
  data: {
    //用于区分不同页面传来的值
    type:"0",
    StatusBar: app.globalData.StatusBar,
    CustomBar: app.globalData.CustomBar,
    hidden: true,
    supplierList: [],
    pysupplierList: [],
    pyallsupplierList: [],
  },

  getSupplierList() {
    var that = this
    wx.request({
      url: 'dddaaasdasdasd://' + host + '/queryByCompanyId',
      data: JSON.stringify({
        companyId: 5
      }),
      method: "POST",
      header: {
        "Content-Type": 'application/json'
      },
      success: res => {
        console.log(res)
        console.log(res.data.result)
        this.setData({
          supplierList: res.data.result
        })
        that.initSupplierList()
      }
    })
  },

  initSupplierList() {
    var that = this
    wx.cloud.callFunction({
      name: 'convert2pinyin',
      data: {
        jsonStr: JSON.stringify(this.data.supplierList),
        options: {
          field: 'name',
          pinyin: 'pinyin',
          initial: 'firstletter'
        }
      },
      success: res => {
        console.log('添加成功')
        console.log(res)
        this.setData({
          supplierList:res.result
        })
        that.initpysupplierList()
      },
      fail: err => {
        console.error('fail')
      }
    })
  },
  addElement() {
    for (let j = 0; j < 26; j++) {
      this.data.pysupplierList.push({
        first: String.fromCharCode(65 + j),
        sList: []
      })
    }
  },
  delElement() {
    //shanchu
    var k = 0
    for (let j = 0; j < 26 - k; j++) {
      if (this.data.pysupplierList[j].sList.length == 0) {
        this.data.pysupplierList.splice(j,1)
        j--
        k++
      }
    }
  },
  initpysupplierList() {
    var that = this
    that.addElement()
    
    for (let i = 0; i < this.data.supplierList.length; i++) {
      let j = this.data.supplierList[i].firstletter
      let k = j.charCodeAt(0)
      this.data.pysupplierList[k - 65].sList.push(this.data.supplierList[i])
    }
    console.log(this.data.pysupplierList)

    that.delElement()
    console.log(this.data.pysupplierList)
    this.setData({
      pysupplierList: this.data.pysupplierList,
      pyallsupplierList: this.data.pysupplierList,
      listCur: this.data.pysupplierList[0].first
    });
  },
  onLoad(options) {
    console.log(options)
    if (options.type != null) {
      this.setData({
        type: options.type
      })
    }
    this.getSupplierList()
  },
  onReady() {
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
  //获取文字信息
  getCur(e) {
    this.setData({
      hidden: false,
      listCur: this.data.pysupplierList[e.target.id].first,
    })
  },

  setCur(e) {
    this.setData({
      hidden: true,
      listCur: this.data.listCur
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
      this.setData({
        listCur: that.data.pysupplierList[num].first
      })
    };
  },

  //触发全部开始选择
  tStart() {
    this.setData({
      hidden: false
    })
  },

  //触发结束选择
  tEnd() {
    this.setData({
      hidden: true,
      listCurID: this.data.listCur
    })
    console.log(this.data.listCurID)
  },
  indexSelect(e) {
    let that = this;
    let barHeight = this.data.barHeight;
    let pysupplierList = this.data.pysupplierList;
    let scrollY = Math.ceil(list.length * e.detail.y / barHeight);
    for (let i = 0; i < list.length; i++) {
      if (scrollY < i + 1) {
        that.setData({
          listCur: pysupplierList[i].first,
          movableY: i * 20
        })
        return false
      }
    }
  },
  inputChange(e) {
    console.log(e.detail.value)
    inputVal = e.detail.value
  },
  search(e) {
    console.log("正在搜索")
    if (inputVal == "") {
      this.setData({
        pysupplierList: this.data.pyallsupplierList
      })
    } else {
      this.data.pysupplierList = []
      addElement()
      for (let i = 0; i < this.data.supplierList.length; i++) {
        let j = this.data.supplierList[i].pinyin
        let k = j.toUpperCase().charCodeAt(0)
        let l = this.data.supplierList[i].name
        if (j.indexOf(inputVal) != -1 || l.indexOf(inputVal) != -1) {
          this.data.pysupplierList[k - 65].sList.push(this.data.supplierList[i])
        }
      }
      delElement()
      console.log(this.data.pysupplierList)

      this.setData({
        pysupplierList: this.data.pysupplierList,
        listCur: this.data.pysupplierList[0].first
      });
    }
  },

  choose(e){
    //采购订单
    if (this.data.type == "1" || this.data.type == "2"){
      var pages = getCurrentPages();
      var currPage = pages[pages.length - 1];   //当前页面
      var prevPage = pages[pages.length - 2];  //上一个页面
      console.log(e)
      var id = e.currentTarget.dataset.id
      var name = e.currentTarget.dataset.name
      this.setData({
        id:id,
        name:name
      })
      //直接调用上一个页面对象的setData()方法，把数据存到上一个页面中去
      prevPage.setData({
        supplier: this.data.name,
        supplierId:this.data.id
      });

      wx.navigateBack({
        delta: 1
      })
    } 
  }

});