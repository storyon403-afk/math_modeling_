github 

国内网的问题，有时候登陆GitHub会有些卡

GitHub就是一个仓库，世界上最大的开源平台。

git直白理解就是一个管理器

我们直接理解仓库为一个开放的远程的文件夹，登陆github以后打开仓库，可以直接在github上改代码，上传东西，很方便。

可以先不管下面的，下面主要是把远程仓库和本地编译器搭建起通道，这样本地编译器可直接通过指令上传代码那些，当然也可以复制后在GitHub上粘贴也是可以的。

—— 也可以克隆仓库在本地(本地编辑以后可上传，方便运行)

基于身份认证分为以下两种方式操作（推荐第二种ssh，因为国内网的原因）：

1.使用github账号登陆任意ide （比如vs code）
打开终端或任意ide的终端界面（比如vs code），切换到想要把仓库克隆到的位置（cd 路径）后，输入命令：
git clone https://github.com/storyon403-afk/math_modeling_
等待一下仓库就克隆好了
当前目录/
└──math_modeling_/


使用ide打开这个仓库，打开ide的终端界面：
git pull //这个意思是更新仓库最新内容到本地,每次都需要，这样才能看见做了哪些更改。

然后就可以更改内容了： git add . //添加当前目录更改的文件的所有内容到本地git
git commit -m “update”   // “”双引号里面的内容是这次更新说明，比如添加了什么算法啊，哪里做了什么修改啊，保存到本地 Git 历史
git push // 就是把本地 Git 提交上传到 GitHub，大家就看得见更新了啥
 git status // 显示本地git状态
  2.不使用github账号登陆ide，那么需要ssh密钥登陆：
打开终端输入：ssh-keygen -t ed25519 -C “你的GitHub邮箱”，回车默认保存位置 ~/.ssh/ （当前目录）会询问设置密码，可设可不设，设置了以后每次提交都要输密码。
然后当前目录输入命令：ls ~/.ssh
会得到密钥，类似于：id_ed25519（私钥）id_ed25519.pub（公钥）
查看共邀输入命令：cat ~/.ssh/id_ed25519.pub 会看到类似：ssh-ed25519 AAAAC3NzaC1…
全部复制，在GitHub ssh key 设置页：找New SSH key 
填写title 和 粘贴公钥到key

测试终端，输入命令：ssh -T git@github.com，第一次会提醒，输yes，成功后会显示success类似字样。
然后克隆仓库这样写,输入命令：
git clone git@github.com:storyon403-afk/math_modeling_ 后面与第一种过程一致
