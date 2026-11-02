---
name: vincent-studio-poster
description: "Vincent 工作室活动海报 Skill：为瑜伽馆、健身房、普拉提馆、运动康复馆、心身灵工作室、音乐疗愈/颂钵工作室生成店庆、周年庆、开业、促销（双11/618/会员日/早鸟）、节假日（春节/中秋/妇女节/母亲节/世界瑜伽日等）活动海报。支持三种入口：已有活动方案→直接出图；方案+照片/Logo/二维码等素材→出图；只有想法→先策划 3 套推广方案，确认后出图。内置 8 种行业风格，一次输出 3:4、9:16、1:1、16:9 四种规格 PNG（HTML 精确排版，中文、价格、Logo 零错字），也可输出生图模型提示词。"
---

# Vincent 工作室活动海报 Skill

把「活动方案」变成「可直接发布的海报」：**策划 → 文案提炼 → 风格设计 → 四规格出图 → 自检交付**。

- 出图方式默认是 **HTML 精确排版 + Chrome 无头截图**（`scripts/render_poster.py`）：中文、价格、日期、Logo、二维码 100% 准确，四个规格一次生成、视觉统一。
- 需要“摄影级场景/人物”但用户没有照片时，用生图模型生成**无文字底图**，再交给脚本排版（见 [ai-image-prompts](references/ai-image-prompts.md)）。

## 适用范围

| 馆型 | 典型活动 |
|---|---|
| 瑜伽馆 / 冥想 | 店庆周年、开业、会员日、世界瑜伽日、新春开年课、工作坊招募 |
| 健身房 / 团操 | 双11/618 卡项大促、开业预售、减脂营、夏日燃脂、新年 flag |
| 普拉提馆 | 私教课包、会员日、体态评估、产后修复专场、母亲节 |
| 运动康复馆 | 体态筛查、开学季青少年脊柱、跑者护膝、术后康复讲座 |
| 心身灵工作室 | 满月/新月冥想、疗愈工作坊、年终觉察、读书会 |
| 音乐疗愈 / 颂钵 | 颂钵音浴、声音冥想之夜、助眠专场、双人疗愈 |

## 核心铁律

1. **事实零编造**：价格、原价、日期、地址、电话、名额、老师资历只用用户提供的；缺失就问，或在方案阶段明确标“建议值，需你确认”。出图前必须得到确认。
2. **合规先行**：遵守《广告法》等常识，详见 [copy-compliance](references/copy-compliance.md)。禁用“最/第一/顶级/国家级”等绝对化用语；康复、疗愈类不得承诺疗效或使用医疗用语（“治愈、根治、治疗”）；原价必须是真实成交价；不写“最终解释权归本店所有”。
3. **一次只问一题**，用编号选项让用户回复数字；用户已给的信息直接采用，不重复问。
4. **四层文案结构**：① 主标题（每行 ≤ 7 字，最多 2–3 行）② 一个视觉锚点（大数字/折扣/周年数）③ 3 条卖点（每条 ≤ 12 字）④ 行动信息（日期 + 地点 + CTA）。其他信息一律下沉或删除。
5. **四规格同一套视觉**：同一活动的 3:4 / 9:16 / 1:1 / 16:9 使用同一风格、配色与文案，仅排版重构。
6. **先渲染、再看图、再交付**：每次渲染后必须查看 PNG（至少总览图），按自检清单修正后再交付。

## 三种入口模式（先判断）

| 模式 | 用户给了什么 | 你要做什么 |
|---|---|---|
| **A 直接出图** | 完整活动方案/文案 | 提炼四层文案 → 推荐风格 → 渲染 |
| **B 方案 + 素材** | 方案 + 照片/Logo/二维码/品牌色 | 同 A，并读取素材：照片色调与构图、Logo 主色 → 校准配色 |
| **C 先策划** | 只有馆型/节日/目标，或说“你帮我想” | 按 [campaign-playbook](references/campaign-playbook.md) 出 3 套方案 → 用户选定/修改 → 再走 A |

