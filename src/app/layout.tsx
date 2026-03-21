import type { Metadata } from "next";
import { Noto_Sans_JP } from "next/font/google";
import "./globals.css";
import Header from "@/components/Header";
import Footer from "@/components/Footer";

const notoSansJP = Noto_Sans_JP({
  variable: "--font-noto-sans-jp",
  subsets: ["latin"],
  weight: ["400", "500", "700", "900"],
  display: "swap",
});

export const metadata: Metadata = {
  title: "健康診断E判定からの逆襲 | 30代・40代メタボ男性のためのダイエットブログ",
  description:
    "健康診断E判定、腹囲91cmの屈辱から100kgの男が『仕組み化』だけでシックスパックを手に入れた全記録。30代・40代のメタボ男性に向けた、実直で信頼できるダイエット情報を発信。",
  keywords: ["ダイエット", "メタボ", "健康診断", "40代", "30代", "シックスパック", "痩せる"],
  openGraph: {
    title: "健康診断E判定からの逆襲",
    description: "100kgの男が『仕組み化』だけでシックスパックを手に入れた全記録",
    type: "website",
    locale: "ja_JP",
  },
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="ja">
      <body className={`${notoSansJP.variable} antialiased`}>
        <Header />
        <main>{children}</main>
        <Footer />
      </body>
    </html>
  );
}
