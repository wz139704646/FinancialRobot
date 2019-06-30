## 更新日志

## [v0.5.14](https://github.com/youzan/vant-weapp/tree/v0.5.14) (2019-05-30)
[Full Changelog](https://github.com/youzan/vant-weapp/compare/v0.5.13...v0.5.14)

**Breaking changes**

- tabbar 无法通过设置border消除白边 [\#1614](https://github.com/youzan/vant-weapp/issues/1614)
- \[Feature Request\] radio能不能像checkbox一样自定义icon？ [\#1586](https://github.com/youzan/vant-weapp/issues/1586)

**Bug Fixes**

- datetime-picker设置max-date报错 [\#1637](https://github.com/youzan/vant-weapp/issues/1637)
- SubmitBar组件tip-icon API没有生效 [\#1626](https://github.com/youzan/vant-weapp/issues/1626)

**Issue**

- bind:click-icon 应该阻止事件冒泡 [\#1670](https://github.com/youzan/vant-weapp/issues/1670)
- 微信小程序Toast.success\('成功'\);图标不显示且报错Failed to load font https://img.yzcdn.cn/vant/vant-icon-839a51.woff2 [\#1669](https://github.com/youzan/vant-weapp/issues/1669)
- Module build failed:  module.exports = \_\_webpack\_public\_path\_\_ + "libs/vant-weapp/lib/common/index.wxss";              ^ Unrecognised input [\#1667](https://github.com/youzan/vant-weapp/issues/1667)
- 使用npm开始项目时报错 [\#1666](https://github.com/youzan/vant-weapp/issues/1666)
- 使用popUpd弹层时，在弹层上上下滑动，或者点击，事件会透传到下方控件 [\#1664](https://github.com/youzan/vant-weapp/issues/1664)
- icon在button中无法上下居中对齐 [\#1663](https://github.com/youzan/vant-weapp/issues/1663)
- 如何不在回调函数中获取picker组件，从而调用相应方法 [\#1661](https://github.com/youzan/vant-weapp/issues/1661)
- 组件的style样式无效 [\#1658](https://github.com/youzan/vant-weapp/issues/1658)
- popup 影响小程序picker-view/picker-view-column 二次渲染赋值value [\#1657](https://github.com/youzan/vant-weapp/issues/1657)
- 小程序 tabbar 功能切换BUG 反馈 [\#1656](https://github.com/youzan/vant-weapp/issues/1656)
- \[Picker\]选择器 层级问题 [\#1655](https://github.com/youzan/vant-weapp/issues/1655)
- 华为P20使用van-field组件password类型时无法选中进行输入 [\#1654](https://github.com/youzan/vant-weapp/issues/1654)
- tab [\#1653](https://github.com/youzan/vant-weapp/issues/1653)
- Cannot find name 'VantComponentOptions'. [\#1652](https://github.com/youzan/vant-weapp/issues/1652)
- radio 和checkbox数据格式的不一致 [\#1650](https://github.com/youzan/vant-weapp/issues/1650)
- 为何每个组件的每个class都生成2个？ [\#1648](https://github.com/youzan/vant-weapp/issues/1648)
- 轮播图的宽高没设置百分比 [\#1647](https://github.com/youzan/vant-weapp/issues/1647)
- 小程序的van-tabs组件和文档说的不一样 [\#1646](https://github.com/youzan/vant-weapp/issues/1646)
- GoodsAction组件的GoodsActionIcon 外部样式类无效 的问题 [\#1644](https://github.com/youzan/vant-weapp/issues/1644)
- GoodsAction组件的GoodsActionIcon 外部样式类无效 [\#1643](https://github.com/youzan/vant-weapp/issues/1643)
- 小标题错误，应该是es5的 [\#1642](https://github.com/youzan/vant-weapp/issues/1642)
- 做了一个百度小程序版本  欢迎使用 [\#1638](https://github.com/youzan/vant-weapp/issues/1638)
- 单列picker，设置default-index，不起作用 [\#1636](https://github.com/youzan/vant-weapp/issues/1636)
- tab自定义头部 [\#1635](https://github.com/youzan/vant-weapp/issues/1635)
- DatetimePicker 如何设置选择生日？ [\#1633](https://github.com/youzan/vant-weapp/issues/1633)
- van-button disabled 无效 还可以点击出发事件 [\#1629](https://github.com/youzan/vant-weapp/issues/1629)
- ts 下引入报错  Cannot compile namespaces when the '--isolatedModules' flag is provided. [\#1628](https://github.com/youzan/vant-weapp/issues/1628)
- tabs 组件问题 [\#1620](https://github.com/youzan/vant-weapp/issues/1620)
- 循环radio后，radio内容区域点击有效，直接点击radio无效 [\#1610](https://github.com/youzan/vant-weapp/issues/1610)
- Search 组件高级模式点击触发查询事件失效 [\#1572](https://github.com/youzan/vant-weapp/issues/1572)
- tabbar 点击切换时能不能先进行一些判断，条件不满足时，不切换tab，还在当前tab上 [\#1564](https://github.com/youzan/vant-weapp/issues/1564)

**Improvements**

- \[bugfix\] SubmitBar: fix tip-icon not work [\#1671](https://github.com/youzan/vant-weapp/pull/1671) ([rex-zsd](https://github.com/rex-zsd))
- \[new feature\] Card: add bottom slot [\#1668](https://github.com/youzan/vant-weapp/pull/1668) ([chenjiahan](https://github.com/chenjiahan))
- \[new feature\] Radio & Checkbox: 统一Radio与Checkbox的API [\#1665](https://github.com/youzan/vant-weapp/pull/1665) ([rex-zsd](https://github.com/rex-zsd))
- \[bugfix\] DatetimePicker: 修复wepy中组件初始化报错 [\#1659](https://github.com/youzan/vant-weapp/pull/1659) ([rex-zsd](https://github.com/rex-zsd))
- \[new feature\] Tabbar: add border prop [\#1649](https://github.com/youzan/vant-weapp/pull/1649) ([chenjiahan](https://github.com/chenjiahan))
- \[docs\] Tabbar: 修复文档标题错误 [\#1645](https://github.com/youzan/vant-weapp/pull/1645) ([rex-zsd](https://github.com/rex-zsd))

## [v0.5.13](https://github.com/youzan/vant-weapp/tree/v0.5.13) (2019-05-15)
[Full Changelog](https://github.com/youzan/vant-weapp/compare/v0.5.12...v0.5.13)

**Breaking changes**

- \[Feature Request\] Dialog的宽度设置 [\#1592](https://github.com/youzan/vant-weapp/issues/1592)
- \[Feature Request\] 建议NoticeBar left-icon支持icon组件 [\#1589](https://github.com/youzan/vant-weapp/issues/1589)
- \[Feature Request\] field组件对password的支持 [\#1581](https://github.com/youzan/vant-weapp/issues/1581)
- NoticeBar取消不了滚动；用不多行显示 [\#1568](https://github.com/youzan/vant-weapp/issues/1568)

**Bug Fixes**

- 关于CheckBox问题 [\#1606](https://github.com/youzan/vant-weapp/issues/1606)
- toast 设置loading 隐藏之后还有view遮住页面 导致页面不能点击 [\#1565](https://github.com/youzan/vant-weapp/issues/1565)
- Stepper 步进器的输入框，从别的地方复制文字进去，会导致整个小程序报错，从而无法使用 [\#1546](https://github.com/youzan/vant-weapp/issues/1546)
- Stepper 录入小数点马上被还原成整数 [\#1533](https://github.com/youzan/vant-weapp/issues/1533)
- van-icon实底question没有问号 [\#1522](https://github.com/youzan/vant-weapp/issues/1522)

**Issue**

- van-swipe-cell向左滑动，右边的 “删除” 没有样式 [\#1622](https://github.com/youzan/vant-weapp/issues/1622)
- picker需要增加一下range-key属性 [\#1619](https://github.com/youzan/vant-weapp/issues/1619)
- formatter	选项格式化函数 报错 [\#1615](https://github.com/youzan/vant-weapp/issues/1615)
- popup 组件中的 close-on-click-overlay 失效 [\#1613](https://github.com/youzan/vant-weapp/issues/1613)
- stepper async-change无效 [\#1611](https://github.com/youzan/vant-weapp/issues/1611)
- van-field不渲染 [\#1608](https://github.com/youzan/vant-weapp/issues/1608)
- tab 文字过长显示不全 [\#1607](https://github.com/youzan/vant-weapp/issues/1607)
- 部分手机 cell is-link 会造成页面空白 [\#1537](https://github.com/youzan/vant-weapp/issues/1537)
- van-toast调用是，关闭的时候还有一块透明的view，没有完全隐藏 [\#1476](https://github.com/youzan/vant-weapp/issues/1476)

**Improvements**

- \[new feature\] Rate: add new prop allow-half [\#1623](https://github.com/youzan/vant-weapp/pull/1623) ([rex-zsd](https://github.com/rex-zsd))
- \[bugfix\] Transition: 修复leave阶段时节点不消失 [\#1621](https://github.com/youzan/vant-weapp/pull/1621) ([rex-zsd](https://github.com/rex-zsd))
- \[new feature\] NoticeBar: add new prop wrapable [\#1617](https://github.com/youzan/vant-weapp/pull/1617) ([rex-zsd](https://github.com/rex-zsd))
- \[bugfix\] Checkbox: fix style error [\#1616](https://github.com/youzan/vant-weapp/pull/1616) ([rex-zsd](https://github.com/rex-zsd))
- \[new feature\] NoticeBar: left-icon replace to Icon component [\#1604](https://github.com/youzan/vant-weapp/pull/1604) ([JakeLaoyu](https://github.com/JakeLaoyu))

## [v0.5.12](https://github.com/youzan/vant-weapp/tree/v0.5.12) (2019-05-05)
[Full Changelog](https://github.com/youzan/vant-weapp/compare/v0.5.11...v0.5.12)

**Issue**

- van-tabs type=card时的宽度如何设置 [\#1598](https://github.com/youzan/vant-weapp/issues/1598)
- Collapse折叠板点击无变化 bug [\#1597](https://github.com/youzan/vant-weapp/issues/1597)
- vant-weapp 官网文档 中 Search 组件缺少 change 方法 [\#1596](https://github.com/youzan/vant-weapp/issues/1596)
- van-stepper 的点击事件会传递给父层级 [\#1594](https://github.com/youzan/vant-weapp/issues/1594)
-  form表单提交无法获得数据 [\#1590](https://github.com/youzan/vant-weapp/issues/1590)
- 请教小程序版van-field如何搭配van-popup? [\#1588](https://github.com/youzan/vant-weapp/issues/1588)
- Layout组件设置gutter无效 [\#1587](https://github.com/youzan/vant-weapp/issues/1587)
- goodsAction的info只显示了1/4（疑似与wxParse样式冲突） [\#1582](https://github.com/youzan/vant-weapp/issues/1582)
- DatetimePikcer 选择2019年的时候 月份显示不全 [\#1580](https://github.com/youzan/vant-weapp/issues/1580)
- switch在微信小程序中显示异常 [\#1575](https://github.com/youzan/vant-weapp/issues/1575)
- Collapse 可以默认展开吗？ [\#1573](https://github.com/youzan/vant-weapp/issues/1573)
- vant-weapp   Slider 组件文档中有垂直方向 但是属性或者propsl里并没有提供参数可以配置 [\#1571](https://github.com/youzan/vant-weapp/issues/1571)
- 官方是否可以增加scroll-view下拉刷新的模块 [\#1570](https://github.com/youzan/vant-weapp/issues/1570)
- 表单placeholder 遮挡 [\#1569](https://github.com/youzan/vant-weapp/issues/1569)
- 框架是否可以增加 pageLifetimes  [\#1566](https://github.com/youzan/vant-weapp/issues/1566)
- SwipeCell 滑动单元格 没效果 [\#1563](https://github.com/youzan/vant-weapp/issues/1563)
- notify无法弹出 [\#1562](https://github.com/youzan/vant-weapp/issues/1562)
- SubmitBar 提交订单栏 没有全选按钮 [\#1561](https://github.com/youzan/vant-weapp/issues/1561)
- van-slider max为200的时候样式会有问题 [\#1559](https://github.com/youzan/vant-weapp/issues/1559)

**Improvements**

- \[Doc\] Tab: update demo [\#1603](https://github.com/youzan/vant-weapp/pull/1603) ([chenjiahan](https://github.com/chenjiahan))
- \[Doc\] Collapse: fix typo in document [\#1602](https://github.com/youzan/vant-weapp/pull/1602) ([chenjiahan](https://github.com/chenjiahan))
- \[new feature\] Dialog: add class-name prop [\#1601](https://github.com/youzan/vant-weapp/pull/1601) ([chenjiahan](https://github.com/chenjiahan))
- \[bugfix\] Stepper: can not input decimal number [\#1600](https://github.com/youzan/vant-weapp/pull/1600) ([chenjiahan](https://github.com/chenjiahan))
- \[bugfix\] Stepper: should filter invalid input [\#1599](https://github.com/youzan/vant-weapp/pull/1599) ([chenjiahan](https://github.com/chenjiahan))
- \[bugfix\] Icon: new and question icon incomplete render [\#1595](https://github.com/youzan/vant-weapp/pull/1595) ([chenjiahan](https://github.com/chenjiahan))
- \[new feature\] SubmitBar: add tip-icon prop [\#1593](https://github.com/youzan/vant-weapp/pull/1593) ([JakeLaoyu](https://github.com/JakeLaoyu))
- \[Doc\] support layout demo [\#1585](https://github.com/youzan/vant-weapp/pull/1585) ([chenjiahan](https://github.com/chenjiahan))
- \[Doc\] add weapp flag to demo page [\#1584](https://github.com/youzan/vant-weapp/pull/1584) ([chenjiahan](https://github.com/chenjiahan))
- \[new feature\] Field: add password prop [\#1583](https://github.com/youzan/vant-weapp/pull/1583) ([chenjiahan](https://github.com/chenjiahan))
- \[Doc\] Dialog: update demo [\#1579](https://github.com/youzan/vant-weapp/pull/1579) ([chenjiahan](https://github.com/chenjiahan))
- \[Doc\] Rate: update demo [\#1578](https://github.com/youzan/vant-weapp/pull/1578) ([chenjiahan](https://github.com/chenjiahan))
- \[bugfix\] SubmitBar: avoid using tag selector [\#1577](https://github.com/youzan/vant-weapp/pull/1577) ([chenjiahan](https://github.com/chenjiahan))
- \[improvement\] NoticeBar: optimize wxml [\#1576](https://github.com/youzan/vant-weapp/pull/1576) ([chenjiahan](https://github.com/chenjiahan))
- \[bugfix\] NoticeBar: avoid using tag selector [\#1574](https://github.com/youzan/vant-weapp/pull/1574) ([chenjiahan](https://github.com/chenjiahan))

## [v0.5.11](https://github.com/youzan/vant-weapp/tree/v0.5.11) (2019-04-24)
[Full Changelog](https://github.com/youzan/vant-weapp/compare/v0.5.10...v0.5.11)

**Breaking changes**

- cell的title自定义时，label不显示 [\#1554](https://github.com/youzan/vant-weapp/issues/1554)
- Toast 轻提示 是否可以增加回调函数 [\#1551](https://github.com/youzan/vant-weapp/issues/1551)
- 文档中Badge组件没有列出事件 [\#1542](https://github.com/youzan/vant-weapp/issues/1542)
- dateTimePicker什么没有自定义的custom-class啊，不支持自定义的class [\#1526](https://github.com/youzan/vant-weapp/issues/1526)
- 功能性的优化希望知悉！ [\#1502](https://github.com/youzan/vant-weapp/issues/1502)
- notify 麻烦支持top 和 zIndex [\#1498](https://github.com/youzan/vant-weapp/issues/1498)

**Bug Fixes**

- area 组件无地区选项又不显示了 [\#1543](https://github.com/youzan/vant-weapp/issues/1543)
- 页面只有一个collapse, 点击tabs 的时候重新加载数据,会报错 [\#1515](https://github.com/youzan/vant-weapp/issues/1515)
- van-field 组件在不输入文本时placeholder提示文本没有垂直居中，输入文本正常 [\#1483](https://github.com/youzan/vant-weapp/issues/1483)

**Issue**

- swipe [\#1550](https://github.com/youzan/vant-weapp/issues/1550)
- vant [\#1549](https://github.com/youzan/vant-weapp/issues/1549)
- 关于mpvue使用van-swipe-cell不出现内容 [\#1548](https://github.com/youzan/vant-weapp/issues/1548)
- 提供megalo版本 [\#1547](https://github.com/youzan/vant-weapp/issues/1547)
- tabbar 未适配 iPhone X，border-top 那条线和 icon 重叠了 [\#1545](https://github.com/youzan/vant-weapp/issues/1545)
- van-action-sheet中close-on-click-overlay属性无效 [\#1544](https://github.com/youzan/vant-weapp/issues/1544)
- Dialog弹出框弹出时，其中的Field输入框会向下抖动 [\#1534](https://github.com/youzan/vant-weapp/issues/1534)
- popup底部弹出时，被页面底部内容覆盖 [\#1532](https://github.com/youzan/vant-weapp/issues/1532)
- auth required for publishing [\#1531](https://github.com/youzan/vant-weapp/issues/1531)
- 希望实现通过active属性在业务代码中能控制tabs组件内容切换 [\#1528](https://github.com/youzan/vant-weapp/issues/1528)
- tbs 组件报错 [\#1523](https://github.com/youzan/vant-weapp/issues/1523)
- https://youzan.github.io/vant-weapp 文档打不开 [\#1521](https://github.com/youzan/vant-weapp/issues/1521)
- https://youzan.github.io/vant-weapp 文档打不开 [\#1520](https://github.com/youzan/vant-weapp/issues/1520)
- 动态修改datePicker defaultIndex ，默认选中项不更新 [\#1519](https://github.com/youzan/vant-weapp/issues/1519)
- 构建npm成功之后，编译报错 : module "miniprogram\_npm/vant-weapp/mixins/observer/props" is not defined [\#1516](https://github.com/youzan/vant-weapp/issues/1516)
- 新需求：van-goods-action-input [\#1514](https://github.com/youzan/vant-weapp/issues/1514)
- 按钮box-shadow在ios问题 [\#1513](https://github.com/youzan/vant-weapp/issues/1513)
- Dialog弹窗被原生组件覆盖 [\#1511](https://github.com/youzan/vant-weapp/issues/1511)
- NavBar 组件safe-area-inset-top属性设置无效 [\#1505](https://github.com/youzan/vant-weapp/issues/1505)

**Improvements**

- \[new feature\] Icon: update @vant/icons [\#1560](https://github.com/youzan/vant-weapp/pull/1560) ([rex-zsd](https://github.com/rex-zsd))
- \[new feature\] DatetimePicker: add new prop formatter & add new external classes [\#1558](https://github.com/youzan/vant-weapp/pull/1558) ([rex-zsd](https://github.com/rex-zsd))
- \[new feature\] Badge: add new event click & improve docs [\#1557](https://github.com/youzan/vant-weapp/pull/1557) ([rex-zsd](https://github.com/rex-zsd))
- \[bugfix\] Area: 修复同步设置areaList时不显示选项 [\#1556](https://github.com/youzan/vant-weapp/pull/1556) ([rex-zsd](https://github.com/rex-zsd))
- refactor\(Picker\): 回滚movable-view重构 @rex-zsd [\#1555](https://github.com/youzan/vant-weapp/pull/1555) ([rex-zsd](https://github.com/rex-zsd))
- \[bugfix\] Slider: fix slider drag and `value` props change at the same time can not drag success [\#1553](https://github.com/youzan/vant-weapp/pull/1553) ([cookfront](https://github.com/cookfront))
- \[new feature\] Toast: add new option onClose & add new slot [\#1552](https://github.com/youzan/vant-weapp/pull/1552) ([rex-zsd](https://github.com/rex-zsd))
- \[new feature\] Picker: add new prop default-index [\#1540](https://github.com/youzan/vant-weapp/pull/1540) ([rex-zsd](https://github.com/rex-zsd))
- \[Doc\] update demo index [\#1539](https://github.com/youzan/vant-weapp/pull/1539) ([chenjiahan](https://github.com/chenjiahan))
- \[new feature\] Collapse: add clickable prop [\#1538](https://github.com/youzan/vant-weapp/pull/1538) ([chenjiahan](https://github.com/chenjiahan))
- \[new feature\] Notify: add new prop zIndex [\#1535](https://github.com/youzan/vant-weapp/pull/1535) ([rex-zsd](https://github.com/rex-zsd))
- \[Doc\] Icon: update demo [\#1530](https://github.com/youzan/vant-weapp/pull/1530) ([chenjiahan](https://github.com/chenjiahan))
- \[new feature\] SubmitBar: add decimal-length prop [\#1529](https://github.com/youzan/vant-weapp/pull/1529) ([chenjiahan](https://github.com/chenjiahan))
- \[improvement\] Field: add right-icon & fix placeholder style problem [\#1527](https://github.com/youzan/vant-weapp/pull/1527) ([rex-zsd](https://github.com/rex-zsd))
- \[improvement\] Picker: refactor component with movable-view [\#1524](https://github.com/youzan/vant-weapp/pull/1524) ([rex-zsd](https://github.com/rex-zsd))
- \[bugfix\] Collapse: remove reference from children of collapse when collapse-item unlinked [\#1517](https://github.com/youzan/vant-weapp/pull/1517) ([rex-zsd](https://github.com/rex-zsd))
- \[new feature\] Cell: add new prop useLabelSlot & add new slot label [\#1510](https://github.com/youzan/vant-weapp/pull/1510) ([rex-zsd](https://github.com/rex-zsd))
- \[new feature\] Feild: add error-message-align prop [\#1509](https://github.com/youzan/vant-weapp/pull/1509) ([zavven](https://github.com/zavven))

## [v0.5.10](https://github.com/youzan/vant-weapp/tree/v0.5.10) (2019-04-11)
[Full Changelog](https://github.com/youzan/vant-weapp/compare/v0.5.9...v0.5.10)

**Breaking changes**

- van-tabs多个tab页的情况下   切换tab页会显示滚动条 [\#1471](https://github.com/youzan/vant-weapp/issues/1471)

**Bug Fixes**

- BUG:当组件van-collapse 被第二个van-tab中使用时，默认展开的效果会丢失 [\#1494](https://github.com/youzan/vant-weapp/issues/1494)
- SwipeCell 内放输入框无法focus输入 [\#1464](https://github.com/youzan/vant-weapp/issues/1464)

**Issue**

- css错误 [\#1508](https://github.com/youzan/vant-weapp/issues/1508)
- 我想在自己的组件中再次封装vant组件，始终不起作用，在page中是有效的 [\#1507](https://github.com/youzan/vant-weapp/issues/1507)
- 当页面同时使用两个tab时点击切换后第二个tab的当前标签没有恢复到第一个 [\#1503](https://github.com/youzan/vant-weapp/issues/1503)
- 感谢你们的辛勤付出 [\#1500](https://github.com/youzan/vant-weapp/issues/1500)
- title-active-color 自定义颜色，选中时文字的颜色没有变化 [\#1499](https://github.com/youzan/vant-weapp/issues/1499)
- van-swipe-cell所有的点击都没有效果 [\#1497](https://github.com/youzan/vant-weapp/issues/1497)
- 我在mpvue中引入van-swipe-cell,没有任何效果 [\#1496](https://github.com/youzan/vant-weapp/issues/1496)
- Bug：van-info在引用wxParse的页面中数字错位 [\#1495](https://github.com/youzan/vant-weapp/issues/1495)
- van-dialog 加 van-field,弹出后field文字会抖动一下 [\#1488](https://github.com/youzan/vant-weapp/issues/1488)
- tree-select点击事件没有效果？ [\#1487](https://github.com/youzan/vant-weapp/issues/1487)

**Improvements**

- \[bugfix\] Collapse: improve performance & optimize initial style set [\#1506](https://github.com/youzan/vant-weapp/pull/1506) ([rex-zsd](https://github.com/rex-zsd))
- \[improvement\] SwipeCell: improve performance & fix prevent scroll [\#1501](https://github.com/youzan/vant-weapp/pull/1501) ([rex-zsd](https://github.com/rex-zsd))
- \[docs\] README: fix change log url [\#1491](https://github.com/youzan/vant-weapp/pull/1491) ([nyaapass](https://github.com/nyaapass))
- \[docs\]: update issue template [\#1490](https://github.com/youzan/vant-weapp/pull/1490) ([rex-zsd](https://github.com/rex-zsd))
- \[docs\]: add es5 guide [\#1489](https://github.com/youzan/vant-weapp/pull/1489) ([rex-zsd](https://github.com/rex-zsd))

## [v0.5.9](https://github.com/youzan/vant-weapp/tree/v0.5.9) (2019-04-03)
[Full Changelog](https://github.com/youzan/vant-weapp/compare/v0.5.8...v0.5.9)

**Breaking changes**

- 是否有编译后的es5版本 [\#1469](https://github.com/youzan/vant-weapp/issues/1469)

**Bug Fixes**

- Slider 单击滑动区域，不能修改滑块位置 [\#1477](https://github.com/youzan/vant-weapp/issues/1477)

**Issue**

- 设置van-tabbar为自定义tabbar时，调用wx.switchTab后active激活状态异常，无法正常对应tabbar [\#1481](https://github.com/youzan/vant-weapp/issues/1481)
- swiperCell组件的event事件无效 [\#1475](https://github.com/youzan/vant-weapp/issues/1475)
- 组件用最新的开发工具，各种报错 [\#1474](https://github.com/youzan/vant-weapp/issues/1474)
- uni-app框架支持 [\#1473](https://github.com/youzan/vant-weapp/issues/1473)
- van-popup无法关闭弹出层，只能关闭遮罩层，微信小程序 [\#1472](https://github.com/youzan/vant-weapp/issues/1472)
- van-cell组件跳转深度层级页数问题？ [\#1470](https://github.com/youzan/vant-weapp/issues/1470)
- van-popup 微信苹果IOS下不显示弹出框 [\#1468](https://github.com/youzan/vant-weapp/issues/1468)
- Tab组件若被包含在 if block当中会存在bug [\#1467](https://github.com/youzan/vant-weapp/issues/1467)
- Toast引用求助 [\#1466](https://github.com/youzan/vant-weapp/issues/1466)
- tab标签页，bind:scroll如何使用 [\#1465](https://github.com/youzan/vant-weapp/issues/1465)
- 在微信小程序预览，可以详细一些吗， [\#1463](https://github.com/youzan/vant-weapp/issues/1463)
- 文档错误·checkbox自定义图标image标签缺少闭合斜杠 [\#1462](https://github.com/youzan/vant-weapp/issues/1462)
- Popup不能弹出图片 [\#1458](https://github.com/youzan/vant-weapp/issues/1458)
- vant tab页  可以加上竖着滑动 [\#1456](https://github.com/youzan/vant-weapp/issues/1456)
- 增强DatetimePicker控件 [\#1455](https://github.com/youzan/vant-weapp/issues/1455)
- Picker选择器 默认选中项 实现方式 [\#1454](https://github.com/youzan/vant-weapp/issues/1454)
- radio加载字体图标报错 [\#1453](https://github.com/youzan/vant-weapp/issues/1453)

**Improvements**

- \[new feature\]: compile es5 dist [\#1485](https://github.com/youzan/vant-weapp/pull/1485) ([rex-zsd](https://github.com/rex-zsd))
- \[bugfix\] Slider: fix click not work [\#1484](https://github.com/youzan/vant-weapp/pull/1484) ([rex-zsd](https://github.com/rex-zsd))
- \[bugfix\] Icon: avoid using tag selector [\#1482](https://github.com/youzan/vant-weapp/pull/1482) ([chenjiahan](https://github.com/chenjiahan))
- \[new feature\] Stepper: add input-width prop [\#1480](https://github.com/youzan/vant-weapp/pull/1480) ([chenjiahan](https://github.com/chenjiahan))
- \[docs\] Checkbox: fix doc error [\#1479](https://github.com/youzan/vant-weapp/pull/1479) ([rex-zsd](https://github.com/rex-zsd))
- \[new feature\]: support safe-area-inset-top [\#1478](https://github.com/youzan/vant-weapp/pull/1478) ([rex-zsd](https://github.com/rex-zsd))
- \[build\]: fix watch not work [\#1461](https://github.com/youzan/vant-weapp/pull/1461) ([rex-zsd](https://github.com/rex-zsd))
- \[improvement\] Tabbar: improve performance [\#1460](https://github.com/youzan/vant-weapp/pull/1460) ([rex-zsd](https://github.com/rex-zsd))
- \[bugfix\] SwipeCell: close event never emit [\#1459](https://github.com/youzan/vant-weapp/pull/1459) ([rex-zsd](https://github.com/rex-zsd))

## [v0.5.8](https://github.com/youzan/vant-weapp/tree/v0.5.8) (2019-03-22)
[Full Changelog](https://github.com/youzan/vant-weapp/compare/v0.5.7...v0.5.8)

## [v0.5.7](https://github.com/youzan/vant-weapp/tree/v0.5.7) (2019-03-09)
[Full Changelog](https://github.com/youzan/vant-weapp/compare/v0.5.6...v0.5.7)

## [v0.5.6](https://github.com/youzan/vant-weapp/tree/v0.5.6) (2019-02-28)
[Full Changelog](https://github.com/youzan/vant-weapp/compare/v0.5.5...v0.5.6)

## [v0.5.5](https://github.com/youzan/vant-weapp/tree/v0.5.5) (2019-02-26)
[Full Changelog](https://github.com/youzan/vant-weapp/compare/v0.5.4...v0.5.5)

## [v0.5.4](https://github.com/youzan/vant-weapp/tree/v0.5.4) (2019-02-18)
[Full Changelog](https://github.com/youzan/vant-weapp/compare/v0.5.3...v0.5.4)

## [v0.5.3](https://github.com/youzan/vant-weapp/tree/v0.5.3) (2019-02-06)
[Full Changelog](https://github.com/youzan/vant-weapp/compare/v0.5.2...v0.5.3)

## [v0.5.2](https://github.com/youzan/vant-weapp/tree/v0.5.2) (2019-01-20)
[Full Changelog](https://github.com/youzan/vant-weapp/compare/v0.5.1...v0.5.2)

## [v0.5.1](https://github.com/youzan/vant-weapp/tree/v0.5.1) (2019-01-10)
[Full Changelog](https://github.com/youzan/vant-weapp/compare/v0.5.0...v0.5.1)



\* *This Change Log was automatically generated by [github_changelog_generator](https://github.com/skywinder/Github-Changelog-Generator)*