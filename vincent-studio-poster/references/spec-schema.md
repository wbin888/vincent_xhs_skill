# 海报 Spec（JSON）字段说明

渲染脚本：`python3 scripts/render_poster.py <spec.json> [选项]`。所有图片路径可以是绝对路径、相对 **spec 文件所在目录**的路径、`http(s)://` 或 `data:` URL；文件不存在会警告并忽略。

## 完整示例

```json
{
  "style": "linen",
  "variant": null,
  "ratios": ["3:4", "9:16", "1:1", "16:9"],
  "output_name": "qimu-3rd-anniversary",
  "palette": { "accent": "#6F8F78" },

  "brand": { "name": "栖木瑜伽", "name_en": "QIMU YOGA STUDIO", "logo": "assets/logo.png", "tagline": "Since 2023" },
  "eyebrow": "3rd Anniversary · 感恩有你",
  "title": "三周年\n与**呼吸**同在",
  "subtitle": "一场为老朋友与新朋友准备的身心礼物",
  "hero": { "value": "3", "unit": "周年", "label": "11.15 – 11.30 · 店庆感恩月" },
  "points": ["阴瑜伽公开课 免费体验", "老会员续卡 加赠 30 天", "带朋友同行 各得一节私教"],
  "offers": [
    { "name": "年卡·店庆价", "price": "3280", "original": "日常价 ¥4680", "note": "限前 30 名", "tag": "限量" },
    { "name": "10 次体验卡", "price": "699", "original": "日常价 ¥980" }
  ],
  "date": "11.15 — 11.30",
  "location": "上海 · 静安区 XX 路 88 号 2F",
  "contact": "预约电话 021-0000 0000",
  "cta": "私信预约 · 名额有限",
  "qr": "assets/qr.png",
  "qr_label": "扫码预约",
  "photo": "assets/teacher.jpg",
  "photo_focus": "50% 25%",
  "footnote": "价格以门店实际为准；体验课每人限 1 次",

  "by_ratio": {
    "1:1":  { "subtitle": "", "offers": [{ "name": "年卡·店庆价", "price": "3280", "original": "日常价 ¥4680" }] },
    "16:9": { "footnote": "" }
  },
  "custom_css": ".st-linen .title{letter-spacing:.06em}"
}
```

## 字段表

| 字段 | 类型 | 说明 |
|---|---|---|
| `style` | string | `linen` `quiet` `power` `pop` `aura` `festive` `clinic` `editorial` `numeral` `ruby` `latte` `doodle` `noir` `mocha`，见 [styles.md](styles.md) |
| `variant` | string | `festive`: `red`/`moon`/`jade`；`pop`: `sunny`/`berry`/`mint`；`aura`: `night`/`dawn`。省略取第一个 |
| `ratios` | string[] | 默认四种全出；命令行 `--ratios` 优先 |
| `output_name` | string | 输出文件名前缀，默认 spec 文件名 |
| `palette` | object | 覆盖 CSS 变量（不带 `--`），如 `{"accent":"#C0563B","bg":"#F4EFE6"}` |
| `brand.name` / `name_en` / `tagline` | string | 品牌中文名、英文名、角标（如 Since 2021） |
| `brand.logo` | path | Logo；建议透明 PNG 或方形图，会被裁成圆形 |
| `eyebrow` | string | 眉题，小字，位于主标题上方 |
| `title` | string | 主标题。`\n` 或 `|` 换行；`**词**` 高亮（强调色） |
| `subtitle` | string | 副标题，支持 `**高亮**` |
| `hero` | object | 视觉锚点：`value`（大数字/字）、`unit`（单位）、`label`（说明） |
| `points` | string[] | 卖点，最多 4 条，建议 3 条；支持 `**高亮**` |
| `offers` | object[] | 价格卡，最多 3 个（列表型风格 quiet/numeral/ruby/latte/noir/mocha 最多 4 个）：`name` `price` `original` `note` `tag` `currency` `unit` |
| `offers[].unit` | string | 价格后的小字单位，如 `/10节`、`/月` |
| `script` | string | 手写英文装饰字（如 `Beauty`、`Pilates`），latte/noir/mocha 显示 |
| `points_title` / `offers_title` | string | 要点/价目区块标题（numeral/ruby/latte/doodle/noir/mocha 显示） |
| `offers[].price` | string | 纯数字自动加 `¥`（`currency` 可改）；非数字原样显示（如 `"免费"`、`"5 折"`） |
| `date` `location` `contact` | string | 行动信息区 |
| `cta` | string | 行动按钮文字，如 `扫码预约` `私信报名` |
| `qr` / `qr_label` | path / string | 二维码图片与说明 |
| `photo` | path | 主图（人物/场馆/器材）。缺省时各风格用自带的抽象插画占位 |
| `photo_focus` | string | 照片裁切焦点 `object-position`，默认 `50% 30%`；人脸偏上用 `50% 20%` |
| `ticker` | string | `power` 风格底部滚动横幅文字（默认品牌英文名 + 眉题） |
| `footnote` | string | 规则/免责声明小字 |
| `by_ratio` | object | 按规格覆盖任意字段，键为 `3:4` `9:16` `1:1` `16:9`；值设为 `""` 或 `[]` 即隐藏 |
| `custom_css` | string | `.css` 文件路径或内联 CSS，追加在风格样式之后 |

