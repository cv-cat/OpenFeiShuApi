# OpenFeiShuApi 🚀 - 飞书第三方API集成库

[![Python Version](https://img.shields.io/badge/python-3.7%2B-blue)](https://www.python.org/)
[![Python Version](https://img.shields.io/badge/nodejs-18%2B-blue)](https://nodejs.org/zh-cn/)

**✨ 飞书开放API的Python现代化封装库，提供简洁优雅的接口设计与全面的功能覆盖。**

**⚠️ 注意：如有侵权联系作者删除。**



| 模块       | 已实现                                                                             |
|----------|---------------------------------------------------------------------------------|
| 飞书PC | ✅ 飞书所有http接口（protobuf）    |
| 飞书PC | ✅ 飞书websockets私信ws协议（接收发消息，gzip+protobuf协议）      |


## 🚀 一些成品
- pendding~


## 特性亮点 ✨

- 🧩 **常用接口全覆盖** - 支持飞书开放平台全部API版本
- 🚀 **异步优先** - 支持async/await异步模式
- 📡 **事件框架** - 简洁易用的事件订阅处理中间件

## 🛠️ 快速开始
### ⛳运行环境
- Python 3.7+
- Node.js 18+

### 🎯安装依赖
```
pip install -r requirements.txt
npm install
```

### 🎨配置文件
复制cookie到代码中（注意！登录飞书后的cookie才是有效的，不登陆没有用，不然怎么知道给谁发消息）


### 🚀运行项目
```
python FlyBookAutoAsync.py
```

### 🗝️注意事项
- FlyBookAutoAsync.py中的代码是接收发消息的主入口，可以根据自己的需求进行修改
- FlyBookApi.py中的代码包含了api接口的模板，sign参数已经解密，可以根据自己的需求进行修改，添加其他的接口


## 🧸额外说明
1. 感谢star⭐和follow📰！不时更新
2. 作者的联系方式在主页里，有问题可以随时联系我
3. 可以关注下作者的其他项目，欢迎 PR 和 issue
4. 感谢赞助！如果此项目对您有帮助，请作者喝一杯奶茶~~ （开心一整天😊😊）
5. thank you~~~

<div align="center">
  <img src="./author/wx_pay.png" width="400px" alt="微信赞赏码"> 
  <img src="./author/zfb_pay.jpg" width="400px" alt="支付宝收款码">
</div>


## 📈 Star 趋势
## Star History
<a href="https://www.star-history.com/#cv-cat/OpenFeiShuApi&Date">
 <picture>
   <source media="(prefers-color-scheme: dark)" srcset="https://api.star-history.com/svg?repos=cv-cat/OpenFeiShuApi&type=Date&theme=dark" />
   <source media="(prefers-color-scheme: light)" srcset="https://api.star-history.com/svg?repos=cv-cat/OpenFeiShuApi&type=Date" />
   <img alt="Star History Chart" src="https://api.star-history.com/svg?repos=cv-cat/OpenFeiShuApi&type=Date" />
 </picture>
</a>
