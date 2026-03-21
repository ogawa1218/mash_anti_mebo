import Link from "next/link";

export default function Footer() {
    return (
        <footer className="bg-primary-900 text-white">
            <div className="mx-auto max-w-6xl px-4 py-12">
                <div className="grid gap-8 md:grid-cols-3">
                    {/* ブログ情報 */}
                    <div>
                        <h3 className="mb-4 text-lg font-bold text-white">
                            健康診断E判定からの逆襲
                        </h3>
                        <p className="text-sm leading-relaxed text-white/80">
                            30代・40代のメタボ男性に向けた、実直で信頼できるダイエット情報を発信しています。
                        </p>
                    </div>

                    {/* リンク */}
                    <div>
                        <h4 className="mb-4 text-sm font-bold text-white">メニュー</h4>
                        <ul className="space-y-2 text-sm">
                            <li>
                                <Link
                                    href="/"
                                    className="text-white/80 hover:text-white hover:no-underline"
                                >
                                    ホーム
                                </Link>
                            </li>
                            <li>
                                <Link
                                    href="/articles"
                                    className="text-white/80 hover:text-white hover:no-underline"
                                >
                                    記事一覧
                                </Link>
                            </li>
                            <li>
                                <Link
                                    href="/about"
                                    className="text-white/80 hover:text-white hover:no-underline"
                                >
                                    このブログについて
                                </Link>
                            </li>
                        </ul>
                    </div>

                    {/* CTA */}
                    <div>
                        <h4 className="mb-4 text-sm font-bold text-white">無料で学ぶ</h4>
                        <p className="mb-4 text-sm text-white/80">
                            デブ卒業への具体的なロードマップを公開中
                        </p>
                        <a
                            href="https://note.com/"
                            target="_blank"
                            rel="noopener noreferrer"
                            className="btn-primary inline-block text-sm"
                        >
                            ロードマップを読む
                        </a>
                    </div>
                </div>

                <div className="mt-12 border-t border-white/20 pt-8 text-center">
                    <p className="text-sm text-white/60">
                        © {new Date().getFullYear()} 健康診断E判定からの逆襲. All rights
                        reserved.
                    </p>
                </div>
            </div>
        </footer>
    );
}
