# 完成GitHub Action设置指南

## 1. 删除不需要的main分支

由于我们将使用master分支作为主分支，我们需要删除不必要的main分支：

1. 访问仓库的Branches页面：https://github.com/Yalexyo/ai-video-workflow-test/branches
2. 找到main分支
3. 点击右侧的删除图标(🗑️)删除分支

## 2. 创建Pull Request测试AI代码审查

1. 访问：https://github.com/Yalexyo/ai-video-workflow-test/pull/new/test/ai-review
2. 确保base分支选择为"master"，compare分支为"test/ai-review"
3. 点击"Create pull request"
4. 添加标题："测试视频处理模块和AI代码审查"
5. 提交PR

## 3. 验证GitHub Action

提交PR后，GitHub Action会自动运行：
1. Action会检测到您修改了src/core/目录下的文件
2. 使用Claude Opus通过OpenRouter API分析代码
3. 在PR评论中添加AI代码审查结果

## 4. 合并PR (可选)

审查AI反馈后，可以合并PR到master分支，完成整个工作流程测试。
