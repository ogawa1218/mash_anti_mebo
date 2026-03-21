import ArticleCard from "./ArticleCard";

// サンプル記事データ
const sampleArticles = [
    {
        slug: "how-to-start-diet-for-metabo",
        title: "【完全版】40代メタボおじさんのダイエット始め方ガイド",
        excerpt:
            "健康診断でE判定を食らったあなたへ。まずやるべきことは過激な食事制限ではない。「続けられる仕組み」を作ることだ。",
        date: "2026年1月15日",
        category: "入門",
    },
    {
        slug: "breakfast-routine",
        title: "朝食を「仕組み化」したら、何も考えずに痩せ始めた話",
        excerpt:
            "毎朝同じメニューにしたら、決断疲れがなくなって自然と食事管理ができるようになった。具体的なメニューを公開。",
        date: "2026年1月12日",
        category: "食事",
    },
    {
        slug: "walking-10000-steps",
        title: "1日1万歩を「無理なく」達成する5つの工夫",
        excerpt:
            "運動嫌いの俺が毎日1万歩を歩けるようになったのは、意志の力ではなく環境を変えたから。通勤ルートの変更が鍵だった。",
        date: "2026年1月10日",
        category: "運動",
    },
    {
        slug: "protein-for-beginners",
        title: "プロテイン、結局どれを買えばいいのか問題に終止符を打つ",
        excerpt:
            "種類が多すぎてわからん！という人のために、俺が実際に飲んで続けられたプロテインを3つだけ紹介する。",
        date: "2026年1月8日",
        category: "食事",
    },
    {
        slug: "cheat-day-strategy",
        title: "チートデイは必要か？100kg→68kgになった俺の結論",
        excerpt:
            "週1でラーメンを食べていたが、それでも痩せた。大事なのは頻度と量のコントロール。具体的なルールを解説。",
        date: "2026年1月5日",
        category: "マインド",
    },
    {
        slug: "sleep-and-diet",
        title: "睡眠を軽視していた俺が、体重停滞を突破した方法",
        excerpt:
            "痩せなくなった原因は食事でも運動でもなく、睡眠だった。7時間睡眠を確保したら、また体重が落ち始めた。",
        date: "2026年1月3日",
        category: "生活習慣",
    },
];

export default function ArticleList() {
    return (
        <section className="bg-gray-50 py-12 md:py-16">
            <div className="mx-auto max-w-6xl px-4">
                <h2 className="mb-8 text-center text-xl font-bold text-gray-900 md:text-2xl">
                    新着記事
                </h2>

                <div className="grid gap-6 sm:grid-cols-2 lg:grid-cols-3">
                    {sampleArticles.map((article) => (
                        <ArticleCard key={article.slug} {...article} />
                    ))}
                </div>

                <div className="mt-10 text-center">
                    <a href="/articles" className="btn-secondary">
                        記事一覧を見る →
                    </a>
                </div>
            </div>
        </section>
    );
}
