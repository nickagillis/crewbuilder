import { NextRequest, NextResponse } from 'next/server'

// Real CrewBuilder backend connection
export async function POST(request: NextRequest) {
  try {
    const body = await request.json()
    const { requirement } = body

    if (!requirement || typeof requirement !== 'string') {
      return NextResponse.json(
        { error: 'Valid requirement string is required' },
        { status: 400 }
      )
    }

    // Log the generation attempt for learning
    console.log('Generation request:', {
      requirement,
      timestamp: new Date().toISOString(),
      userAgent: request.headers.get('user-agent'),
    })

    // Connect to real CrewBuilder FastAPI backend
    const backendUrl = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'
    
    console.log(`Connecting to CrewBuilder backend: ${backendUrl}/api/generate`)
    
    const response = await fetch(`${backendUrl}/api/generate`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ requirement }),
      // Increase timeout for the complete 10-agent pipeline
      signal: AbortSignal.timeout(300000) // 5 minutes timeout
    })

    if (!response.ok) {
      const errorData = await response.json().catch(() => ({ error: 'Unknown error' }))
      throw new Error(`Backend error: ${response.status} - ${errorData.error || 'Unknown error'}`)
    }

    const result = await response.json()

    // Log successful generation for learning
    console.log('Generation successful:', {
      requirement: requirement.substring(0, 100) + '...',
      success: result.success,
      stages_completed: result.data?.pipeline_stages?.length || 0,
      timestamp: new Date().toISOString(),
    })

    return NextResponse.json(result)

  } catch (error) {
    console.error('Generation error:', error)
    
    // Check if it's a timeout or connection error
    if (error instanceof Error) {
      if (error.name === 'AbortError') {
        return NextResponse.json(
          { 
            error: 'Generation timed out - the 10-agent pipeline is taking longer than expected. Please try again.',
            details: 'This usually happens when the AI agents are thinking deeply about complex requirements.'
          },
          { status: 408 }
        )
      }
      
      if (error.message.includes('fetch')) {
        return NextResponse.json(
          { 
            error: 'Cannot connect to CrewBuilder backend. Please ensure the API server is running on port 8000.',
            details: 'Run: python api_server.py'
          },
          { status: 503 }
        )
      }
    }
    
    return NextResponse.json(
      { 
        error: 'Failed to generate system',
        details: error instanceof Error ? error.message : 'Unknown error'
      },
      { status: 500 }
    )
  }
}

// Real backend integration - no simulation functions needed