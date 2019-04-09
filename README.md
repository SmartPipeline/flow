# flow
flow是一个开发团队工作流工具，可以简化开发人员工作步骤，以及规范开发流程。\
flow is a development workflow tool. It can simplify devloper work steps, and unifies the developer approach

# 模块 Modules
## flow setup
主要包括同时克隆多个项目克隆，项目初始化设置，自动创建新分支\
This module contains clone multiple projects, do initial setup and checkout into new dev branch.

## flow update
多个项目同时rebase，保持与远程代码同步\
This module contains rebase multiple projects, to make sure syncing with remote code.

## flow push
检查本地代码状态（代码是否修改、修改是否提交），推送分支代码\
This module can check local branch status (if changes, if committed or not), and then push dev branch codes into orgin master branch.

## flow cleanup
检查本地代码状态（代码是否修改、修改是否提交、分支是否推送、分支是否被合并），删除本地项目，清除分支信息\
This module can check local branch status (if changes, if committed, if pushed, if merged into origin master), and then cleanup local project, delete orgin dev branch.

# 目标 TODO
linux, windows通用，而且根据各公司开发流程不同能够灵活修改
This tool can be used in Linux and Windows. Flexible modification according to the development process of each faclity.
