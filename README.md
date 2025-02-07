# 索尼链自动刷tx脚本
## 索尼链OG徽章活动
## 从 2025 年 1 月 14 日到 2025 年 2 月 27 日之间，需要在 Soneium 上完成 45 笔交易，就可以得到OG徽章
## 官方也明确说明，这个OG徽章是获得传奇的门票，可能后续还有活动，OG徽章将于 2025 年 2 月 28 日自动空投到钱包，不可转让

## 1.说明：主要刷ETH- WETH互转，无任何磨损，只花费少量gas。
## 建议本地电脑运行，私匙文件在服务器无法保证安全
配置说明：自行修改以下参数，比如符合要求的把2改为45

##

    eth_amount = 0.001  # 每次交易的ETH数量
    
    num_transactions = 2  # 每个地址的交易次数
    
    GAS_LIMIT = 36194     # 如果交易失败，把gas调大一些

##


## 2.安装运行环境
支持系统为MAC及ubuntu正常运行

win系统没测试，正常运行python代码的win应该也可以运行。

address.txt存放私匙一行一个，abi.json不要做任何修改。

##

    pip install web3 eth_account

    pip install --upgrade web3

##

## 3.运行脚本

    python3 soneium.py

![image](https://github.com/user-attachments/assets/62691e0a-5a88-4978-a5af-5ec06fea73eb) 