## 各风格可覆盖的配色变量

| 风格 | 变量 |
|---|---|
| linen | `bg` `ink` `accent` `accent2` `soft` `card` |
| quiet | `bg` `ink` `accent` `accent2` `line` `onphoto` |
| power | `bg` `ink` `accent`（荧光主色） `accent2` `muted` |
| pop | `bg` `ink` `accent` `accent2` `accent3` `paper` |
| aura | `bg` `ink` `accent` `accent2` `accent3` `glass` `glassline` |
| festive | `bg` `ink` `accent`（金） `accent2` `deep` |
| clinic | `bg` `ink` `accent` `accent2` `card` `line` |
| editorial | `bg` `ink` `accent` `muted` `line` |
| numeral | `bg` `ink` `accent` `accent2` `panel` `bar` `line` |
| ruby | `bg` `ink` `accent` `accent2` `deep` `card` `line` `onred` |
| latte | `bg` `ink` `accent` `accent2` `pill` `line` `onphoto` |
| doodle | `bg` `ink` `accent`（黄） `accent2` `teal` `box` |
| noir | `bg` `ink` `accent`（薄荷） `accent2` `line` |
| mocha | `bg` `ink` `accent` `accent2` `box` `band` `line` |

## 布局类名（写 `custom_css` 时使用）

- 根元素：`.poster.st-<style>.ra-<portrait|tall|square|wide>.v-<variant>`，并带 `has-photo/no-photo`、`has-offers/no-offers` 等状态类。
- 1rem = 画布短边的 1%；文字字号用 em，基于 `--base`（每个规格不同）× 自动缩放系数 `--k`。
- 网格区域：`brand` `head` `hero` `pts` `off` `photo` `info` `fine`。重排版面示例：

```css
.st-quiet.ra-square{grid-template-columns:1fr 1fr;grid-template-areas:"photo brand" "photo head" "photo pts" "photo off" "info info"}
```

- 主要元素：`.brand` `.headline > .eyebrow/.title/.subtitle` `.hero > .hv/.hu/.hl` `.points li` `.offers .offer > .otag/.on/.op/.oo/.onote` `.photo > .frame > img` `.info > .date/.loc/.contact/.cta/.qr` `.fine` `.deco > i.d1–d5`。

## 命令行选项

| 选项 | 作用 |
|---|---|
| `--out DIR` | 输出目录，默认 `<spec 目录>/output` |
| `--ratios 3:4,1:1` | 只渲染部分规格 |
| `--style X` / `--variant V` | 临时换风格/变体（便于对比） |
| `--scale 2` | 2 倍像素（印刷/大屏） |
| `--sheet` | 额外输出四规格总览图 `_sheet.png` |
| `--html-only` | 只生成 HTML（无 Chrome 时） |
| `--chrome PATH` | 指定浏览器路径（也可设环境变量 `CHROME_PATH`） |
| `--no-check` | 跳过密度检测（略快） |
| `--list-styles` | 列出风格 |
| `--doctor` | 检查 Chrome 与中文字体 |

渲染日志里的 `fit=` 是文字自动缩放系数：1.00 表示无需缩小；< 0.75 会提示 `POSTER_DENSE`，应精简该规格内容。
