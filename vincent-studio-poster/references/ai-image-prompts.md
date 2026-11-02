# 生图模型提示词（AI 底图 / 纯提示词交付）

两种用法：

1. **推荐：AI 生成无文字底图 → 脚本排版**。用户没有照片但需要摄影级画面时，用生图模型（GPT-Image、Midjourney、即梦、可灵、Nano Banana 等）生成**不含任何文字**的照片，保存后填入 spec 的 `photo`。脚本负责所有文字，保证零错字。
2. **备选：纯提示词交付**。无法运行脚本时，输出完整海报提示词；提醒用户生图模型可能写错中文，价格/日期需核对或后期替换。

## 1. 无文字底图提示词模板

```
<主体描述>, <场景>, <光线>, <色调>, <构图：主体位置与留白>, photorealistic editorial photography, 35mm, soft natural light, high detail,
no text, no letters, no watermark, no logo, no signage
比例：<与海报照片区域接近的比例，见下表>
```

各风格照片区域的推荐比例：

| 风格 | 照片区域形状 | 生成比例 |
|---|---|---|
| linen | 拱门竖幅 | 3:4 或 2:3 |
| quiet | 大幅出血 | 3:4（竖版海报）/ 1:1（方/横版） |
| power | 斜切竖幅（会转黑白） | 3:4 |
| pop | 倾斜圆角卡片 | 4:3 |
| aura | 圆形光门 | 1:1，主体居中 |
| festive | 月门圆窗 | 1:1，主体居中 |
| clinic | 圆角竖卡 | 3:4 |
| editorial | 竖幅杂志大图 | 3:4 |

## 2. 各风格底图示例

- **linen**：`A woman practicing seated meditation on a linen yoga mat in a sunlit yoga studio with arched window, oat beige and sage green tones, warm morning side light, airy minimal interior, subject centered with headroom, no text`
- **quiet**：`A reformer pilates machine in a minimalist studio with warm grey plaster walls, a woman in neutral activewear performing an elegant leg stretch, soft diffused light, muted taupe palette, lots of negative space, editorial luxury photography, no text`
- **power**：`A muscular athlete mid-deadlift in a dark industrial gym, dramatic rim lighting, sweat and chalk dust, high contrast, low angle, subject on the right third, no text`
- **pop**：`Happy diverse group dancing in a bright colorful fitness studio, candid laughter, saturated yellow pink and blue palette, flash photography look, no text`
- **aura**：`Tibetan singing bowls on a cushion in a dark candlelit room, soft purple and teal haze, gentle glow, mystical calm atmosphere, centered composition, no text`
- **festive**：`A woman in a modern Chinese-style outfit doing a graceful yoga pose in front of a round moon gate, warm red and gold tones, lanterns softly blurred in background, centered composition, no text`
- **clinic**：`A physiotherapist assessing a client's posture in a bright modern rehabilitation studio, icy blue and white tones, clean professional environment, natural light, no text`
- **editorial**：`Portrait of a confident yoga teacher standing in a studio, magazine cover style, soft studio lighting, warm neutral background, subject slightly left, no text`

## 3. 纯提示词交付模板（含文字，备选）

```
设计一张<比例>的<馆型><活动>海报，<风格描述（取 styles.md 对应风格的气质与配色）>。
画面：<照片/插画主体与位置>。
文字（务必准确、简体中文）：
- 顶部小字：「<eyebrow>」
- 主标题（最大、<字体气质>）：「<title 第一行>」「<title 第二行>」，其中「<高亮词>」用<强调色>
- 大数字：「<hero.value><hero.unit>」
- 卖点：「<p1>」「<p2>」「<p3>」
- 价格：「<offer name> ¥<price>」（原价「<original>」带删除线）
- 底部：「<date>」「<location>」，按钮「<cta>」
排版：<各区域位置>，留白充足，层级清晰，文字不压人脸。
比例 <3:4 / 9:16 / 1:1 / 16:9>，高清，商业海报质感。
```

四个规格各输出一条（只改比例与“排版”描述）。
