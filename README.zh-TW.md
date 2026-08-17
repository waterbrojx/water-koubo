# water-koubo

[简体中文](README.md) | 繁體中文 | [English](README.en.md)

> 短影音爆款口播二創 Skill。
>
> 給一篇完整參考稿，直接得到標題、封面文字和一篇可拍口播稿。

![version](https://img.shields.io/badge/version-1.0.0-blue) ![Agent Skills](https://img.shields.io/badge/Agent-Skills-black) ![license](https://img.shields.io/badge/license-CC_BY--NC_4.0-green)

**支援：Codex、Claude Code、WorkBuddy、DeepSeek Harness，以及其他能夠讀取 Skills 的 Agent。**

water-koubo 由老肖AI运营建立。老肖把 13 年網路營運經驗裡一直在用的口播二創方法，整理成了這個 Skill。這套方法已經用於真實帳號的口播內容生產。

[快速開始](#快速開始) · [能力一覽](#能力一覽) · [怎樣運作](#怎樣運作) · [安裝](#安裝) · [完整說明](#完整使用說明)

![water-koubo 演示流程圖](./media/method-flow.png)

## water-koubo 解決什麼問題

把一篇爆款參考稿交給 water-koubo。它會保住原稿的觀點、結構、案例和爆點，重寫開頭、判斷、句子和細節，校準經歷與案例歸屬，一次給你標題、封面文字和完整口播正文。

適合手上已經有完整參考稿，想快速二創成自己能拍內容的創作者。

## 快速開始

安裝完成後，在支援 Skills 的 Agent 中輸入：

~~~text
$water-koubo
【貼上或附上一份完整中文參考稿】
幫我二創成一篇可拍的中文口播稿。
~~~

參考稿完整可讀時，water-koubo 會直接交付成稿。

## 能力一覽

| 能力 | 你能得到什麼 |
|---|---|
| **爆款邏輯不丟** | 抓住原稿最有價值的觀點、結構、案例和爆點 |
| **開頭重新寫** | 換一個新的開場，讓第一句話更抓人 |
| **內容真正二創** | 重寫判斷、句子和細節，讓成稿有新的資訊和表達 |
| **案例歸屬準確** | 誰的經歷寫誰，參考稿裡的親歷不會變成你的親歷 |
| **補出新的爆點** | 前段加進一個新的判斷，讓內容更有記憶點 |
| **完整成稿一次給全** | 標題、封面文字和口播正文一次交付 |

成稿讀起來順、拿起來能拍，事實和歸屬也對得上。

## 怎樣運作

water-koubo 會按五步完成一篇二創稿：

1. **一篇完整參考稿**：讀取原稿和你這次提出的要求。
2. **找出爆款寫法**：抓住觀點、結構、案例、爆點和結尾。
3. **重新創作**：重寫開頭、判斷、句子和細節。
4. **核對歸屬**：檢查事實、案例和經歷分別屬於誰。
5. **完整成稿**：交付標題、封面文字和口播正文。

## 安裝

在終端執行：

~~~bash
npx -y skills add waterbrojx/water-koubo -g --all
~~~

安裝後回到支援 Skills 的 Agent，使用 **$water-koubo** 加一篇完整參考稿即可開始。ZIP 匯入時選擇 **skills/water-koubo** 目錄。

目前版本：**1.0.0 / Unreleased**。首次公開日期會在正式發佈前寫入。

## 完整使用說明

### 輸入

- 每次提供一篇完整參考稿；
- 支援直接貼上文字，以及宿主能夠完整讀取的 TXT、Markdown、Word 和可選取文字的 PDF；
- 檔案無法完整讀取時，補充一份完整參考稿即可。

### 輸出

~~~text
標題：

封面文字：

口播正文：
~~~

安裝問題、使用回饋、商業授權或合作，請加入微信 **Waterbro_jx**，備註 **Skill**。

## 更新日誌

### 1.0.0 · Unreleased

- 首次發佈 water-koubo；
- 給一篇完整參考稿，直接生成標題、封面文字和可拍口播正文；
- 加入完整演示流程圖。

## 作者與授權條款

**老肖AI运营｜微信：Waterbro_jx**

<img src="./media/wechat-qr.jpg" alt="老肖AI运营微信二維碼" width="240">

商業授權或合作請備註 **Skill**。

本專案採用 [CC BY-NC 4.0](https://creativecommons.org/licenses/by-nc/4.0/deed.zh-hant)：

- 非商業使用免費；
- 短影音獲客、代營運、收費培訓或收費產品等商業使用，需要老肖AI运营另行授權；
- 再發佈或修改專案材料，必須保留署名、授權條款與修改說明；
- 使用 Skill 生成的稿件無需顯示「老肖AI运营」署名，商業使用仍需授權；
- 「老肖AI运营」品牌、橫幅、微信二維碼及其組合版式另行保留權利。

詳細條款見 [LICENSE](LICENSE) 與 [NOTICE](NOTICE)。官方專案地址：[waterbrojx/water-koubo](https://github.com/waterbrojx/water-koubo)。
