# SAMS

Student Affair Management System（学生事务管理系统）是长春大学计算机科学技术学院团委主导的学生工作电子化平台。

该系统是学生思想政治素养第二课堂成绩单的电子化实践，具有德育分申请、查询、公示等功能。

## Source
根据长计团联【2023】2号《关于推进学团工作标准化的通知》文件相关要求，为保障学生信息安全，保障学生权益，特开源本系统源代码，以便安全部门审计。

## Installation

### 1. 创建数据库
在目标MYSQL数据库中创建一个名为sams的数据库

```sql
create database sams
```
### 2. 构建docker镜像
```bash
git clone https://github.com/phil616/sams.git
docker build -t sams .
```

### 3. 运行docker容器
```bash
docker run \
-e DB_HOST=localhost \
-e DB_PORT=3306 \
-e DB_NAME=sams \
-e DB_USER=root \
-e DB_PASSWORD=123456 \
-e CACHE_HOST=localhost \
-e CACHE_PORT=6379 \
-e JWT_SECRET_KEY=hexrecommended \
-e WX_MINI_SECRET=hexonly \
-e WX_MINI_APPID=hexonly \
-e APP_INIT_SECRET=hexrecommended \
-e APP_ENCRYPT_SECRET=hexrecommended \
-e EMAIL_USERNAME=username@mail.com \
-e EMAIL_PASSWORD=123456 \
-p 80:80 \
-v /path/of/log:/app/logs \
-v /path/of/storage/file:/app/storage \
sams
```
docker容器预计大小：1.1GigBytes

### 4. 环境解释
1. DB_HOST：MYSQL主机
2. DB_PORT：MYSQL端口
3. DB_NAME：MYSQL数据库名称
4. DB_USER：MYSQL用户名
5. DB_PASSWORD：MYSQL数据库密码
6. CACHE_HOST：Redis主机
7. CACHE_PORT：Redis端口
8. JWT_SECRET_KEY：JWT验证密钥
9. WX_MINI_SECRET：微信小程序接入密钥
10. APP_INIT_SECRET：初始化用户凭证
11. WX_MINI_APPID：微信小程序注册id
12. APP_ENCRYPT_SECRET：加密初始密钥
13. EMAIL_USERNAME：邮箱用户名
14. EMAIL_PASSWORD：邮箱登录密码

为保证二进制字符串的统一性和密钥随机性，建议使用urandom函数生成密钥类字符串。

```bash
cat /dev/urandom | tr -dc 'a-f0-9' | fold -w 64 | head -n 1
```
### 5. 日志管理

由于Fast API后台日志输出到STDOUT，因此可用下列命令输出到文件中。
```bash
docker logs -f --tail 100 [docker_ID] >> /var/log/sams/logs/STDOUTlogfile.txt 2>&1 &
```
推荐的目录：
```bash
/usr/local/sams/log
/usr/local/sams/storage
```