## 工作流程

### 第 1 步：收集要点（缺什么问什么，一次一题）

必需：**馆型与品牌名、活动类型/主题、活动日期、核心优惠或亮点、CTA 方式**。
可选：地址、电话、二维码、Logo、照片、品牌色、需要的规格（默认四种全出）。

问题示例（编号选择）：
> 这次活动主要目标是？ 1. 拉新获客 2. 老会员续费 3. 节日氛围/品牌曝光 4. 清淡季促活 5. 新课程/新老师推广

### 第 2 步（仅模式 C）：给出 3 套推广方案

读取 [campaign-playbook](references/campaign-playbook.md)，节日相关再读 [holiday-calendar](references/holiday-calendar.md)，馆型调性读 [studio-dna](references/studio-dna.md)。
按 playbook 的“方案输出模板”给出 **稳妥型 / 爆发型 / 情感型** 3 套方案（主题名、机制、价格结构、节奏、物料清单、海报主文案草稿）。用户回复编号或修改意见后进入第 3 步。

### 第 3 步：提炼海报文案

把方案压缩成 spec 字段（见 [spec-schema](references/spec-schema.md)）：

| 字段 | 规则 |
|---|---|
| `eyebrow` | 眉题：活动类型/英文/期数，如 `3rd Anniversary · 感恩有你` |
| `title` | 主标题，`\n` 分行，`**词**` 高亮 1 处 |
| `subtitle` | 一句话价值，≤ 20 字 |
| `hero` | 视觉锚点：`{"value":"5","unit":"折","label":"年卡限时"}` |
| `points` | 3 条卖点（最多 4） |
| `offers` | 1–3 个价格卡：`name / price / original / note / tag` |
| `date` `location` `contact` `cta` `qr` | 行动信息 |
| `footnote` | 必要的规则说明/免责声明（小字） |

把提炼结果给用户确认一次（尤其价格与日期）。

### 第 4 步：选择风格与配色

先给 Top 3 推荐（每条一句理由），用户回复编号即可；用户说“你定”就用第一推荐。

| 风格 `style` | 气质 | 最适合 |
|---|---|---|
| `linen` 晨光亚麻 | 燕麦米白 + 鼠尾草绿、拱门照片、衬线标题 | 瑜伽、冥想、阴瑜伽、工作坊、店庆 |
| `quiet` 静奢极简 | 大幅出血照片、细线、菜单式价目 | 普拉提、高端私教、会员日 |
| `power` 能量大字报 | 黑底 + 荧光绿、斜切黑白照片、滚动横幅 | 健身房、双11/618、特训营、开业冲刺 |
| `pop` 多巴胺派对 | 高饱和撞色、粗描边贴纸、爆炸贴 | 开业、店庆、团课、亲子、夏日、520 |
| `aura` 疗愈光晕 | 深紫极光渐变、圆形光门、声波涟漪 | 音乐疗愈、颂钵、满月冥想、心身灵 |
| `festive` 东方节庆 | 双金框、竖排书法标题、月门圆窗、青海波 | 春节、元旦、中秋、国庆、端午、冬至 |
| `clinic` 专业康复 | 冰蓝网格、数据卡、白卡片 | 运动康复、体态筛查、产后修复 |
| `editorial` 杂志周年刊 | 报头 + 巨型数字叠印、编辑排版 | 周年庆、品牌升级、年度回顾 |

变体：`festive` → `red`（春节/国庆/元旦）、`moon`（中秋/七夕/冬至）、`jade`（端午/清明/春分）；`pop` → `sunny` / `berry` / `mint`；`aura` → `night` / `dawn`（浅色）。

**配色校准**：有 Logo 或品牌色时，用 `palette` 覆盖 `accent`（主强调色）/`accent2`；有照片时取服装/环境主色做 `accent`，保持与风格底色协调。各风格可覆盖的变量见 [spec-schema](references/spec-schema.md)。
规格与安全区说明见 [formats](references/formats.md)。

