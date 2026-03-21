export default function HeroSection() {
    return (
        <section className="bg-gradient-to-br from-primary-800 via-primary-900 to-primary-800 py-16 md:py-24">
            <div className="mx-auto max-w-4xl px-4 text-center">
                {/* メインキャッチコピー */}
                <h1 className="mb-6 text-2xl font-black leading-tight text-white md:text-4xl lg:text-5xl">
                    <span className="block text-accent-500">健康診断E判定、</span>
                    <span className="block">腹囲91cmの屈辱から。</span>
                </h1>

                <p className="mx-auto mb-8 max-w-2xl text-lg font-bold leading-relaxed text-white/90 md:text-xl">
                    100kgの男が
                    <span className="text-accent-400">『仕組み化』</span>
                    だけでシックスパックを手に入れた全記録
                </p>

                {/* CTA */}
                <a
                    href="https://note.com/"
                    target="_blank"
                    rel="noopener noreferrer"
                    className="btn-primary text-lg md:text-xl"
                >
                    ロードマップ（Note）を読む →
                </a>
            </div>
        </section>
    );
}
