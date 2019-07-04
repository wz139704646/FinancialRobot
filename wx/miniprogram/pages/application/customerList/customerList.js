const app = getApp();
var inputVal = '';

Page({
  data: {
    StatusBar: app.globalData.StatusBar,
    CustomBar: app.globalData.CustomBar,
    hidden: true,
    customerList:[
      {
        name:'z',
        phone:'123345678',
        imgurl:'/imgs/app.png',
      }, {
        name: 'y',
        phone: '123345678',
        imgurl: '/imgs/app.png'
      }, {
        name: 'u',
        phone: '123345678',
        imgurl: '/imgs/app.png'
      }, {
        name: 'a',
        phone: '123345678',
        imgurl: '/imgs/app.png'
      }, {
        name: 'e',
        phone: '123345678',
        imgurl: '/imgs/app.png'
      }

    ],

    pycustomerList:[],

    pyallcustomerList:[],
  },

  getCustomerList(){
    var that = this
    wx.request({
      url: 'http://192.168.137.132:5000/queryAllCustomer',
      data: JSON.stringify({
        conpanyId:app.globalData.conpanyId
      }),
      method: "POST",
      header: {
        "Content-Type": 'application/json'
      },
      success: res => {
        console.log(res)
        console.log(res.customerList)
        this.setData({
          customerList:res.customerList
        })
        that.initCustomerList()
      }
    })
  },

  initCustomerList() {
    var that = this
    wx.cloud.callFunction({
      name: 'convert2pinyin',
      data: {
        jsonStr: JSON.stringify(this.data.customerList),
        options: {
          field: 'name',
          pinyin: 'pinyin',
          init:'firstletter'
        }
      },
      success: res => {
        console.log('添加成功')
        console.log(res)
        that.initpycustomerList()
      },
      fail: err => {
        console.error('fail')
      }
    })
  },

  initpycustomerList(){
    for (let j = 0; j < 26; j++) {
      this.data.pycustomerList.push({
        first: String.fromCharCode(65 + j),
        cList: []
      })
    }
    // console.log(this.data.pycustomerList)
    // console.log("A".charCodeAt(0))
    // console.log("a".toUpperCase())
    for (let i = 0; i < this.data.customerList.length - 1; i++) {
      let j = this.data.customerList[i].firstletter
      let k = j.charCodeAt(0)
      this.data.pycustomerList[k - 65].cList.push(this.data.customerList[i])
    }
    console.log(this.data.pycustomerList)
  },
  onLoad() {
    this.getCustomerList()
    this.setData({
      pycustomerList: this.data.pycustomerList,
      listCur: this.data.pycustomerList[0]
    });
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
      listCur: this.data.pycustomerList[e.target.id].first,
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
        listCur: that.data.pycustomerList[num].first
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
    let pycustomerList = this.data.pycustomerList;
    let scrollY = Math.ceil(list.length * e.detail.y / barHeight);
    for (let i = 0; i < list.length; i++) {
      if (scrollY < i + 1) {
        that.setData({
          listCur: pycustomerList[i],
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
    if(inputVal == ""){
      this.setData({
        pycustomerList:this.data.pyallcustomerList
      })
    }else{
      this.data.pycustomerList=[]
      for (let i = 0; i < this.data.customerList.length - 1; i++) {
        let j = this.data.customerList[i].pinyin
        let k = j.charCodeAt(0)
        if(j.search(inputVal) != -1){
          this.data.pycustomerList[k - 65].cList.push(this.data.customerList[i])
        }else{
          wx.showToast({
            title: '查询不到该客户信息',
          })
          this.setData({
            pycustomerList: this.data.pyallcustomerList
          })
        }
      }
      console.log(this.data.pycustomerList)
    }
  },
});