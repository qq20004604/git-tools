# git-tools

## 1、功能说明

可以自动在gitlab中的n个仓库m个分支搜索指定字符串，并返回其所在位置

输出日志参见：log文件夹

安装依赖：

```ssh
pip install -r requirements.txt
```

## 2、功能说明

> 核心功能：

在简单配置后，将自动查询目标字符串，位于 Gitlab 某个仓库->某个分支->某个文件->
第几行->该行具体内容，并输出日志。

> 具体功能描述：

1. 支持Gitlab群组搜索：配置群组ID后，自动搜索该群组下每一个仓库；
2. 搜索引擎：支持 Python 或者 Go，默认是Python
3. 指定群组ID：给出群组ID后，搜索该群组下每一个仓库；
4. 代码仓库过滤：允许只处理符合规则的代码仓库，以仓库名为规则进行匹配。支持所有仓库、仓库名关键词匹配、仓库名正则匹配；
5. 分支排序过滤：允许只处理符合规则的分支。支持全部分支、分支名正则匹配（也可以只当做关键词匹配使用），最后提交时间排序；
6. 分支处理数限制：当分支比较多的时候，允许只处理前 N 个分支；
7. 分支最后一次提交时间限制：允许只处理在最近 N 天内提交过的分支，超出分支将被忽略；
8. 被搜索文件过滤：允许只搜索文件名符合规则的文件。支持所有文件、指定名称的文件、文件名正则匹配、文件后缀名匹配等；

> 其他：

1. 简单详细的配置说明；
2. 所有代码都已开源，安全可靠；
3. 功能不断完善中；

目前支持模式：

1. 群组模式（group）
2. 单项目（repository）

## 3、下一步增加内容

1. 支持单项目查询（已支持）；
2. 支持本地查询

## 4、其他

> 分支管理

1. branch_match_type：last_commit_time 已测试，【all、name_match】 未测试，但应该没问题；
2. branch_match_name：未测试，但应该没问题；
3. branch_limit：已测试
4. commit_since_before：已测试

> 群组模式（type_group 项配置）

1. group_id：已测试
2. project_match_type：all 已测试，normal 已测试，regexp 已测试；

> 单项目模式（type_repository 项配置）

1. repository_model：已测试
2. repository_id：已测试
3. repository_name：已测试

> 多项目模式（type_repositories 项配置）

1. repositories_model：已测试
2. repositories_id：已测试
3. repositories_name：已测试
