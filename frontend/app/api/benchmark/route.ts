import { NextRequest, NextResponse } from 'next/server';

const BACKEND_URL = process.env.BACKEND_URL || 'http://localhost:8000';

export async function GET(request: NextRequest) {
  try {
    const { searchParams } = new URL(request.url);
    const num_queries = searchParams.get('num_queries') || '20';

    const response = await fetch(
      `${BACKEND_URL}/api/benchmark/run?num_queries=${num_queries}`,
      {
        headers: {
          'ngrok-skip-browser-warning': 'true',
          'Bypass-Tunnel-Reminder': 'true',
        },
      }
    );

    const data = await response.json();
    return NextResponse.json(data);
  } catch (err) {
    console.error('Proxy /api/benchmark error:', err);
    return NextResponse.json({ error: 'Backend unreachable' }, { status: 502 });
  }
}
