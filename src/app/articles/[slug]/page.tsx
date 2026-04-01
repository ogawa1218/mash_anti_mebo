import type { Metadata } from "next";
import CTASection from "@/components/CTASection";
import PointBox from "@/components/PointBox";
import Link from "next/link";
import episodes from "@/data/episodes";

// サンプル記事データ（実際はCMSやMDXから取得）
const articleData: Record<
    string,
    {
        title: string;
        date: string;
        category: string;
        content: React.ReactNode;
    }
> = {
    "how-to-start-diet-for-metabo": {
        title: "【完全版】40代メタボおじさんのダイエット始め方ガイド",
        date: "2026年1月15日",
        category: "入門",
        content: (
            <>
                <p>
                    健康診断でE判定を食らったあなたへ。
                    <br />
                    おめでとう、ここからがスタートだ。
                </p>

                <h2>まずやるべきことは「過激な制限」ではない</h2>

                <p>
                    多くの人が最初にやりがちなのが、いきなり糖質制限やファスティング。
                    <br />
                    気持ちはわかる。俺もそうだった。
                </p>

                <p>
                    でも、それは<strong>続かない</strong>。
                    <br />
                    1週間で挫折して、リバウンドして、自己嫌悪に陥る。
                    <br />
                    その繰り返しだった。
                </p>

                <PointBox>
                    <p>
                        <strong>最初の1ヶ月は「記録」だけでいい。</strong>
                        <br />
                        何を食べたか、体重はいくつか。
                        <br />
                        それを毎日メモするだけで、自然と意識が変わる。
                    </p>
                </PointBox>

                <h2>「仕組み化」の第一歩：朝食の固定</h2>

                <p>
                    俺が最初にやったのは、朝食を完全に固定すること。
                    <br />
                    毎朝同じものを食べる。考えない。決断しない。
                </p>

                <p>
                    これだけで、1日の決断疲れが激減した。
                    <br />
                    昼と夜の食事も自然とコントロールできるようになる。
                </p>

                <h3>具体的な朝食メニュー</h3>

                <ul className="list-disc pl-6 space-y-2 my-4">
                    <li>プロテイン（水で溶かす）</li>
                    <li>ゆで卵 2個</li>
                    <li>バナナ 1本</li>
                </ul>

                <p>
                    以上。これを毎日食べる。
                    <br />
                    カロリーは約400kcal、タンパク質は約40g取れる。
                </p>

                <h2>次にやること</h2>

                <p>
                    朝食の固定に慣れたら、次は「歩く習慣」を作る。
                    <br />
                    詳しくは次の記事で解説している。
                </p>
            </>
        ),
    },
};

// エピソードデータからスタブ記事を生成
const episodeArticleData = Object.fromEntries(
    episodes.map((ep) => [
        ep.slug,
        {
            title: `第${ep.episodeNumber}回｜${ep.title}`,
            date: ep.date,
            category: ep.category,
            content: (
                <>
                    <p>{ep.excerpt}</p>
                    <PointBox>
                        <p>
                            <strong>この記事はPodcast「Longevity Navigator」第{ep.episodeNumber}回の内容をnote記事化したものです。</strong>
                        </p>
                    </PointBox>
                    <h2>内容は準備中です</h2>
                    <p>
                        詳細な記事コンテンツは順次公開予定です。
                        <br />
                        stand.fmでPodcastをお聴きいただけます。
                    </p>
                </>
            ),
        },
    ])
);

// 全記事データをマージ
const allArticleData = { ...articleData, ...episodeArticleData };

// メタデータ生成
export async function generateMetadata({
    params,
}: {
    params: Promise<{ slug: string }>;
}): Promise<Metadata> {
    const { slug } = await params;
    const article = allArticleData[slug];

    if (!article) {
        return {
            title: "記事が見つかりません | 健康診断E判定からの逆襲",
        };
    }

    return {
        title: `${article.title} | 健康診断E判定からの逆襲`,
        description: `${article.title}についての詳細な解説記事`,
    };
}

export default async function ArticlePage({
    params,
}: {
    params: Promise<{ slug: string }>;
}) {
    const { slug } = await params;
    const article = allArticleData[slug];

    // 記事が見つからない場合
    if (!article) {
        return (
            <div className="mx-auto max-w-3xl px-4 py-16 text-center">
                <h1 className="mb-4 text-2xl font-bold">記事が見つかりません</h1>
                <p className="mb-8 text-gray-600">
                    お探しの記事は存在しないか、削除された可能性があります。
                </p>
                <Link href="/" className="btn-primary">
                    トップページへ戻る
                </Link>
            </div>
        );
    }

    return (
        <>
            {/* 記事ヘッダー */}
            <header className="bg-primary-800 py-12 md:py-16">
                <div className="mx-auto max-w-3xl px-4">
                    <span className="mb-4 inline-block rounded bg-accent-500 px-3 py-1 text-sm font-bold text-white">
                        {article.category}
                    </span>
                    <h1 className="text-2xl font-bold leading-tight text-white md:text-3xl lg:text-4xl">
                        {article.title}
                    </h1>
                    <time className="mt-4 block text-sm text-white/70">{article.date}</time>
                </div>
            </header>

            {/* 記事本文 */}
            <article className="mx-auto max-w-3xl px-4 py-12">
                <div className="prose prose-lg max-w-none">{article.content}</div>
            </article>

            {/* CTA（フッター直前） */}
            <CTASection />
        </>
    );
}
