'use client'

import { useState, useRef, useEffect } from 'react'
import { motion } from 'framer-motion'
import { Send, Sparkles, ArrowRight, Bot, User } from 'lucide-react'

interface Message {
  id: string
  role: 'assistant' | 'user'
  content: string
  timestamp: Date
}

interface ClarificationConversationProps {
  requirement: string
  sessionId: string
  onComplete: (conversationHistory: Message[]) => void
  onSkip: () => void
}

export default function ClarificationConversation({ 
  requirement,
  sessionId,
  onComplete,
  onSkip 
}: ClarificationConversationProps) {
  const [messages, setMessages] = useState<Message[]>([
    {
      id: '1',
      role: 'assistant',
      content: `I see you want to: "${requirement}"\n\nThat sounds interesting! Let me ask you a few questions to make sure I build exactly what you need. Feel free to tell me anything that comes to mind - the more context, the better!`,
      timestamp: new Date()
    },
    {
      id: '2', 
      role: 'assistant',
      content: "What's the main problem you're trying to solve with this automation? What takes up most of your time right now?",
      timestamp: new Date()
    }
  ])
  const [input, setInput] = useState('')
  const [isThinking, setIsThinking] = useState(false)
  const [questionCount, setQuestionCount] = useState(1)
  const messagesEndRef = useRef<HTMLDivElement>(null)

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" })
  }

  useEffect(() => {
    scrollToBottom()
  }, [messages])

  const handleSend = async () => {
    if (!input.trim() || isThinking) return

    const userMessage: Message = {
      id: Date.now().toString(),
      role: 'user',
      content: input,
      timestamp: new Date()
    }

    setMessages(prev => [...prev, userMessage])
    setInput('')
    setIsThinking(true)

    try {
      // Call the real AI backend
      const response = await fetch(`${process.env.NEXT_PUBLIC_API_URL || 'https://web-production-bd955.up.railway.app'}/api/clarify/chat`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          message: input,
          history: messages.map(m => ({ role: m.role, content: m.content })),
          requirement: requirement
        })
      })

      const data = await response.json()
      
      const aiResponse: Message = {
        id: Date.now().toString(),
        role: 'assistant',
        content: data.response,
        timestamp: new Date()
      }

      setMessages(prev => [...prev, aiResponse])
      setQuestionCount(prev => prev + 1)
      
      // Check if AI is ready to build
      if (data.ready_to_build) {
        setQuestionCount(10) // Trigger completion state
      }
    } catch (error) {
      // Fallback to simulated response if API fails
      const aiResponse = generateContextualResponse(userMessage.content, questionCount)
      setMessages(prev => [...prev, aiResponse])
      setQuestionCount(prev => prev + 1)
    } finally {
      setIsThinking(false)
    }
  }

  const generateContextualResponse = (userInput: string, qCount: number): Message => {
    // In production, this would call the actual clarification agent
    const responses = [
      "That makes sense. How many people would be using this system? And roughly how often?",
      "Got it! What tools or platforms are you currently using that this would need to integrate with?",
      "Perfect. What would success look like for you? How would you measure if this automation is working well?",
      "I think I have a good understanding now. Is there anything else specific you'd like this system to do or any concerns you have?"
    ]

    const content = qCount < 4 ? responses[qCount - 1] : 
      "Excellent! I have everything I need to build you an amazing system. Let me get started on designing your custom AI agents...";

    return {
      id: Date.now().toString(),
      role: 'assistant',
      content,
      timestamp: new Date()
    }
  }

  const handleComplete = () => {
    onComplete(messages)
  }

  const readyToComplete = questionCount >= 4 && !isThinking

  return (
    <div className="max-w-4xl mx-auto h-full flex flex-col">
      {/* Header */}
      <div className="text-center mb-4">
        <h2 className="text-2xl font-bold text-gray-900">Let's Chat About Your Project</h2>
        <button
          onClick={onSkip}
          className="text-sm text-gray-500 hover:text-gray-700 underline mt-1"
        >
          Skip chat and build with original description
        </button>
      </div>

      {/* Chat Container */}
      <div className="flex-1 bg-white rounded-lg shadow-lg flex flex-col" style={{ height: '600px' }}>
        {/* Messages */}
        <div className="flex-1 overflow-y-auto p-6 space-y-4">
          {messages.map((message) => (
            <motion.div
              key={message.id}
              initial={{ opacity: 0, y: 10 }}
              animate={{ opacity: 1, y: 0 }}
              className={`flex ${message.role === 'user' ? 'justify-end' : 'justify-start'}`}
            >
              <div className={`flex items-start max-w-[80%] ${
                message.role === 'user' ? 'flex-row-reverse' : ''
              }`}>
                <div className={`flex-shrink-0 w-8 h-8 rounded-full flex items-center justify-center ${
                  message.role === 'user' ? 'bg-indigo-600 ml-2' : 'bg-gray-300 mr-2'
                }`}>
                  {message.role === 'user' ? (
                    <User className="w-5 h-5 text-white" />
                  ) : (
                    <Bot className="w-5 h-5 text-gray-700" />
                  )}
                </div>
                <div className={`rounded-lg p-4 ${
                  message.role === 'user' 
                    ? 'bg-indigo-600 text-white' 
                    : 'bg-gray-100 text-gray-800'
                }`}>
                  <p className="whitespace-pre-wrap">{message.content}</p>
                  <p className={`text-xs mt-1 ${
                    message.role === 'user' ? 'text-indigo-200' : 'text-gray-500'
                  }`}>
                    {message.timestamp.toLocaleTimeString()}
                  </p>
                </div>
              </div>
            </motion.div>
          ))}
          
          {isThinking && (
            <motion.div
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
              className="flex justify-start"
            >
              <div className="flex items-center space-x-2 bg-gray-100 rounded-lg p-4">
                <div className="flex space-x-1">
                  <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce" style={{ animationDelay: '0ms' }}></div>
                  <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce" style={{ animationDelay: '150ms' }}></div>
                  <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce" style={{ animationDelay: '300ms' }}></div>
                </div>
              </div>
            </motion.div>
          )}
          
          <div ref={messagesEndRef} />
        </div>

        {/* Input Area */}
        <div className="border-t p-4">
          {!readyToComplete ? (
            <div className="flex space-x-2">
              <input
                type="text"
                value={input}
                onChange={(e) => setInput(e.target.value)}
                onKeyPress={(e) => e.key === 'Enter' && handleSend()}
                placeholder="Type your response..."
                className="flex-1 px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-indigo-500 focus:border-transparent"
                disabled={isThinking}
              />
              <button
                onClick={handleSend}
                disabled={!input.trim() || isThinking}
                className="px-6 py-2 bg-indigo-600 text-white rounded-lg hover:bg-indigo-700 disabled:opacity-50 disabled:cursor-not-allowed flex items-center"
              >
                <Send className="h-4 w-4" />
              </button>
            </div>
          ) : (
            <motion.button
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              onClick={handleComplete}
              className="w-full px-6 py-3 bg-green-600 text-white rounded-lg font-semibold flex items-center justify-center space-x-2 hover:bg-green-700"
            >
              <span>Build My AI System</span>
              <ArrowRight className="h-5 w-5" />
            </motion.button>
          )}
        </div>
      </div>

      {/* Dynamic Tips */}
      <div className="mt-4 text-center text-sm text-gray-500">
        <p>
          <Sparkles className="inline w-4 h-4 text-yellow-500" />
          {' '}This AI conversation helps us understand your unique needs and build a better system for you
        </p>
      </div>
    </div>
  )
}