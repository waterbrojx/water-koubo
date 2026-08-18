from __future__ import annotations

import hashlib
import re
import struct
import unittest
import zipfile
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SKILL_DIR = ROOT / "skills" / "water-koubo"
QR_SHA256 = "C122BE4BBE5F93744B96FE8089DF1E257DE06593587B797E77787E322B6CD5A1"
README_FILES = ["README.md", "README.zh-TW.md", "README.en.md"]
RULE_IDS = [f"M{i:02d}" for i in range(1, 11)] + [f"Q{i:02d}" for i in range(1, 7)]


def chars(*codepoints: int) -> str:
    return "".join(chr(codepoint) for codepoint in codepoints)


PERCENTAGE_GATE = chars(56, 53, 37)
OLD_PUBLIC_NAME = chars(118, 105, 114, 97, 108, 45, 115, 99, 114, 105, 112, 116, 45, 114, 101, 109, 105, 120)


def read(relative_path: str) -> str:
    return (ROOT / relative_path).read_text(encoding="utf-8")


def png_size(path: Path) -> tuple[int, int]:
    data = path.read_bytes()
    if data[:8] != b"\x89PNG\r\n\x1a\n":
        raise AssertionError(f"Not a PNG: {path}")
    return struct.unpack(">II", data[16:24])


def jpeg_size(path: Path) -> tuple[int, int]:
    data = path.read_bytes()
    if data[:2] != b"\xff\xd8":
        raise AssertionError(f"Not a JPEG: {path}")

    offset = 2
    while offset < len(data):
        if data[offset] != 0xFF:
            offset += 1
            continue
        while offset < len(data) and data[offset] == 0xFF:
            offset += 1
        marker = data[offset]
        offset += 1
        if marker in {0xD8, 0xD9}:
            continue
        segment_length = struct.unpack(">H", data[offset : offset + 2])[0]
        if marker in {0xC0, 0xC1, 0xC2}:
            height, width = struct.unpack(">HH", data[offset + 3 : offset + 7])
            return width, height
        offset += segment_length

    raise AssertionError(f"JPEG size not found: {path}")


