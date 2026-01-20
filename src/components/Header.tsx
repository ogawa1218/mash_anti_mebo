"use client";

import Link from "next/link";
import { useState } from "react";

export default function Header() {
    const [isMenuOpen, setIsMenuOpen] = useState(false);

    return (
        <header className="sticky top-0 z-50 bg-primary-800 shadow-lg">
            <div className="mx-auto max-w-6xl px-4">
                <div className="flex h-16 items-center justify-between md:h-20">
                    {/* ロゴ */}
                    <Link
                        href="/"
                        className="text-lg font-bold text-white hover:text-gray-200 hover:no-underline md:text-xl"
                    >
                        健康診断E判定からの逆襲
                    </Link>

                    {/* デスクトップナビ */}
                    <nav className="hidden items-center gap-6 md:flex">
                        <Link
                            href="/"
                            className="text-sm font-medium text-white/90 hover:text-white hover:no-underline"
                        >
                            ホーム
                        </Link>
                        <Link
                            href="/articles"
                            className="text-sm font-medium text-white/90 hover:text-white hover:no-underline"
                        >
                            記事一覧
                        </Link>
                        <Link
                            href="/about"
                            className="text-sm font-medium text-white/90 hover:text-white hover:no-underline"
                        >
                            このブログについて
                        </Link>
                        <a
                            href="https://note.com/"
                            target="_blank"
                            rel="noopener noreferrer"
                            className="btn-primary text-sm"
                        >
                            ロードマップ（Note）を読む
                        </a>
                    </nav>

                    {/* モバイルメニューボタン */}
                    <div className="flex items-center gap-3 md:hidden">
                        <a
                            href="https://note.com/"
                            target="_blank"
                            rel="noopener noreferrer"
                            className="btn-primary px-3 py-2 text-xs"
                        >
                            Note
                        </a>
                        <button
                            onClick={() => setIsMenuOpen(!isMenuOpen)}
                            className="p-2 text-white"
                            aria-label="メニューを開く"
                        >
                            <svg
                                className="h-6 w-6"
                                fill="none"
                                stroke="currentColor"
                                viewBox="0 0 24 24"
                            >
                                {isMenuOpen ? (
                                    <path
                                        strokeLinecap="round"
                                        strokeLinejoin="round"
                                        strokeWidth={2}
                                        d="M6 18L18 6M6 6l12 12"
                                    />
                                ) : (
                                    <path
                                        strokeLinecap="round"
                                        strokeLinejoin="round"
                                        strokeWidth={2}
                                        d="M4 6h16M4 12h16M4 18h16"
                                    />
                                )}
                            </svg>
                        </button>
                    </div>
                </div>

                {/* モバイルメニュー */}
                {isMenuOpen && (
                    <nav className="border-t border-white/20 py-4 md:hidden">
                        <div className="flex flex-col gap-4">
                            <Link
                                href="/"
                                className="text-sm font-medium text-white/90 hover:text-white hover:no-underline"
                                onClick={() => setIsMenuOpen(false)}
                            >
                                ホーム
                            </Link>
                            <Link
                                href="/articles"
                                className="text-sm font-medium text-white/90 hover:text-white hover:no-underline"
                                onClick={() => setIsMenuOpen(false)}
                            >
                                記事一覧
                            </Link>
                            <Link
                                href="/about"
                                className="text-sm font-medium text-white/90 hover:text-white hover:no-underline"
                                onClick={() => setIsMenuOpen(false)}
                            >
                                このブログについて
                            </Link>
                        </div>
                    </nav>
                )}
            </div>
        </header>
    );
}
