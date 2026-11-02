# taobao-visual-studio

淘宝/天猫（兼容京东、拼多多、抖音电商）主图 + 详情页视觉策划与生图 Agent Skill。

流程：信息补全 → 消费者卖点地图 + 转化驱动力 → 产品身份锁定 → 主图 5 + 详情页 8-12 屏统一策划（审批闸门）→ 风格锁 + 逐张 Prompt → 出图 → 平台规范 / 《广告法》违禁词 / 视觉自检 → 交付。

## 安装

```bash
# GitHub Copilot CLI（Claude Code 换成 ~/.claude/skills，Codex 换成 ~/.codex/skills）
git clone https://github.com/wbin888/vincent_xhs_skill.git ~/vincent_xhs_skill && mkdir -p ~/.copilot/skills && cp -R ~/vincent_xhs_skill/taobao-visual-studio ~/.copilot/skills/
```

重启工具后说：`用 taobao-visual-studio 帮我做一套淘宝主图和详情页`

## 结构

- `SKILL.md`：主流程
- `references/`：平台规范、套图序列、Prompt 工艺、合规、来源分析
- `scripts/check_image.py`：白底/尺寸/大小检查，`--fix` 导出合规尺寸
- `scripts/lint_copy.py`：《广告法》极限词与类目禁用词检查
- `scripts/generate_image.py`：OpenAI 兼容生图接口（`IMAGE_API_KEY` / `IMAGE_API_BASE` / `IMAGE_MODEL`）

脚本依赖：Python 3.9+；`check_image.py` 需要 Pillow。
