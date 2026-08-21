# 孫の手 ／ Magonote

痒い所に手が届く、ちょっとした便利道具の詰め合わせポータル。

**公開URL:** https://choppermoon1623-tech.github.io/magonote/
**説明書:** https://choppermoon1623-tech.github.io/magonote/manual.html （全アプリの使い方ガイド。`manual.html`）

## コンセプト

「やりたいことは一瞬なのに、いざ探すと会員登録・アップロード・広告・透かしが待っている」──
その小さな面倒をなくすための道具置き場。

収録の基準は3つ。

1. **端末内で完結する**（アップロード不要 = 校務で扱うファイルも安心）
2. **起動3秒・操作3ステップで終わる**
3. **専用ソフトを入れるほどではない規模**

## 収録中

| 道具 | かゆい所 |
|---|---|
| [PDFツール](https://choppermoon1623-tech.github.io/pdf-tool/) | 紙に印刷して直して、また取り込む…をやめたい |
| [画像形式変換](https://choppermoon1623-tech.github.io/image-convert/) | iPhoneの写真（HEIC）がパソコンで開けない |
| [写真リサイザー](https://choppermoon1623-tech.github.io/photo-resizer/) | 添付できる容量を超えてしまった |
| [大型タイマー](https://choppermoon1623-tech.github.io/big-timer/) | グループ活動の残り時間を全員に見せたい |
| [QR提出チェック](https://choppermoon1623-tech.github.io/submit-check/) | 誰が出していないか、名簿と突き合わせて数えるのが大変 |
| [QRコード工房](https://choppermoon1623-tech.github.io/qr-studio/) | QRを1個作りたいだけなのに、生成サイトは広告と透かしだらけ |
| [テキスト整形](https://choppermoon1623-tech.github.io/text-formatter/) | PDFからコピーした文章が変な改行だらけ |
| [班分けメーカー](https://choppermoon1623-tech.github.io/group-maker/) | 配慮しながらの班分けが毎回パズルになっている |
| [差し込み印刷](https://choppermoon1623-tech.github.io/mail-merge/) | 賞状の名前を1枚ずつ手で打ち替えている |
| [当番表メーカー](https://choppermoon1623-tech.github.io/toban-maker/) | 学期はじめのたびに当番表を画用紙で手作りしている |
| [トーナメント・対戦表](https://choppermoon1623-tech.github.io/tournament-maker/) | 球技大会のトーナメントの線を毎回手描きしている |
| [ふりがな付け](https://choppermoon1623-tech.github.io/furigana/) | 低学年や外国籍の子向けのおたよりに、ルビを1つずつ振っている |
| [週時間割メーカー](https://choppermoon1623-tech.github.io/jikanwari-maker/) | 先生の予定を突き合わせながらの週時間割づくりに毎週何時間もかかっている |

## 道具を増やすとき

1. `C:\Users\USER\dev\apps\<repo名>\` にアプリを作り、GitHub Pages で公開する
2. このリポジトリの `index.html` の該当カテゴリに `a.card` を1つ足す
   （`.nm` = 名前、`.ds` = 説明、`.itch` = 解消される「かゆい所」）
3. カテゴリごとの件数バッジと検索は自動で追従します
4. 説明書も更新する：`manual-src/` の該当mdに「## アプリ名／ひとこと／使い方／便利機能／注意・コツ」を追記し、
   `build_manual.py` のカテゴリ表（CATS）にアイコン・名前・repo名を足して `python build_manual.py` を実行すると
   `manual.html` が再生成されます

[H.M Works アプリポータル](https://choppermoon1623-tech.github.io/HMWorks/) のサブポータルです。
