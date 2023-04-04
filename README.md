# git-tools

## 1、功能说明

可以自动在gitlab中的n个仓库m个分支搜索指定字符串，并返回其所在位置

输出日志参见：log文件夹

安装依赖：

```ssh
pip install -r requirements.txt
```


## 2、配置和自定义功能支持

参考 config.yml 文件

目前模式只支持群组模式（group）

## 3、下一步增加内容

1. 支持单项目查询；
2. 支持本地查询


## 4、其他

> 群组模式（type_group项配置）

1. group_id：已测试
2. project_match_type：all 已测试，normal 已测试，regexp 已测试；
3. branch_match_type：last_commit_time 已测试，【all、name_match】 未测试，但应该没问题；
4. branch_match_name：未测试，但应该没问题；
5. branch_limit：已测试
6. commit_since_before：已测试