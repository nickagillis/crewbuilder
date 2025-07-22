import { NextRequest, NextResponse } from 'next/server'

export async function POST(request: NextRequest) {
  try {
    const body = await request.json()
    
    // Connect to real CrewBuilder FastAPI backend
    const backendUrl = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'
    
    console.log(`Deploying via CrewBuilder backend: ${backendUrl}/api/deploy`)
    
    const response = await fetch(`${backendUrl}/api/deploy`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(body),
      signal: AbortSignal.timeout(600000) // 10 minutes timeout for deployment
    })

    if (!response.ok) {
      const errorData = await response.json().catch(() => ({ error: 'Unknown error' }))
      throw new Error(`Deployment error: ${response.status} - ${errorData.detail || errorData.error || 'Unknown error'}`)
    }

    const result = await response.json()
    return NextResponse.json(result)

  } catch (error) {
    console.error('Deployment error:', error)
    
    if (error instanceof Error) {
      if (error.name === 'AbortError') {
        return NextResponse.json(
          { 
            error: 'Deployment timed out. This can happen with complex systems.',
            details: 'Please try again or check Railway dashboard.'
          },
          { status: 408 }
        )
      }
    }
    
    return NextResponse.json(
      { 
        error: 'Failed to deploy system',
        details: error instanceof Error ? error.message : 'Unknown error'
      },
      { status: 500 }
    )
  }
}