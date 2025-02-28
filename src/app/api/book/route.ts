import { NextResponse } from 'next/server';
import { exec } from 'child_process';
import { promisify } from 'util';

const execPromise = promisify(exec);

export async function POST(request: Request) {
  try {
    const { date, times, interval } = await request.json();

    // Format date for Python script
    const formattedDate = new Date(date).toISOString().split('T')[0];

    // Convert times array to comma-separated string
    const timesList = times.join(',');

    console.log(`Executing: python main.py --date "${formattedDate}" --times "${timesList}" --interval ${interval}`);

    let stdout = '';
    let stderr = '';
    try {
      // Execute Python script with parameters
      ({ stdout, stderr } = await execPromise(
        `python main.py --date "${formattedDate}" --times "${timesList}" --interval ${interval}`
      ))
    }
    catch (error) {
      console.error('Error executing booking script:', error);
      return NextResponse.json(
        { error: 'Internal server error', details: String(error) },
        { status: 500 }
      );
    }

    if (stderr) {
      console.error('Python script error:', stderr);
      return NextResponse.json(
        { error: 'Failed to execute booking script', details: stderr },
        { status: 500 }
      );
    }

    console.log('Python script output:', stdout);

    // Check if booking was successful
    if (stdout.includes('Successfully booked')) {
      return NextResponse.json({ success: true, message: 'Booking successful' });
    } else {
      return NextResponse.json(
        { success: false, message: 'No available slots', details: stdout },
        { status: 409 }
      );
    }
  } catch (error) {
    console.error('API error:', error);
    return NextResponse.json(
      { error: 'Internal server error', details: String(error) },
      { status: 500 }
    );
  }
} 