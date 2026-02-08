import type { TimeRange } from "../types";

const TIME_RANGES: { value: TimeRange; label: string }[] = [
  { value: "1h", label: "1 Hour" },
  { value: "6h", label: "6 Hours" },
  { value: "24h", label: "24 Hours" },
  { value: "7d", label: "7 Days" },
];

interface TimeRangeSelectorProps {
  selected: TimeRange;
  onChange: (range: TimeRange) => void;
}

function TimeRangeSelector({ selected, onChange }: TimeRangeSelectorProps) {
  return (
    <div className="time-range-selector" role="group" aria-label="Time range">
      {TIME_RANGES.map((range) => (
        <button
          key={range.value}
          className={`time-range-btn ${selected === range.value ? "active" : ""}`}
          onClick={() => onChange(range.value)}
          aria-pressed={selected === range.value}
        >
          {range.label}
        </button>
      ))}
    </div>
  );
}

export default TimeRangeSelector;
