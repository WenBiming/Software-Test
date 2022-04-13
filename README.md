# KylinAutoGUI 😎


## 工具简介



## 运行方式

### 配置要求
硬件要求：  
软件要求：  
系统要求：Kylin-Desktop   
依赖要求：scrot&emsp;xdotool  &emsp;python3  



### 安装xdotool依赖
sudo apt install xdotool
### 安装scrot依赖
sudo apt install scrot
### 安装python依赖
pip3 install -r requirements.txt


### 运行命令
运行示例case的方法：  
python3 case1.py

## 使用方法

1.安装所有依赖   
2.根据需求使用[基础方法](usage_manual.md "点击查看使用方法")编写测试用例


## 目录结构 
kylinautogui&emsp;&emsp;&emsp;&emsp;&emsp;&emsp; &emsp;#根目录  
├── libs    
   └── untils  
           └── functions.py&emsp;&emsp;&emsp;#主要方法  
├── log  &emsp;&emsp;&emsp;&emsp;&emsp;&emsp; &emsp; &emsp;#log日志存放目录  
├── README.md &emsp;&emsp;&emsp;&emsp;#说明文档  
├── requirements.txt&emsp;&emsp;&emsp;#Python依赖文件  
├── result&emsp;&emsp;&emsp;&emsp;&emsp; &emsp; &emsp; #结果存放目录  
├── screenshot&emsp;&emsp;&emsp;&emsp;&emsp; #截图存放目录  
└── test  &emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp; #测试用例目录  
      ├── testcase.py  &emsp;&emsp;&emsp;&emsp;#测试用例文件  
      └── test.py  &emsp;&emsp;&emsp;&emsp;&emsp;&emsp;#方法测试文件  



## 常见问题
1.在arm架构下验证，第一次运行需额外安装python3-tk python3-dev  
安装命令:  
sudo apt-get install python3-tk python3-dev

## 版本更新

### v0.1
优化部分方法  
修改方法名称  
增加入参校验及方法执行返回值  
部分会出问题的方法暂时设为私有方法 



