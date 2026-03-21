export default function BeforeAfter() {
    return (
        <section className="bg-gray-100 py-12 md:py-16">
            <div className="mx-auto max-w-4xl px-4">
                <h2 className="mb-8 text-center text-xl font-bold text-gray-900 md:text-2xl">
                    証拠写真
                </h2>

                <div className="grid gap-6 md:grid-cols-2 md:gap-8">
                    {/* Before */}
                    <div className="overflow-hidden rounded-lg bg-white shadow-lg">
                        <div className="flex aspect-[4/5] items-center justify-center bg-gray-300">
                            <div className="p-8 text-center">
                                <p className="mb-2 text-lg font-bold text-gray-600">
                                    Before写真
                                </p>
                                <p className="text-sm text-gray-500">
                                    ここに100kg・腹囲91cm時代の
                                    <br />
                                    写真を配置してください
                                </p>
                            </div>
                        </div>
                        <div className="bg-primary-800 p-4 text-center">
                            <p className="text-lg font-bold text-white">Before</p>
                            <p className="text-2xl font-black text-accent-500">
                                100kg・腹囲91cm
                            </p>
                        </div>
                    </div>

                    {/* After */}
                    <div className="overflow-hidden rounded-lg bg-white shadow-lg">
                        <div className="flex aspect-[4/5] items-center justify-center bg-gray-300">
                            <div className="p-8 text-center">
                                <p className="mb-2 text-lg font-bold text-gray-600">
                                    After写真
                                </p>
                                <p className="text-sm text-gray-500">
                                    ここに68kg・シックスパック時代の
                                    <br />
                                    写真を配置してください
                                </p>
                            </div>
                        </div>
                        <div className="bg-primary-800 p-4 text-center">
                            <p className="text-lg font-bold text-white">After</p>
                            <p className="text-2xl font-black text-accent-500">
                                68kg・シックスパック
                            </p>
                        </div>
                    </div>
                </div>

                {/* 変化の数値 */}
                <div className="mt-8 grid grid-cols-3 gap-4 rounded-lg bg-white p-6 shadow-md">
                    <div className="text-center">
                        <p className="text-sm text-gray-600">体重</p>
                        <p className="text-2xl font-black text-primary-700 md:text-3xl">
                            -32kg
                        </p>
                    </div>
                    <div className="text-center">
                        <p className="text-sm text-gray-600">腹囲</p>
                        <p className="text-2xl font-black text-primary-700 md:text-3xl">
                            -20cm以上
                        </p>
                    </div>
                    <div className="text-center">
                        <p className="text-sm text-gray-600">期間</p>
                        <p className="text-2xl font-black text-primary-700 md:text-3xl">
                            約1年
                        </p>
                    </div>
                </div>
            </div>
        </section>
    );
}
