# KylinAutoGUI


## 工具简介
用于开发GUI自动化测试工具的基础方法封装
功能包括：  
通用操作方法  
窗口操作方法  
鼠标、键盘操作方法  
截图方法  
文字识别方法  


## 运行方式

### 配置要求
硬件要求：  
软件要求：  
系统要求：  
依赖要求：scrot  
&emsp;&emsp;&emsp;&emsp;&emsp;xdotool  
&emsp;&emsp;&emsp;&emsp;&emsp;python3  


### 安装依赖
sudo apt install xdotool
### 安装截图依赖
sudo apt install scrot
### 安装python依赖
pip3 install -r requirements.txt


### 运行命令
运行示例case的方法：  
python3 case1.py

## 使用方法
先安装依赖  
查看基础方法(http://172.17.31.188:8090/pages/viewpage.action?pageId=11568606)  
根据需求使用基础方法编写测试用例  


## 目录结构 
├── case1.py /示例case文件  
├── libs  
│   └── untils  
│           └── functions.py /方法文件  
├── README.md  
├── result /存放最终扫描结果  
├── log /存放log日志  
└── screenshot /存放截图文件  


## 常见问题


## 版本更新

### v0.1
优化部分方法  
修改方法名称  
增加入参校验及方法执行返回值  
部分会出问题的方法暂时设为私有方法