### 第 5 步：写 spec 并渲染

1. 把 spec 写成 JSON（放在用户工作目录，如 `poster/<活动名>.json`；素材路径相对 JSON 文件）。可参考 `examples/` 下 8 个示例。
2. 渲染（本 skill 目录记为 `$SKILL`）：

```bash
python3 $SKILL/scripts/render_poster.py poster/anniv.json --sheet          # 四规格 + 总览图
python3 $SKILL/scripts/render_poster.py poster/anniv.json --ratios 3:4     # 只出 3:4
python3 $SKILL/scripts/render_poster.py poster/anniv.json --style aura     # 临时换风格对比
python3 $SKILL/scripts/render_poster.py poster/anniv.json --scale 2        # 2 倍高清
python3 $SKILL/scripts/render_poster.py --doctor                           # 检查 Chrome / 中文字体
```

输出到 `<spec 目录>/output/`：`<name>_3x4.png`、`_9x16.png`、`_1x1.png`、`_16x9.png`、`_sheet.png`，以及同名可编辑 `.html`。
3. 某规格信息过密时，用 `by_ratio` 精简，例如 `"by_ratio": {"1:1": {"subtitle": "", "offers": [...只留 1 个]}}`。
4. 需要独特版式时：用 `custom_css`（CSS 文件路径或内联字符串）追加样式；可覆盖 `grid-template-areas` 重新布局，或直接修改生成的 HTML 再截图。

### 第 6 步：看图自检（必须查看 PNG）

- [ ] 主标题是全图最大元素，手机缩略图下 1 秒可读
- [ ] 价格、日期、地址、电话与用户确认的一致，无错字
- [ ] 无文字压住人物五官；照片主体未被裁掉（用 `photo_focus` 调整，如 `"50% 20%"`）
- [ ] 四个规格信息一致；1:1、16:9 没有拥挤（拥挤就用 `by_ratio` 删减）
- [ ] 无溢出、无重叠、无孤字成行（标题行尾单字时调整断行）
- [ ] 合规：无绝对化用语、无疗效承诺、原价真实、有必要的规则小字
- [ ] 若渲染时打印 `POSTER_DENSE`，说明文字被缩小超过 25%，应删减内容

### 第 7 步：交付

1. **文案与设计说明**：风格、配色理由、四层文案。
2. **海报文件**：四规格 PNG 路径（若环境支持展示图片，展示总览图）。
3. **可编辑源文件**：spec JSON + HTML。
4. 结尾只问一句：“需要调整文案/配色/风格，或生成朋友圈文案与社群通知吗？”

## 无法运行脚本时

- 没有 Chrome/Chromium/Edge：加 `--html-only` 生成 HTML，让用户用浏览器打开后截图；或设置环境变量 `CHROME_PATH`。
- 完全无法执行代码（如纯对话环境）：按 [ai-image-prompts](references/ai-image-prompts.md) 输出四规格生图提示词，并提醒用户生图模型的中文可能出错，价格和日期需自行核对。

## 文件索引

| 文件 | 何时读取 |
|---|---|
| [references/styles.md](references/styles.md) | 风格详情、选择矩阵、配色提取 |
| [references/campaign-playbook.md](references/campaign-playbook.md) | 模式 C 策划方案；优惠机制设计 |
| [references/holiday-calendar.md](references/holiday-calendar.md) | 节日/节点活动 |
| [references/studio-dna.md](references/studio-dna.md) | 判断馆型调性、配色、用词 |
| [references/copy-compliance.md](references/copy-compliance.md) | 写文案与出图前合规检查 |
| [references/formats.md](references/formats.md) | 规格、平台用途、密度上限 |
| [references/spec-schema.md](references/spec-schema.md) | 写 spec JSON |
| [references/ai-image-prompts.md](references/ai-image-prompts.md) | 生成无文字底图或纯提示词交付 |
| `examples/*.json` | 8 个风格各一个完整示例 |
