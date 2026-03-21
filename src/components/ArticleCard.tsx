import Link from "next/link";

interface ArticleCardProps {
    slug: string;
    title: string;
    excerpt: string;
    date: string;
    category?: string;
}

export default function ArticleCard({
    slug,
    title,
    excerpt,
    date,
    category,
}: ArticleCardProps) {
    return (
        <article className="group overflow-hidden rounded-lg bg-white shadow-md transition-all hover:shadow-xl">
            {/* サムネイルプレースホルダー */}
            <div className="aspect-video bg-gray-200">
                <div className="flex h-full items-center justify-center">
                    <span className="text-sm text-gray-400">記事サムネイル</span>
                </div>
            </div>

            <div className="p-5">
                {/* カテゴリー */}
                {category && (
                    <span className="mb-2 inline-block rounded bg-primary-700 px-2 py-1 text-xs font-bold text-white">
                        {category}
                    </span>
                )}

                {/* タイトル */}
                <h3 className="mb-2 text-lg font-bold leading-tight text-gray-900 group-hover:text-primary-700">
                    <Link href={`/articles/${slug}`} className="hover:no-underline">
                        {title}
                    </Link>
                </h3>

                {/* 概要 */}
                <p className="mb-3 line-clamp-2 text-sm leading-relaxed text-gray-600">
                    {excerpt}
                </p>

                {/* 日付 */}
                <time className="text-xs text-gray-400">{date}</time>
            </div>
        </article>
    );
}
