interface StatusBadgeProps {
  usage: number;
}

function getStatusLevel(usage: number): { label: string; className: string } {
  if (usage >= 90) {
    return { label: "Critical", className: "status-badge--red" };
  }
  if (usage >= 70) {
    return { label: "Warning", className: "status-badge--yellow" };
  }
  return { label: "Healthy", className: "status-badge--green" };
}

function StatusBadge({ usage }: StatusBadgeProps) {
  const { label, className } = getStatusLevel(usage);

  return <span className={`status-badge ${className}`}>{label}</span>;
}

export default StatusBadge;
