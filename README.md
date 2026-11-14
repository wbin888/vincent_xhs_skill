# vincent-xhs-cover

> 小红书爆款封面 & 高转化招生海报 **提示词生成 Skill** · 194 种风格 · 3:4 竖版（可扩展 4:3 / 16:9）

发一张人物照和一段文案，它会读取照片色调、提炼文案重点、从 194 种风格（含宋式美学、胶片感、赛博朋克等 173 种美学风格）中推荐最合适的，再一步步问清细节，最后输出一段可直接复制给生图模型（Nano Banana / GPT-4o / 即梦 / Flux / Midjourney）的完整提示词。

- [快速开始](#快速开始)
- [安装](#安装)
- [使用方法](#使用方法)
- [194 种风格一览](#194-种风格一览)
- [常见问题](#常见问题)

## 快速开始

仓库地址：<https://github.com/wbin888/vincent_xhs_skill>

按你使用的工具复制**一整段**到终端执行（会先下载仓库，再复制到 skills 目录）：

```bash
# Claude Code
git clone https://github.com/wbin888/vincent_xhs_skill.git ~/vincent_xhs_skill && mkdir -p ~/.claude/skills && cp -R ~/vincent_xhs_skill/vincent-xhs-cover ~/.claude/skills/

# Codex
git clone https://github.com/wbin888/vincent_xhs_skill.git ~/vincent_xhs_skill && mkdir -p ~/.codex/skills && cp -R ~/vincent_xhs_skill/vincent-xhs-cover ~/.codex/skills/

# GitHub Copilot CLI
git clone https://github.com/wbin888/vincent_xhs_skill.git ~/vincent_xhs_skill && mkdir -p ~/.copilot/skills && cp -R ~/vincent_xhs_skill/vincent-xhs-cover ~/.copilot/skills/

# 通用 Agent Skills 目录
git clone https://github.com/wbin888/vincent_xhs_skill.git ~/vincent_xhs_skill && mkdir -p ~/.agents/skills && cp -R ~/vincent_xhs_skill/vincent-xhs-cover ~/.agents/skills/
```

> 已经下载过（`~/vincent_xhs_skill` 已存在）时，去掉前面的 `git clone … &&` 即可。

重启工具后，对它说：

```text
用 vincent-xhs-cover 帮我做一张小红书封面
```

## 安装

### 第 1 步：下载

任选一种：

- **Git**：`git clone https://github.com/wbin888/vincent_xhs_skill.git ~/vincent_xhs_skill`
- **GitHub CLI**：`gh repo clone wbin888/vincent_xhs_skill ~/vincent_xhs_skill`
- **ZIP**：打开 <https://github.com/wbin888/vincent_xhs_skill>，点 **Code → Download ZIP**，解压。

下载后要用的是其中的 **`vincent-xhs-cover/` 整个文件夹**，里面必须包含：

```text
vincent-xhs-cover/
├── SKILL.md
├── THIRD_PARTY_NOTICES.md
├── agents/openai.yaml
└── references/styles/   ← 22 个风格文件（1–21 各一个 + 22–194 美学风格库），缺了它无法出提示词
```

### 第 2 步：放到对应工具的 skills 目录

| 工具 | 个人目录（所有项目可用） | 项目目录（仅当前项目） |
|---|---|---|
| Claude Code | `~/.claude/skills/` | `.claude/skills/` |
| OpenAI Codex CLI | `~/.codex/skills/` | `.codex/skills/` |
| GitHub Copilot CLI / Agent | `~/.copilot/skills/` | `.github/skills/` |
| 其他支持 Agent Skills 的工具 | `~/.agents/skills/` | `.agents/skills/` |

**macOS / Linux**（把 `~/.claude/skills` 换成上表中你的目录）：

```bash
mkdir -p ~/.claude/skills
cp -R ~/vincent_xhs_skill/vincent-xhs-cover ~/.claude/skills/
```

**Windows（PowerShell）**：

```powershell
git clone https://github.com/wbin888/vincent_xhs_skill.git "$HOME\vincent_xhs_skill"
New-Item -ItemType Directory -Force "$HOME\.claude\skills" | Out-Null
Copy-Item -Recurse -Force "$HOME\vincent_xhs_skill\vincent-xhs-cover" "$HOME\.claude\skills\"
```

**只想在某个项目里用**：在该项目根目录执行，例如 Copilot：

```bash
mkdir -p .github/skills && cp -R ~/vincent_xhs_skill/vincent-xhs-cover .github/skills/
```

**Claude 网页版 / 桌面 App**：把 `vincent-xhs-cover` 文件夹压缩成 ZIP（压缩包内第一层就是 `vincent-xhs-cover/`），然后在 **设置 → 功能（Capabilities）→ Skills** 中上传。

```bash
cd ~/vincent_xhs_skill && zip -r vincent-xhs-cover.zip vincent-xhs-cover
```

### 第 3 步：确认安装成功

```bash
ls ~/.claude/skills/vincent-xhs-cover/references/styles | wc -l   # 应输出 22
```

然后**重启**工具（或开一个新会话），问一句“你能用哪些 skills？”，列表里出现 `vincent-xhs-cover` 即安装成功。

### 更新到最新版

```bash
cd ~/vincent_xhs_skill && git pull
rm -rf ~/.claude/skills/vincent-xhs-cover
cp -R ~/vincent_xhs_skill/vincent-xhs-cover ~/.claude/skills/
```

> 先删除再复制，避免旧版本残留文件。从旧版（只有 `SKILL.md` 的单文件版本）升级时尤其需要这样做。

### 卸载

```bash
rm -rf ~/.claude/skills/vincent-xhs-cover
```

## 使用方法

### 调用

| 工具 | 方式 |
|---|---|
| Claude Code | 输入 `/vincent-xhs-cover`，或直接描述需求 |
| Codex CLI | 输入 `$vincent-xhs-cover`，或直接描述需求 |
| Copilot CLI | 直接描述需求，并提到 `vincent-xhs-cover` |

直接描述需求的例子：

```text
用 vincent-xhs-cover 帮我生成一张普拉提器械私教招生小红书海报提示词。
```

```text
用 vincent-xhs-cover，这是我的照片和文章，帮我推荐风格做封面。
[附上照片] [粘贴文案]
```

### 流程

```text
① 发图片 + 文案 → ② 推荐 Top 3 风格（或自选 1–194）→ ③ 动作 → ④ 素材用途
→ ⑤ 背景 → ⑥ 字体 → ⑦ 字色 → ⑧ 提炼重点 & 选标题 → 输出提示词
```

- 第 2 步回复 ⭐ 编号或“你定”即采用第一推荐；也可以回复 1–194 任一编号自选。
- 第 2 步也可以直接说风格名，如“宋式美学”“胶片感”，会自动匹配编号。
- 第 3 步选 `0` 一键套用当前风格的最佳预设，直接跳到选标题。
- 首条消息就附上图片、文案或指定风格，会自动跳过对应步骤。

### 输出

1. **色调诊断 & 重点摘要**：识别到的参考照色调与配色方案，提炼出的主标题、高亮词、3 条重点、CTA。
2. **完整提示词**：独立代码块，一键复制到生图模型。
3. **横版延展**：满意后可重构为 4:3 / 16:9 左右分栏横版（公众号、朋友圈、B 站）。

## 核心能力

- **参考照色调统一**：先识别服装色、光影冷暖与主色相，背景、卡片、字色都围绕它配色，避免抠图感。
- **文案重点 4 层提炼**：主标题（4–10 字）+ 高亮词/大数字 + 3 条重点（每条 4–8 字）+ 底部 CTA。
- **智能推荐风格**：综合照片特征（服装、场景、色调、素材数量）与文案类型给出 Top 3 及理由。
- **194 种风格统一编号**：1–21 为专属版式，22–194 为 173 种美学风格（东方古典、日式、世界区域、西方艺术流派、数字科幻、胶片摄影、插画动画、色彩调性、暗黑亚文化等），套用通用美学封面版式。
- **出图前 9 项复核**：色调、文案层级、3:4 比例、五官不遮挡、手部结构、黄色统一 `#FDFFA7`、素材分工、零占位符、† 风格不写名称。
- **按需加载**：风格文件各自独立，每次只读取选中的那一个（22–194 只取所选那一行），`SKILL.md` 约 24KB，响应更快、更省上下文。

## 194 种风格一览

**体系一：经典大字抠图封面**

| # | 风格 | 适合 |
|---|---|---|
| 1 | 爆款大字压顶风 | 强钩子标题、经验公开 |
| 2 | 巨字拆分冲击风 | 概念、身份、能力类主题 |
| 3 | 小白科普问答风 | “什么是 / 怎么理解” |
| 4 | 教程清单风 | 安装、部署、上手教程 |
| 5 | 产品测评榜单风 | 横评、榜单、红黑榜 |
| 6 | 种草推荐风 | 资源、播客、工具推荐 |
| 7 | 贴纸拼贴入门风 | 入门、搭建、工具组合 |
| 8 | 黑底效率工作流风 | 工作法、自动化效率流 |

**体系二：课程招生海报**（均含 主标题 + 导师形象 + 3 条卖点/课表 + 报名 CTA）

| # | 风格 | 适合 |
|---|---|---|
| 9 | 苹果极简杂志风·名师私教 | 高客单 1v1、主理人大师课 |
| 10 | 备忘录手写便签风·课表大纲 | 课表发布、入门班、陪跑营 |
| 11 | 多巴胺高饱和插画风·活力团课 | 燃脂团课、有氧舞蹈 |
| 12 | 醒目大字报纯享风·限时特训 | 早鸟、周年庆、特训营 |
| 13 | Bento 卡片网格风·全维课程 | 体系课、教培、套餐卡 |
| 14 | 自然疗愈呼吸感·瑜伽/冥想 | 流瑜伽、阴瑜伽、工作坊 |
| 15 | 精准体态美学·普拉提私教 | 器械私教、体态矫正、产后修复 |

**体系三：通用版式**

| # | 风格 | 适合 |
|---|---|---|
| 16 | 手绘版 | 知识图解、动作要点、亲和力招生 |
| 17 | 纯文本版 | 金句观点、干货提纲、不露脸通知 |
| 18 | 简约版 | 高审美生活方式、高端工作室 |
| 19 | 贴图版 | 多图合集、场馆/课程多维展示 |
| 20 | 对比版 | Before/After、正误对比、避坑 |
| 21 | 单色印刷版 | 读书/观点/文化活动、个人品牌、独立杂志与孔版网点质感 |

**体系四：美学风格（22–194）**——统一套用通用美学封面版式（顶部标题 + 人物 + 3 条重点 + 底部 CTA），画面气质由所选风格决定；色板融入参考照色调，绘画/插画类人物以该风格重绘且五官神似。

| 编号 | 分类 | 举例 |
|---|---|---|
| 22–58 | 中国古典 · 文人美学 · 东方幻想 | 宋式美学、新中式、侘寂、留白、水墨、工笔、敦煌、国潮、故宫、岁朝清供 |
| 59–70 | 日本与东亚近现代 | 浮世绘、琳派、昭和、大正浪漫、和风、治愈系手绘动画 |
| 71–82 | 世界区域美学 | 韩式、印度、波斯细密画、北欧、斯堪的纳维亚、美式复古、波西米亚 |
| 83–110 | 西方艺术流派 | 印象派、超现实、Art Deco、巴洛克、构成主义、包豪斯、波普、铜版画 |
| 111–129 | 数字 · 科幻 · 现代设计 | 极简、极繁、赛博朋克、蒸汽波、Y2K、三维渲染、像素、故障艺术 |
| 130–140 | 摄影与光影 | 胶片、拍立得、柯达/富士、时尚摄影、丁达尔、浅景深、电影感 |
| 141–159 | 插画 · 动画 · 绘本 | 动漫、美漫、绘本、扁平、彩铅、黏土、折纸、水彩、波点 |
| 160–172 | 色彩与调性 | 莫兰迪、马卡龙、糖果色、霓虹、低饱和、黑白、暖/冷色调 |
| 173–175 | 亚文化与暗黑 | 哥特、暗黑、洛丽塔 |
| 176–194 | 补充风格 | 电影写真、手办、版画、港风动漫、复古动漫、莫奈/毕加索/伦勃朗/马蒂斯式 |

每个风格的色彩/构图/质感/光线关键词与通用版式模板见 [`22-194-aesthetic-library.md`](vincent-xhs-cover/references/styles/22-194-aesthetic-library.md)。

## 设计规范

- 默认 **3:4 竖版**，定稿后可扩展 4:3 / 16:9。
- 真人出镜，以图 1 保持五官一致；风格 17 可不出镜。
- 主标题超大、短促，移动端一眼可读。
- 黄色统一使用柔和浅黄 `#FDFFA7`（风格 21 例外：最多 2 种油墨，按墨色表选色）。
- 文字不遮挡眼睛和嘴巴，重要元素全部位于安全区内。
- 风格 22–194 一次只用一种美学，色板向参考照色调靠拢；吉卜力、皮克斯等工作室/在世艺术家相关风格在提示词中只写特征描述，不写名称。

## 目录结构

```text
vincent_xhs_skill/
├── README.md
└── vincent-xhs-cover/            ← 安装时复制这个文件夹
    ├── SKILL.md                  # 铁律、风格推荐、8 步问答、复核清单、输出格式
    ├── THIRD_PARTY_NOTICES.md    # 第三方许可声明
    ├── agents/openai.yaml        # Codex / OpenAI 展示信息
    └── references/styles/        # 1–21 各自的模板 + 22–194 美学风格库
        ├── 01-big-title-top.md
        ├── ...
        └── 21-mono-color-print.md
```

## 常见问题

**工具里找不到这个 skill？**
确认复制的是 `vincent-xhs-cover` 文件夹本身（目标路径应为 `…/skills/vincent-xhs-cover/SKILL.md`，而不是 `…/skills/vincent_xhs_skill/vincent-xhs-cover/` 或 `…/skills/SKILL.md`），然后重启工具。

**选完风格后提示找不到模板？**
`references/styles/` 没有一起复制。按“更新到最新版”的步骤删除后重新复制。

**它会直接出图吗？**
默认输出提示词。如果当前工具支持生图且你要求直接出图，会先生成一张 3:4 竖图再附提示词。

**怎么用 22–194 美学风格？**
和 1–21 一样，在第 2 步回复编号即可（如 `28`），或直接说风格名（如“东方禅意”“柯达胶片”）。完整清单见 [`22-194-aesthetic-library.md`](vincent-xhs-cover/references/styles/22-194-aesthetic-library.md)。

**可以不露脸吗？**
选风格 17（纯文本版），上传一张色调参考图即可，也可以只在角落放一个小头像。