class PublicPackageContractTests(unittest.TestCase):
    def test_repository_tree_is_complete(self) -> None:
        required = [
            "README.md",
            "README.zh-TW.md",
            "README.en.md",
            "LICENSE",
            "NOTICE",
            "VERSION",
            ".gitignore",
            ".github/workflows/validate.yml",
            "media/banner-source.svg",
            "media/banner.png",
            "media/method-flow.svg",
            "media/method-flow.png",
            "media/wechat-qr.jpg",
            "skills/water-koubo/SKILL.md",
            "skills/water-koubo/agents/openai.yaml",
            "dist/water-koubo-v1.0.0.zip",
        ]
        for relative_path in required:
            with self.subTest(path=relative_path):
                self.assertTrue((ROOT / relative_path).is_file())
        self.assertEqual([], list((SKILL_DIR / "references").glob("*.md")))
        self.assertFalse((SKILL_DIR / "scripts" / "profile.mjs").exists())

    def test_public_name_is_water_koubo_everywhere(self) -> None:
        skill = read("skills/water-koubo/SKILL.md")
        metadata = read("skills/water-koubo/agents/openai.yaml")
        self.assertIn("name: water-koubo", skill.split("---", 2)[1])
        self.assertIn('display_name: "water-koubo"', metadata)
        self.assertIn('default_prompt: "使用 $water-koubo', metadata)
        for path in README_FILES:
            text = read(path)
            self.assertTrue(text.startswith("# water-koubo\n"), path)
            self.assertIn("waterbrojx/water-koubo", text)
            self.assertIn("$water-koubo", text)

    def test_no_old_public_name_remains(self) -> None:
        public_files = [
            *README_FILES,
            "LICENSE",
            "NOTICE",
            "VERSION",
            ".github/workflows/validate.yml",
            "media/banner-source.svg",
            "skills/water-koubo/SKILL.md",
            "skills/water-koubo/agents/openai.yaml",
        ]
        combined = "\n".join(read(path) for path in public_files)
        self.assertNotIn(OLD_PUBLIC_NAME, combined)
        self.assertNotIn(OLD_PUBLIC_NAME.upper().replace("-", " "), combined)

    def test_skill_frontmatter_has_chinese_triggers(self) -> None:
        skill = read("skills/water-koubo/SKILL.md")
        self.assertTrue(skill.startswith("---\n"))
        frontmatter = skill.split("---", 2)[1]
        keys = {
            line.split(":", 1)[0].strip()
            for line in frontmatter.splitlines()
            if ":" in line
        }
        self.assertEqual({"name", "description"}, keys)
        self.assertIn("description: Use when", frontmatter)
        for trigger in [
            "二创",
            "洗稿",
            "爆款口播",
            "完整参考稿",
        ]:
            with self.subTest(trigger=trigger):
                self.assertIn(trigger, frontmatter)
        for unsupported in ["二創", "完整參考稿", "remix", "talking-head script"]:
            with self.subTest(unsupported=unsupported):
                self.assertNotIn(unsupported, frontmatter)

    def test_openai_interface_is_short_and_implicitly_invokable(self) -> None:
        metadata = read("skills/water-koubo/agents/openai.yaml")
        self.assertIn('display_name: "water-koubo"', metadata)
        self.assertIn("给一篇完整参考稿", metadata)
        self.assertIn("allow_implicit_invocation: true", metadata)

    def test_skill_inlines_the_complete_rule_contract(self) -> None:
        text = read("skills/water-koubo/SKILL.md")
        ids = re.findall(r"^## \[(M\d{2}|Q\d{2})\]", text, re.MULTILINE)
        self.assertEqual(RULE_IDS, ids)
        self.assertNotIn(PERCENTAGE_GATE, text)
        for phrase in [
            "单一完整来源",
            "核心判断与限定",
            "因果推进",
            "开头功能",
            "案例证明",
            "爆点位置",
            "结尾意义",
            "原段落顺序",
            "新增判断",
            "前 3 段",
            "第一人称",
            "事实归属",
            "最多 5 轮",
        ]:
            with self.subTest(phrase=phrase):
                self.assertIn(phrase, text)

    def test_runtime_is_chinese_and_only_returns_three_fields(self) -> None:
        skill = read("skills/water-koubo/SKILL.md")
        required = [
            "正常成稿始终使用简体中文",
            "标题：",
            "封面文字：",
            "口播正文：",
            "不回复“收到”",
            "不显示进度",
        ]
        for phrase in required:
            with self.subTest(phrase=phrase):
                self.assertIn(phrase, skill)
        for unsupported in [
            "method.zh-CN.md",
            "method.zh-TW.md",
            "method.en.md",
            "默认跟随参考稿语言",
            "標題：",
            "Title:",
            "Cover Text:",
            "English output",
            "用户修改该文件",
            "references/method.md",
            "官方公开方法源",
        ]:
            with self.subTest(unsupported=unsupported):
                self.assertNotIn(unsupported, skill)

    def test_missing_reference_prompt_is_exact_and_chinese(self) -> None:
        skill = read("skills/water-koubo/SKILL.md")
        self.assertIn("`把完整参考稿发我。`", skill)
        self.assertIn("只回复这一句话", skill)
        self.assertNotIn("把完整參考稿發給我。", skill)
        self.assertNotIn("Send me the complete reference script.", skill)

    def test_personal_settings_feature_is_fully_absent(self) -> None:
        self.assertFalse((SKILL_DIR / "scripts" / "profile.mjs").exists())
        public_files = [*README_FILES, "NOTICE", "skills/water-koubo/SKILL.md"]
        combined = "\n".join(read(path) for path in public_files)
        for phrase in [
            "记住你的设置",
            "記住你的設定",
            "Remember your settings",
            "个人设置",
            "個人設定",
            "个人记录",
            "profile.md",
            "profile.mjs",
            "保存为我的设置",
        ]:
            with self.subTest(phrase=phrase):
                self.assertNotIn(phrase, combined)

    def test_readmes_have_complete_parallel_sections(self) -> None:
        expected_headings = {
            "README.md": [
                "water-koubo 解决什么问题",
                "快速安装",
                "能力一览",
                "怎样工作",
                "完整使用说明",
                "更新日志",
                "作者与许可证",
                "反馈",
            ],
            "README.zh-TW.md": [
                "water-koubo 解決什麼問題",
                "快速安裝",
                "能力一覽",
                "怎樣運作",
                "完整使用說明",
                "更新日誌",
                "作者與授權條款",
                "回饋",
            ],
            "README.en.md": [
                "What water-koubo helps with",
                "Quick install",
                "Capabilities",
                "How it works",
                "Full usage guide",
                "Changelog",
                "Author and license",
                "Feedback",
            ],
        }
        for path, headings in expected_headings.items():
            text = read(path)
            positions = []
            for heading in headings:
                marker = f"## {heading}"
                self.assertIn(marker, text, path)
                positions.append(text.index(marker))
            self.assertEqual(sorted(positions), positions, path)

    def test_readme_first_screen_matches_the_locked_product_story(self) -> None:
        readme = read("README.md")
        first_section = readme.split("## water-koubo 解决什么问题", 1)[0]
        ordered = [
            "# water-koubo",
            "简体中文",
            "繁體中文",
            "English",
            "短视频爆款口播二创 Skill",
            "给一篇完整参考稿，直接得到标题、封面文字和一篇可拍口播稿",
            "version-1.0.0",
            "Agent-Skills",
            "license-CC_BY--NC_4.0",
            "支持：Codex、Claude Code、WorkBuddy、DeepSeek Harness",
            "water-koubo 由老肖AI运营创建",
            "13 年互联网运营",
            "真实账号的口播内容生产",
            "快速安装",
            "能力一览",
            "怎样工作",
            "完整说明",
            "反馈",
        ]
        positions = [first_section.index(phrase) for phrase in ordered]
        self.assertEqual(sorted(positions), positions)
        self.assertNotIn("media/banner.png", first_section)
        for removed in [
            "《企业想落地AI，方向其实就两个》",
            "41.5 万曝光",
            "4.26 万观看",
            "1,374 收藏",
            "254 涨粉",
            "小红书数据截至 2026-06-26",
        ]:
            self.assertNotIn(removed, first_section)

    def test_specific_result_is_absent_and_six_capabilities_match_across_languages(self) -> None:
        retained_background = {
            "README.md": ["13 年互联网运营经验", "真实账号的口播内容生产"],
            "README.zh-TW.md": ["13 年網路營運經驗", "真實帳號的口播內容生產"],
            "README.en.md": ["13 years of internet operations experience", "used in real account production"],
        }
        for path in README_FILES:
            text = read(path)
            for phrase in retained_background[path]:
                with self.subTest(path=path, retained=phrase):
                    self.assertIn(phrase, text)
            for fact in [
                "《企业想落地AI，方向其实就两个》",
                "41.5",
                "4.26",
                "1,374",
                "2026-06-26",
                "415,408 impressions",
                "42,616 views",
                "254 followers gained",
            ]:
                with self.subTest(path=path, fact=fact):
                    self.assertNotIn(fact, text)

        capabilities = {
            "README.md": [
                "爆款逻辑不丢",
                "开头重新写",
                "内容真正二创",
                "案例归属准确",
                "补出新的爆点",
                "完整成稿一次给全",
            ],
            "README.zh-TW.md": [
                "爆款邏輯不丟",
                "開頭重新寫",
                "內容真正二創",
                "案例歸屬準確",
                "補出新的爆點",
                "完整成稿一次給全",
            ],
            "README.en.md": [
                "Keep the viral logic",
                "Rewrite the opening",
                "Create a real remix",
                "Keep cases properly attributed",
                "Add a new peak",
                "Get the full script package",
            ],
        }
        for path, labels in capabilities.items():
            section = read(path).split("## Capabilities" if path.endswith(".en.md") else "## 能力一覽" if path.endswith("zh-TW.md") else "## 能力一览", 1)[1]
            next_heading = section.find("\n## ")
            if next_heading >= 0:
                section = section[:next_heading]
            for label in labels:
                with self.subTest(path=path, label=label):
                    self.assertIn(label, section)

    def test_readmes_publish_the_same_method_flow(self) -> None:
        expected = {
            "README.md": [
                "一篇完整参考稿",
                "找出爆款写法",
                "重新创作",
                "核对归属",
                "完整成稿",
            ],
            "README.zh-TW.md": [
                "一篇完整參考稿",
                "找出爆款寫法",
                "重新創作",
                "核對歸屬",
                "完整成稿",
            ],
            "README.en.md": [
                "One complete reference script",
                "Find the viral mechanics",
                "Rewrite the script",
                "Check attribution",
                "Complete deliverables",
            ],
        }
        for path, steps in expected.items():
            text = read(path)
            self.assertIn("./media/method-flow.png", text)
            self.assertNotIn("media/method-flow.svg", text)
            heading = "## How it works" if path.endswith(".en.md") else "## 怎樣運作" if path.endswith("zh-TW.md") else "## 怎样工作"
            section = text.split(heading, 1)[1]
            next_heading = section.find("\n## ")
            if next_heading >= 0:
                section = section[:next_heading]
            positions = [section.index(step) for step in steps]
            self.assertEqual(sorted(positions), positions, path)

    def test_public_method_library_is_fully_absent(self) -> None:
        self.assertFalse((SKILL_DIR / "references" / "method.md").exists())
        forbidden = [
            "公开方法库",
            "公開方法庫",
            "Open method library",
            "公开知识库",
            "公開知識庫",
            "Public knowledge base",
            "skills/water-koubo/references/method.md",
        ]
        for path in README_FILES:
            text = read(path)
            for phrase in forbidden:
                with self.subTest(path=path, forbidden=phrase):
                    self.assertNotIn(phrase, text)

    def test_readmes_keep_actual_use_to_one_command_and_one_reference(self) -> None:
        examples = {
            "README.md": "使用 $water-koubo，把这篇完整参考稿二创成一篇可拍口播稿。",
            "README.zh-TW.md": "使用 $water-koubo，把這篇完整參考稿二創成一篇可拍的中文口播稿。",
            "README.en.md": "Use $water-koubo to turn this complete reference script into a shoot-ready Chinese talking-head script.",
        }
        for path, example in examples.items():
            with self.subTest(path=path):
                self.assertIn(example, read(path))

    def test_readmes_offer_agent_first_installation(self) -> None:
        expected = {
            "README.md": {
                "heading": "## 快速安装",
                "old_headings": ["## 快速开始", "## 安装"],
                "instruction": "帮我安装这个 Skill：https://github.com/waterbrojx/water-koubo",
                "fallback": "Agent 不支持直接安装时",
                "zip": "ZIP 导入",
            },
            "README.zh-TW.md": {
                "heading": "## 快速安裝",
                "old_headings": ["## 快速開始", "## 安裝"],
                "instruction": "幫我安裝這個 Skill：https://github.com/waterbrojx/water-koubo",
                "fallback": "Agent 不支援直接安裝時",
                "zip": "ZIP 匯入",
            },
            "README.en.md": {
                "heading": "## Quick install",
                "old_headings": ["## Quick start", "## Installation"],
                "instruction": "Install this Skill for me: https://github.com/waterbrojx/water-koubo",
                "fallback": "When your Agent cannot install directly",
                "zip": "ZIP import",
            },
        }
        command = "npx -y skills add waterbrojx/water-koubo -g --all"
        for path, contract in expected.items():
            text = read(path)
            with self.subTest(path=path):
                self.assertEqual(1, text.count(contract["heading"]))
                for old_heading in contract["old_headings"]:
                    self.assertNotIn(old_heading, text)
                self.assertEqual(1, text.count(contract["instruction"]))
                self.assertIn("<details>", text)
                self.assertIn("</details>", text)
                self.assertIn(contract["fallback"], text)
                self.assertIn(command, text)
                self.assertIn(contract["zip"], text)

    def test_readmes_offer_issue_feedback(self) -> None:
        expected = {
            "README.md": [
                "## 反馈",
                "安装失败",
                "规则冲突",
                "Agent／模型",
                "指令",
                "输出片段",
                "期望结果",
                "个人和客户信息",
            ],
            "README.zh-TW.md": [
                "## 回饋",
                "安裝失敗",
                "規則衝突",
                "Agent／模型",
                "指令",
                "輸出片段",
                "期望結果",
                "個人和客戶資訊",
            ],
            "README.en.md": [
                "## Feedback",
                "installation fails",
                "rules conflict",
                "Agent or model",
                "prompt",
                "output excerpt",
                "expected result",
                "personal and client information",
            ],
        }
        issue_url = "https://github.com/waterbrojx/water-koubo/issues/new"
        for path, phrases in expected.items():
            text = read(path)
            with self.subTest(path=path):
                self.assertIn(f"]({issue_url})", text)
                for phrase in phrases:
                    self.assertIn(phrase, text)
                self.assertIn("Waterbro_jx", text)
                self.assertIn("Skill", text)

        combined = "\n".join(read(path) for path in README_FILES)
        self.assertNotIn("安装问题、使用反馈、商业授权或合作，请添加微信", combined)
        self.assertNotIn("安裝問題、使用回饋、商業授權或合作，請加入微信", combined)

    def test_language_explanation_is_absent_from_the_frontstage(self) -> None:
        scope_files = [*README_FILES, "media/banner-source.svg"]
        if (ROOT / ".preview" / "render_readme_preview.py").is_file():
            scope_files.append(".preview/render_readme_preview.py")
        combined = "\n".join(read(path) for path in scope_files)
        for unsupported in [
            "### 语言",
            "### 語言",
            "### Language",
            "项目介绍提供简体中文",
            "專案介紹提供簡體中文",
            "Project documentation is available",
            "正常成稿使用简体中文",
            "正常成稿使用簡體中文",
            "Normal output is in Simplified Chinese",
            "三语成稿",
            "三種語言各有一份",
            "three output languages",
            "method.zh-TW.md",
            "method.en.md",
        ]:
            with self.subTest(unsupported=unsupported):
                self.assertNotIn(unsupported, combined)

    def test_removed_frontstage_copy_and_exact_commercial_line(self) -> None:
        combined = "\n".join(read(path) for path in README_FILES)
        for removed in [
            "### 必要限制",
            "### Necessary limitations",
            "正常结果不附加过程说明、评分或发布建议。",
            "正常結果不附加過程說明、評分或發佈建議。",
            "Normal results contain no process notes, scores, or publishing advice.",
            "提供简体中文、繁體中文和 English 三套项目介绍",
        ]:
            self.assertNotIn(removed, combined)
        readme = read("README.md")
        exact = "短视频获客、代运营、收费培训或收费产品等商业使用，需要老肖AI运营单独授权；"
        self.assertIn(exact, readme)
        self.assertNotIn("变现账号、企业营销、获客、代运营", readme)

    def test_frontstage_copy_has_no_backstage_terms_or_contrast_template(self) -> None:
        combined = "\n".join(read(path) for path in README_FILES)
        forbidden = [
            "内部流程",
            "内部拆解",
            "内部分析",
            "回放",
            "验收",
            "子代理",
            "会话 A/B",
            "信息块",
            "置换",
            "合同测试",
            "內部流程",
            "內部拆解",
            "驗收",
            "子代理",
            "session A/B",
            "sub-agent",
            "internal workflow",
        ]
        for phrase in forbidden:
            with self.subTest(phrase=phrase):
                self.assertNotIn(phrase.lower(), combined.lower())
        self.assertIsNone(re.search(r"不是.{0,80}而是", combined, re.DOTALL))
        self.assertIsNone(re.search(r"並非.{0,80}而是", combined, re.DOTALL))
        self.assertIsNone(re.search(r"\bnot\b.{0,100}\bbut\b", combined, re.IGNORECASE | re.DOTALL))

    def test_author_license_and_repository_links_match_across_languages(self) -> None:
        for path in README_FILES:
            text = read(path)
            for phrase in [
                "老肖AI运营",
                "Waterbro_jx",
                "media/wechat-qr.jpg",
                "CC BY-NC 4.0",
                "waterbrojx/water-koubo",
            ]:
                with self.subTest(path=path, phrase=phrase):
                    self.assertIn(phrase, text)

    def test_qr_code_uses_compact_display_width_across_languages(self) -> None:
        for path in README_FILES:
            text = read(path)
            with self.subTest(path=path):
                self.assertEqual(1, text.count('src="./media/wechat-qr.jpg"'))
                self.assertEqual(1, text.count('width="240"'))
        if (ROOT / ".preview" / "README.html").is_file():
            preview = read(".preview/README.html")
            self.assertIn('src="../media/wechat-qr.jpg"', preview)
            self.assertIn('width="240"', preview)
            self.assertNotIn('&lt;img src="./media/wechat-qr.jpg"', preview)

    def test_public_text_has_no_private_runtime_leakage(self) -> None:
        public_files = [
            *README_FILES,
            "LICENSE",
            "NOTICE",
            "VERSION",
            ".gitignore",
            ".github/workflows/validate.yml",
            "media/banner-source.svg",
            "skills/water-koubo/SKILL.md",
            "skills/water-koubo/agents/openai.yaml",
        ]
        combined = "\n".join(read(path) for path in public_files)
        forbidden = [
            PERCENTAGE_GATE,
            chr(70) + ":" + chr(92),
            chars(67, 58, 92, 85, 115, 101, 114, 115, 92, 119, 97, 116, 101, 114),
            chars(30693, 35782, 26143, 29699),
            chars(87, 97, 116, 101, 114, 32, 19994, 21153),
            chars(79, 98, 115, 105, 100, 105, 97, 110),
            chars(82, 50, 48, 50),
            chars(68, 89, 45, 48, 48, 51),
            chars(109, 105, 115, 115, 105, 111, 110, 32, 112, 97, 99, 107),
            chars(114, 117, 110, 112, 97, 99, 107),
            chars(32032, 26448, 21345),
            chars(36807, 31243, 21345),
            chars(68, 101, 101, 112, 83, 101, 101, 107, 32, 86, 52, 32, 80, 82, 79),
        ]
        for marker in forbidden:
            with self.subTest(marker=marker):
                self.assertNotIn(marker, combined)

    def test_brand_assets_are_exact_and_renderable(self) -> None:
        qr = ROOT / "media" / "wechat-qr.jpg"
        digest = hashlib.sha256(qr.read_bytes()).hexdigest().upper()
        self.assertEqual(QR_SHA256, digest)
        self.assertEqual((720, 720), jpeg_size(qr))
        self.assertEqual((1280, 640), png_size(ROOT / "media" / "banner.png"))
        self.assertEqual((1600, 900), png_size(ROOT / "media" / "method-flow.png"))

        source = read("media/banner-source.svg")
        for exact_text in [
            "water-koubo",
            "爆款口播二创 Skill",
            "给一篇完整参考稿，直接得到一篇可拍口播稿",
            "老肖AI运营",
        ]:
            self.assertIn(exact_text, source)
        self.assertNotRegex(source, r"不是.{0,80}而是")

        flow = read("media/method-flow.svg")
        for exact_text in [
            "一篇完整参考稿",
            "找出爆款写法",
            "重新创作",
            "核对归属",
            "完整成稿",
        ]:
            self.assertIn(exact_text, flow)

    def test_all_readme_local_links_exist(self) -> None:
        for readme_path in README_FILES:
            links = re.findall(r"!?\[[^\]]*\]\(([^)]+)\)", read(readme_path))
            for target in links:
                if target.startswith(("http://", "https://", "#")):
                    continue
                local_target = target.split("#", 1)[0]
                with self.subTest(readme=readme_path, target=local_target):
                    self.assertTrue((ROOT / local_target).exists())

    def test_release_zip_has_direct_import_structure(self) -> None:
        archive = ROOT / "dist" / "water-koubo-v1.0.0.zip"
        expected = {
            "water-koubo/SKILL.md",
            "water-koubo/agents/openai.yaml",
        }
        with zipfile.ZipFile(archive) as package:
            files = {name for name in package.namelist() if not name.endswith("/")}
            self.assertEqual(expected, files)
            for relative in expected:
                source = "skills/" + relative
                self.assertEqual(read(source), package.read(relative).decode("utf-8"))

    @unittest.skipUnless((ROOT / ".preview").is_dir(), "local preview files are intentionally untracked")
    def test_local_previews_cover_all_three_languages(self) -> None:
        previews = [
            ".preview/github-preview.zh-CN.png",
            ".preview/github-preview.zh-TW.png",
            ".preview/github-preview.en.png",
        ]
        for path in previews:
            with self.subTest(path=path):
                width, height = png_size(ROOT / path)
                self.assertEqual(1440, width)
                self.assertGreaterEqual(height, 4000)

    @unittest.skipUnless((ROOT / ".preview").is_dir(), "local preview files are intentionally untracked")
    def test_preview_renderer_uses_the_real_readmes_as_its_source(self) -> None:
        source = read(".preview/render_readme_preview.py")
        for path in README_FILES:
            self.assertIn(path, source)
        self.assertIn("read_text", source)
        for hardcoded_copy_store in ["PAGES =", "cap_lines", "knowledge_text", "profile_text"]:
            self.assertNotIn(hardcoded_copy_store, source)


if __name__ == "__main__":
    unittest.main()
