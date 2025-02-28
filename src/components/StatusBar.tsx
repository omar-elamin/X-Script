interface StatusBarProps {
  status: string;
}

export default function StatusBar({ status }: StatusBarProps) {
  if (!status) return null;

  return (
    <div className="bg-gray-100 p-4 rounded-md">
      <p className="text-gray-700">{status}</p>
    </div>
  );
} 