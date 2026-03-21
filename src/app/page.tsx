import HeroSection from "@/components/HeroSection";
import BeforeAfter from "@/components/BeforeAfter";
import EmpathySection from "@/components/EmpathySection";
import ArticleList from "@/components/ArticleList";
import CTASection from "@/components/CTASection";

export default function Home() {
  return (
    <>
      {/* ヒーローセクション */}
      <HeroSection />

      {/* Before/After証拠画像エリア */}
      <BeforeAfter />

      {/* 共感セクション */}
      <EmpathySection />

      {/* 記事リスト */}
      <ArticleList />

      {/* CTA（フッター直前） */}
      <CTASection />
    </>
  );
}
