interface SummaryCardProps {
  title: string;
  value: string;
  subtitle: string;
}

function SummaryCard({ title, value, subtitle }: SummaryCardProps) {
  return (
    <div className="summary-card">
      <div className="summary-card-title">{title}</div>
      <div className="summary-card-value">{value}</div>
      <div className="summary-card-subtitle">{subtitle}</div>
    </div>
  );
}

export default SummaryCard;
