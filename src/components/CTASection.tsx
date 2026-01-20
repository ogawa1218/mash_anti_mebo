export default function CTASection() {
    return (
        <section className="bg-gradient-to-r from-accent-600 to-accent-500 py-12 md:py-16">
            <div className="mx-auto max-w-3xl px-4 text-center">
                <h2 className="mb-4 text-2xl font-black text-white md:text-3xl">
                    デブ卒業への第一歩
                </h2>

                <p className="mb-6 text-lg leading-relaxed text-white/90">
                    100kgから68kgになった具体的なロードマップを公開中。
                    <br className="hidden md:block" />
                    意志の力に頼らない「仕組み化ダイエット」の全貌がここに。
                </p>

                <a
                    href="https://note.com/"
                    target="_blank"
                    rel="noopener noreferrer"
                    className="inline-flex items-center justify-center gap-2 rounded-lg bg-white px-8 py-4 text-lg font-bold text-accent-600 shadow-lg transition-all hover:-translate-y-1 hover:shadow-xl"
                >
                    デブ卒業への第一歩はこちら →
                </a>

                <p className="mt-4 text-sm text-white/70">
                    ※ Note販売ページまたはメルマガ登録ページへ移動します
                </p>
            </div>
        </section>
    );
}
