# water-koubo

[简体中文](README.md) | [繁體中文](README.zh-TW.md) | English

> A viral short-video talking-head remix Skill.
>
> Give it one complete reference script and get a title, cover text, and a shoot-ready script.

![version](https://img.shields.io/badge/version-1.0.0-blue) ![Agent Skills](https://img.shields.io/badge/Agent-Skills-black) ![license](https://img.shields.io/badge/license-CC_BY--NC_4.0-green)

**Works with Codex, Claude Code, WorkBuddy, DeepSeek Harness, and other Agents that support Skills.**

water-koubo was created by 老肖AI运营. It packages a talking-head remix method drawn from 13 years of internet operations experience. The method has been used in real account production.

[Quick start](#quick-start) · [Capabilities](#capabilities) · [How it works](#how-it-works) · [Installation](#installation) · [Full guide](#full-usage-guide)

![water-koubo demo flow](./media/method-flow.png)

## What water-koubo helps with

Give water-koubo one strong reference script. It keeps the original idea, structure, cases, and peaks, then rewrites the opening, judgments, sentences, and details. It checks the attribution of facts and experiences and delivers a title, cover text, and complete talking-head script in one go.

It is built for creators who already have a complete reference script and want to turn it into content they can shoot.

## Quick start

After installation, enter this in an Agent that supports Skills:

~~~text
$water-koubo
[Paste or attach one complete Chinese reference script]
Remix it into a shoot-ready Chinese talking-head script.
~~~

When the reference is complete and readable, water-koubo delivers the finished script directly.

## Capabilities

| Capability | What you get |
|---|---|
| **Keep the viral logic** | Retains the strongest idea, structure, cases, and peaks from the reference |
| **Rewrite the opening** | Creates a fresh opening that earns attention from the first line |
| **Create a real remix** | Rewrites judgments, sentences, and details with new information and expression |
| **Keep cases properly attributed** | Keeps each experience with its real owner and avoids turning a source story into your personal story |
| **Add a new peak** | Adds a new judgment early so the script leaves a stronger impression |
| **Get the full script package** | Delivers the title, cover text, and talking-head script together |

The result is natural to say aloud, ready to shoot, and careful with facts and attribution.

## How it works

water-koubo completes each remix in five steps:

1. **One complete reference script**: Read the source and your current request.
2. **Find the viral mechanics**: Identify the idea, structure, cases, peaks, and ending.
3. **Rewrite the script**: Create a new opening, judgments, sentences, and details.
4. **Check attribution**: Confirm who owns each fact, case, and experience.
5. **Complete deliverables**: Return the title, cover text, and talking-head script.

## Installation

Run this command in a terminal:

~~~bash
npx -y skills add waterbrojx/water-koubo -g --all
~~~

Return to an Agent that supports Skills, use **$water-koubo**, and provide one complete reference script. For ZIP import, choose the **skills/water-koubo** directory.

Current version: **1.0.0 / Unreleased**. The first public release date will be added before publication.

## Full usage guide

### Input

- Provide one complete reference script at a time;
- Paste text directly or attach a TXT, Markdown, Word, or text-selectable PDF that the host can read completely;
- If the file cannot be read completely, provide a complete reference script.

### Output

~~~text
标题：

封面文字：

口播正文：
~~~

For installation help, usage feedback, commercial licensing, or collaboration, add **Waterbro_jx** on WeChat and include **Skill** in your note.

## Changelog

### 1.0.0 · Unreleased

- First release of water-koubo;
- Turns one complete reference script into a title, cover text, and shoot-ready talking-head script;
- Adds a complete visual walkthrough.

## Author and license

**老肖AI运营｜WeChat: Waterbro_jx**

<img src="./media/wechat-qr.jpg" alt="老肖AI运营 WeChat QR code" width="240">

For commercial licensing or collaboration, include **Skill** in your note.

This project uses [CC BY-NC 4.0](https://creativecommons.org/licenses/by-nc/4.0/):

- Non-commercial use is free;
- Commercial use for short-video customer acquisition, agency services, paid training, or paid products requires separate authorization from 老肖AI运营;
- Redistribution or modification of project materials must retain attribution, the license notice, and a description of changes;
- Scripts generated with the Skill do not need to display the 老肖AI运营 attribution, while commercial use still requires authorization;
- The 老肖AI运营 brand, banner, WeChat QR code, and their combined presentation remain separately reserved.

See [LICENSE](LICENSE) and [NOTICE](NOTICE) for details. Official project: [waterbrojx/water-koubo](https://github.com/waterbrojx/water-koubo).
