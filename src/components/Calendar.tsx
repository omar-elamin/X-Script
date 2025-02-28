'use client';

import { Calendar as CalendarComponent } from 'react-calendar';
import 'react-calendar/dist/Calendar.css';

interface CalendarProps {
  selectedDate: Date;
  onDateChange: (date: Date) => void;
}

export default function Calendar({ selectedDate, onDateChange }: CalendarProps) {
  const maxDate = new Date();
  maxDate.setMonth(maxDate.getMonth() + 3);

  return (
    <div className="space-y-4">
      <h2 className="text-xl font-semibold text-gray-900">Select Date</h2>
      <CalendarComponent
        onChange={(value) => onDateChange(value as Date)}
        value={selectedDate}
        minDate={new Date()}
        maxDate={maxDate}
        className="mx-auto"
      />
    </div>
  );
} 