'use client';

import { DragDropContext, Droppable, Draggable } from 'react-beautiful-dnd';
import { DropResult } from 'react-beautiful-dnd';

interface TimeSelectorProps {
  selectedTimes: string[];
  onTimesChange: (times: string[]) => void;
}

export default function TimeSelector({ selectedTimes, onTimesChange }: TimeSelectorProps) {
  const availableTimes = [
    "07:00", "08:00", "09:00", "10:00", "11:00", "12:00",
    "13:00", "14:00", "15:00", "16:00", "17:00", "18:00",
    "19:00", "20:00", "21:00", "22:00", "23:00"
  ];

  const handleTimeToggle = (time: string) => {
    if (selectedTimes.includes(time)) {
      onTimesChange(selectedTimes.filter(t => t !== time));
    } else {
      onTimesChange([...selectedTimes, time]);
    }
  };

  const handleDragEnd = (result: DropResult) => {
    if (!result.destination) return;

    const items = Array.from(selectedTimes);
    const [reorderedItem] = items.splice(result.source.index, 1);
    items.splice(result.destination.index, 0, reorderedItem);

    onTimesChange(items);
  };

  return (
    <div className="space-y-6">
      <div>
        <h2 className="text-xl font-semibold text-gray-900 mb-4">Select Times</h2>
        <div className="grid grid-cols-3 sm:grid-cols-4 md:grid-cols-6 gap-2">
          {availableTimes.map((time) => (
            <label
              key={time}
              className="flex items-center space-x-2 cursor-pointer"
            >
              <input
                type="checkbox"
                checked={selectedTimes.includes(time)}
                onChange={() => handleTimeToggle(time)}
                className="rounded text-blue-500"
              />
              <span>{time}</span>
            </label>
          ))}
        </div>
      </div>

      {selectedTimes.length > 0 && (
        <div>
          <h3 className="text-lg font-medium text-gray-900 mb-3">
            Priority Order
          </h3>
          <DragDropContext onDragEnd={handleDragEnd}>
            <Droppable droppableId="times">
              {(provided) => (
                <div
                  {...provided.droppableProps}
                  ref={provided.innerRef}
                  className="space-y-2"
                >
                  {selectedTimes.map((time, index) => (
                    <Draggable key={time} draggableId={time} index={index}>
                      {(provided) => (
                        <div
                          ref={provided.innerRef}
                          {...provided.draggableProps}
                          {...provided.dragHandleProps}
                          className="bg-gray-100 p-3 rounded-md flex items-center"
                        >
                          <span className="mr-2">☰</span>
                          {index + 1}. {time}
                        </div>
                      )}
                    </Draggable>
                  ))}
                  {provided.placeholder}
                </div>
              )}
            </Droppable>
          </DragDropContext>
        </div>
      )}
    </div>
  );
} 