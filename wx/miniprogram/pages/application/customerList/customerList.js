const app = getApp();
var inputVal = '';

Page({
  data: {
    StatusBar: app.globalData.StatusBar,
    CustomBar: app.globalData.CustomBar,
    hidden: true,
    customerList:[
      

    ],

    pycustomerList:[],

    pyallcustomerList:[],
  },

  getCustomerList(){
    var that = this
    wx.request({
      url: 'http://127.0.0.1:5000/queryAllCustomer',
      data: JSON.stringify({
        companyId:"5"
      }),
      method: "POST",
      header: {
        "Content-Type": 'application/json'
      },
      success: res => {
        console.log(res)
        console.log(res.data.result)
        this.setData({
          customerList:res.data.result
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
          initial:'firstletter'
        }
      },
      success: res => {
        console.log('添加成功')
        console.log(res)
        this.setData({
          customerList:res.result
        })
        that.initpycustomerList()
      },
      fail: err => {
        console.error('fail')
      }
    })
  },
  addElement(){
    for (let j = 0; j < 26; j++) {
      this.data.pycustomerList.push({
        first: String.fromCharCode(65 + j),
        cList: []
      })
    }
  },
  delElement(){
    var k = 0
    for (let j = 0; j < 26 - k; j++) {
      if (this.data.pycustomerList[j].cList.length == 0) {
        this.data.pycustomerList.splice(j,1)
        j--
        k++
      }
    }
    console.log(this.data.pycustomerList)
  },
  initpycustomerList(){
    var that = this
    that.addElement()

    for (let i = 0; i < this.data.customerList.length; i++) {
      let j = this.data.customerList[i].firstletter
      let k = j.charCodeAt(0)
      this.data.pycustomerList[k - 65].cList.push(this.data.customerList[i])
    }

    that.delElement()
    this.setData({
      pycustomerList: this.data.pycustomerList,
      pyallcustomerList:this.data.pycustomerList,
      listCur: this.data.pycustomerList[0].first
    });
  },
  onLoad() {
    this.getCustomerList()
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
          listCur: pycustomerList[i].first,
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
    var that = this
    console.log("正在搜索")
    if(inputVal == ""){
      this.setData({
        pycustomerList:this.data.pyallcustomerList
      })
    }else{
      this.data.pycustomerList=[]
      that.addElement()
      for (let i = 0; i < this.data.customerList.length; i++) {
        let j = this.data.customerList[i].pinyin
        let k = j.toUpperCase().charCodeAt(0)
        let l = this.data.customerList[i].name
        if(j.indexOf(inputVal) != -1 || l.indexOf(inputVal) != -1){
          this.data.pycustomerList[k - 65].cList.push(this.data.customerList[i])
        }
      }
      that.delElement()
      console.log(this.data.pycustomerList)

      this.setData({
        pycustomerList: this.data.pycustomerList,
        listCur: this.data.pycustomerList[0].first
      });
    }

  },
});