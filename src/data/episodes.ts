export type Episode = {
    slug: string;
    episodeNumber: number;
    title: string;
    excerpt: string;
    date: string;
    category: string;
};

const episodes: Episode[] = [
    {
        slug: "episode-31",
        episodeNumber: 31,
        title: "食後10分歩くだけで血糖はどこまで変わるのか",
        excerpt:
            "食後に座りっぱなしのループを断ち切る最小の習慣。10分歩行が血糖ピークを抑える理由を研究と実体験で整理する。",
        date: "2026年3月19日",
        category: "運動",
    },
    {
        slug: "episode-32",
        episodeNumber: 32,
        title: "100kg→68kg、5年リバウンドなしで分かった1つの真実",
        excerpt:
            "最強のダイエットは「痩せる方法」ではなく「戻る仕組み」を持つこと。なぜ完璧主義が一番危ないのかを解説する。",
        date: "2026年3月19日",
        category: "マインド",
    },
    {
        slug: "episode-33",
        episodeNumber: 33,
        title: "量より頻度。30分かけて5日で体は変わる",
        excerpt:
            "週1回の長時間運動より週5回の短時間運動が持続しやすい理由。頻度を上げることで体が変わり始めるメカニズムを解説。",
        date: "2026年3月19日",
        category: "運動",
    },
    {
        slug: "episode-34",
        episodeNumber: 34,
        title: "筋トレは筋肉のためだけじゃない",
        excerpt:
            "筋トレが代謝・ホルモン・メンタルにまで影響する理由。筋肉以外のメリットを知ると、継続する動機が変わってくる。",
        date: "2026年3月20日",
        category: "運動",
    },
    {
        slug: "episode-35",
        episodeNumber: 35,
        title: "もう手遅れなんて言わせない",
        excerpt:
            "40代・50代から始めても体は変わる。「もう遅い」という思い込みが最大の障壁であることを、科学的根拠で覆す。",
        date: "2026年3月20日",
        category: "マインド",
    },
    {
        slug: "episode-36",
        episodeNumber: 36,
        title: "断食は万能じゃない",
        excerpt:
            "ファスティングが流行しているが、メタボ改善に万能ではない理由。向いている人・向かない人の違いと正しい活用法を解説。",
        date: "2026年3月20日",
        category: "食事",
    },
    {
        slug: "episode-37",
        episodeNumber: 37,
        title: "朝7時台の運動は同じ運動でも差が出るのか",
        excerpt:
            "運動の時間帯は体脂肪燃焼に影響するのか。朝の運動タイミングと体内時計の関係を研究ベースで整理する。",
        date: "2026年3月20日",
        category: "運動",
    },
    {
        slug: "episode-38",
        episodeNumber: 38,
        title: "筋トレは週2で十分、続く形が最強だった",
        excerpt:
            "毎日やらなくていい。週2回で筋肉を維持・増加できる根拠と、忙しい会社員でも続く筋トレ設計の具体例を紹介。",
        date: "2026年3月20日",
        category: "運動",
    },
    {
        slug: "episode-39",
        episodeNumber: 39,
        title: "朝の運動は時間より固定が勝つ",
        excerpt:
            "何時にやるかより「毎日同じ時間」にやることが習慣化の鍵。朝運動を定着させるための時間固定の設計法。",
        date: "2026年3月20日",
        category: "運動",
    },
    {
        slug: "episode-40",
        episodeNumber: 40,
        title: "タンパク質は「量」より「タイミング」で変わる",
        excerpt:
            "プロテインを飲む量より、いつ飲むかで筋肉への効果は大きく変わる。食事タイミングとタンパク質摂取の最適解を解説。",
        date: "2026年3月21日",
        category: "食事",
    },
    {
        slug: "episode-41",
        episodeNumber: 41,
        title: "内臓脂肪が落ちやすい食べ方、3つのポイント",
        excerpt:
            "皮下脂肪より内臓脂肪の方が実は落ちやすい。食事の順番・速さ・量のコントロールで内臓脂肪を効率よく減らす方法。",
        date: "2026年3月22日",
        category: "食事",
    },
    {
        slug: "episode-42",
        episodeNumber: 42,
        title: "血圧を下げる習慣、薬に頼る前にできること",
        excerpt:
            "健診で血圧を指摘された人へ。減塩・運動・睡眠の組み合わせで血圧は変わる。薬の前にできる生活習慣の改善策。",
        date: "2026年3月23日",
        category: "生活習慣",
    },
    {
        slug: "episode-43",
        episodeNumber: 43,
        title: "糖化が老化を加速する。AGEsを増やさない食べ方",
        excerpt:
            "糖化（AGEs）は肌・血管・臓器の老化を加速する。糖化を防ぐ食べ方の工夫と、日常で意識すべきポイントを整理。",
        date: "2026年3月24日",
        category: "食事",
    },
    {
        slug: "episode-44",
        episodeNumber: 44,
        title: "健診結果の正しい読み方。E判定を逆転させた視点",
        excerpt:
            "健診の数値は「警告」ではなく「現在地」。E判定からの逆転に必要な、数値の正しい読み方と優先順位の付け方。",
        date: "2026年3月25日",
        category: "入門",
    },
];

export default episodes;
