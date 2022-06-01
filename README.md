# FightTheLord


### SocketServer



### 项目架构:
Card 包含基本信息
Rule 对输入确定规则
Manager 



### TODO  

##### socket连接
采用socketserver及线程保持会话
在handle中编写逻辑
服务器开启客户端
建立socket通信
向客户端中传入ip,端口号,作为标识

##### 功能介绍
room_pool: 房间池,房间的集合
user_pool: 用户池,用户的集合

User: 用户对象,每个对象包含当前状态,所属的当前房间,绑定的ip及端口,当前的牌的数量,出牌的行为,准备,
roomitem: 房间对象,当前房间的状态(是否开始),加入用户,用户退出
manager: 容器对象,用于发牌,决定发牌顺序等逻辑,在roomitem中初始化


##### 操作说明


