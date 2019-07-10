const app = getApp();
Page({
  data: {
    StatusBar: app.globalData.StatusBar,
    CustomBar: app.globalData.CustomBar,
    sellIconList: [{
      icon: 'shop',
      color: 'red',
      badge: 0,
      name: '销售记录',
      url: "/pages/application/sellList/sellList"
    }, {
      icon: 'friendadd',
      color: 'orange',
      badge: 0,
      name: '新增客户',
      url: "/pages/application/newCustomer/newCustomer"
    }, {
      icon: 'peoplelist',
      color: 'yellow',
      badge: 0,
      name: '客户列表',
      url: "/pages/application/customerList/customerList"
    }, {
      icon: 'cart',
      color: 'olive',
      badge: 0,
      name: '销售开单',
      url: "/pages/application/sellBill/sellBill"
    }, {
      icon: 'search',
      color: 'red',
      badge: 0,
      name: '查看近期',
      url: "/pages/application/searchRecent/searchRecent"
    }],
    buyIconList: [{
      icon: 'deliver_fill',
      color: 'red',
      badge: 0,
      name: '采购记录',
      url: '/pages/application/buyList/buyList'
    }, {
      icon: 'friendaddfill',
      color: 'orange',
      badge: 0,
      name: '新增供应商',
      url: '/pages/application/newSupplier/newSupplier'
    }, {
      icon: 'expressman',
      color: 'yellow',
      badge: 0,
      name: '供应商列表',
      url: '/pages/application/supplierList/supplierList'
    }, {
      icon: 'file',
      color: 'olive',
      badge: 0,
      name: '采购开单',
      url: "/pages/application/buyBill/buyBill"
    }],
    fundIconList: [{
      icon: 'sponsor',
      color: 'red',
      badge: 0,
      name: '收款记录',
      url: ''
    }, {
      icon: 'sponsor',
      color: 'orange',
      badge: 0,
      name: '付款记录',
      url: ''
    }, {
      icon: 'recharge',
      color: 'yellow',
      badge: 0,
      name: '其他收入记录',
      url: ''
    }, {
      icon: 'recharge',
      color: 'olive',
      badge: 0,
      name: '其他支出记录',
      url: ''
    }, {
      icon: 'moneybag',
      color: 'orange',
      badge: 0,
      name: '资金流水',
      url: ''
    }, {
      icon: 'newshot',
      color: 'yellow',
      badge: 0,
      name: '资金转账记录',
      url: ''
    }, {
      icon: 'creative',
      color: 'olive',
      badge: 0,
      name: '利润分析',
      url: ''
    }],
    storeIconList: [{
      icon: 'goods',
      color: 'red',
      badge: 0,
      name: '新增商品',
      url: '/pages/application/newGood/newGood'
    }, {
      icon: 'list',
      color: 'orange',
      badge: 0,
      name: '商品列表',
      url: '/pages/application/goodList/goodList'
    }, {
      icon: 'deliver',
      color: 'yellow',
      badge: 0,
      name: '调拨记录',
      url: ''
    }, {
      icon: 'search',
      color: 'olive',
      badge: 0,
      name: '查看近期',
      url: ''
    }, {
      icon: 'edit',
      color: 'red',
      badge: 0,
      name: '其他入库',
      url: '/pages/application/inStore/inStore'
    }, {
      icon: 'edit',
      color: 'orange',
      badge: 0,
      name: '其他出库',
      url: ''
    }],
    financialIconList: [{
      icon: 'ticket',
      color: 'red',
      badge: 0,
      name: '凭证',
      url: ''
    }, {
      icon: 'copy',
      color: 'yellow',
      badge: 0,
      name: '报表',
      url: ''
    }, {
      icon: 'sort',
      color: 'yellow',
      badge: 0,
      name: '科目余额',
      url: ''
    }],
    gridCol: 4,
    skin: false
  },

  // ListTouch触摸开始
  ListTouchStart(e) {
    this.setData({
      ListTouchStart: e.touches[0].pageX
    })
  },

  // ListTouch计算方向
  ListTouchMove(e) {
    this.setData({
      ListTouchDirection: e.touches[0].pageX - this.data.ListTouchStart > 0 ? 'right' : 'left'
    })
  },

  show(e) {
    console.log("navigate")
    wx.navigateTo({
      url: e.currentTarget.id,
    })
  }
})