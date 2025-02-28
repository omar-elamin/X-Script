interface RetryIntervalProps {
  value: number;
  onChange: (value: number) => void;
}

export default function RetryInterval({ value, onChange }: RetryIntervalProps) {
  return (
    <div className="space-y-2">
      <h2 className="text-xl font-semibold text-gray-900">Retry Settings</h2>
      <div className="flex items-center space-x-2">
        <label htmlFor="retry-interval">Retry Interval (seconds):</label>
        <input
          id="retry-interval"
          type="number"
          min="1"
          value={value}
          onChange={(e) => onChange(Math.max(1, parseInt(e.target.value) || 1))}
          className="w-20 px-2 py-1 border rounded-md"
        />
      </div>
    </div>
  );
} 