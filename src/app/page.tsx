'use client';

import Calendar from '@/components/Calendar';
import TimeSelector from '@/components/TimeSelector';
import RetryInterval from '@/components/RetryInterval';
import StatusBar from '@/components/StatusBar';
import { useState, useRef } from 'react';

export default function Home() {
  const [selectedDate, setSelectedDate] = useState<Date>(new Date());
  const [selectedTimes, setSelectedTimes] = useState<string[]>([]);
  const [retryInterval, setRetryInterval] = useState<number>(300);
  const [status, setStatus] = useState<string>('');
  const [isBooking, setIsBooking] = useState<boolean>(false);
  const retryTimeoutRef = useRef<NodeJS.Timeout | null>(null);

  const attemptBooking = async () => {
    try {
      const response = await fetch('/api/book', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          date: selectedDate,
          times: selectedTimes,
          interval: retryInterval,
        }),
      });

      if (response.ok) {
        setStatus('Booking completed!');
        setIsBooking(false);
        return true;
      }
      console.log(response);
      return false;
    } catch (error) {
      setStatus(`Error: ${error}`);
      setIsBooking(false);
      console.log(error);
      return false;
    }
  };

  const handleStartBooking = async () => {
    if (selectedTimes.length === 0) {
      setStatus('Please select at least one time slot');
      return;
    }

    setIsBooking(true);
    setStatus('Starting booking process...');

    if (!(await attemptBooking())) {
      setStatus(`No available slots, retrying in ${retryInterval} seconds...`);
      retryTimeoutRef.current = setTimeout(handleStartBooking, retryInterval * 1000);
    }
  };

  const handleStopBooking = () => {
    if (retryTimeoutRef.current) {
      clearTimeout(retryTimeoutRef.current);
    }
    setStatus('Booking stopped');
    setIsBooking(false);
  };

  return (
    <div className="min-h-screen bg-gray-50">
      <div className="max-w-4xl mx-auto py-8 px-4 sm:px-6 lg:px-8">
        <h1 className="text-3xl font-bold text-gray-900 mb-8">
          Fitness Slot Booking
        </h1>
        
        <div className="space-y-8">
          <div className="bg-white p-6 rounded-lg shadow">
            <Calendar 
              selectedDate={selectedDate} 
              onDateChange={setSelectedDate} 
            />
          </div>

          <div className="bg-white p-6 rounded-lg shadow">
            <RetryInterval 
              value={retryInterval} 
              onChange={setRetryInterval} 
            />
          </div>

          <div className="bg-white p-6 rounded-lg shadow">
            <TimeSelector 
              selectedTimes={selectedTimes}
              onTimesChange={setSelectedTimes}
            />
          </div>

          <div className="flex gap-4">
            <button
              onClick={handleStartBooking}
              disabled={isBooking}
              className="bg-blue-500 text-white px-6 py-2 rounded-md hover:bg-blue-600 
                         disabled:bg-gray-400 disabled:cursor-not-allowed"
            >
              Book Selected Slots
            </button>
            <button
              onClick={handleStopBooking}
              disabled={!isBooking}
              className="bg-red-500 text-white px-6 py-2 rounded-md hover:bg-red-600
                         disabled:bg-gray-400 disabled:cursor-not-allowed"
            >
              Stop Retrying
            </button>
          </div>

          <StatusBar status={status} />
        </div>
      </div>
    </div>
  );
}
