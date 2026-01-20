interface PointBoxProps {
    children: React.ReactNode;
    label?: string;
}

export default function PointBox({
    children,
    label = "ここがポイント",
}: PointBoxProps) {
    return (
        <div className="point-box">
            <span className="point-box-label">{label}</span>
            <div className="point-box-content">{children}</div>
        </div>
    );
}
