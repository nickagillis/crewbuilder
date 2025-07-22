'use client'

import { useState, useEffect } from 'react'
import { motion } from 'framer-motion'
import { MessageCircle, Send, Sparkles, ArrowRight } from 'lucide-react'

interface Question {
  question: string
  context: string
  options: string[]
  type: 'open' | 'multiple_choice' | 'yes_no'
}

interface ClarificationChatProps {
  questions: Question[]
  sessionId: string
  requirement: string
  onComplete: (responses: Record<string, string>) => void
  onSkip: () => void
}

export default function ClarificationChat({ 
  questions, 
  sessionId,
  requirement,
  onComplete,
  onSkip 
}: ClarificationChatProps) {
  const [responses, setResponses] = useState<Record<string, string>>({})
  const [currentInput, setCurrentInput] = useState('')
  const [answeredQuestions, setAnsweredQuestions] = useState<number[]>([])
  const [currentQuestionIndex, setCurrentQuestionIndex] = useState(0)

  const allQuestionsAnswered = answeredQuestions.length === questions.length

  const handleAnswer = (questionIndex: number, answer: string) => {
    setResponses({
      ...responses,
      [`question_${questionIndex}`]: answer
    })
    if (!answeredQuestions.includes(questionIndex)) {
      setAnsweredQuestions([...answeredQuestions, questionIndex])
    }
    
    // Move to next unanswered question
    const nextUnanswered = questions.findIndex((_, idx) => 
      idx > questionIndex && !answeredQuestions.includes(idx)
    )
    if (nextUnanswered !== -1) {
      setCurrentQuestionIndex(nextUnanswered)
    }
    setCurrentInput('')
  }

  const handleSubmitCurrent = () => {
    if (currentInput.trim()) {
      handleAnswer(currentQuestionIndex, currentInput)
    }
  }

  const handleComplete = () => {
    if (allQuestionsAnswered) {
      onComplete(responses)
    }
  }

  return (
    <div className="max-w-4xl mx-auto">
      {/* Header */}
      <div className="text-center mb-6">
        <div className="flex items-center justify-center mb-4">
          <MessageCircle className="h-8 w-8 text-indigo-600 mr-2" />
          <h2 className="text-3xl font-bold text-gray-900">Let's Chat About Your Needs</h2>
        </div>
        <p className="text-gray-600 mb-2">
          I have a few questions to better understand your requirements
        </p>
        <button
          onClick={onSkip}
          className="text-sm text-gray-500 hover:text-gray-700 underline"
        >
          Skip this and use my original description
        </button>
      </div>

      {/* Chat Container */}
      <div className="bg-white rounded-lg shadow-lg p-6" style={{ maxHeight: '600px', overflowY: 'auto' }}>
        {/* User's Original Requirement */}
        <div className="mb-6 p-4 bg-gray-50 rounded-lg">
          <p className="text-sm text-gray-600 mb-1">You said:</p>
          <p className="text-gray-900">{requirement}</p>
        </div>

        {/* AI Introduction */}
        <motion.div
          initial={{ opacity: 0, y: 10 }}
          animate={{ opacity: 1, y: 0 }}
          className="flex items-start mb-6"
        >
          <Sparkles className="h-6 w-6 text-indigo-600 mt-1 mr-3 flex-shrink-0" />
          <div>
            <p className="text-gray-800">
              Great! I'd like to understand your needs better so I can build the perfect system for you. 
              Feel free to answer these questions in any order:
            </p>
          </div>
        </motion.div>

        {/* Questions List */}
        <div className="space-y-4">
          {questions.map((q, idx) => {
            const isAnswered = answeredQuestions.includes(idx)
            const answer = responses[`question_${idx}`]
            
            return (
              <motion.div
                key={idx}
                initial={{ opacity: 0, x: -20 }}
                animate={{ opacity: 1, x: 0 }}
                transition={{ delay: idx * 0.1 }}
                className={`p-4 rounded-lg border-2 ${
                  isAnswered 
                    ? 'border-green-200 bg-green-50' 
                    : idx === currentQuestionIndex
                    ? 'border-indigo-300 bg-indigo-50'
                    : 'border-gray-200'
                }`}
              >
                <div className="flex items-start">
                  <span className={`text-lg font-semibold mr-3 ${
                    isAnswered ? 'text-green-600' : 'text-gray-600'
                  }`}>
                    {idx + 1}.
                  </span>
                  <div className="flex-1">
                    <p className="font-medium text-gray-900 mb-1">{q.question}</p>
                    {q.context && (
                      <p className="text-sm text-gray-600 mb-3 italic">{q.context}</p>
                    )}
                    
                    {isAnswered ? (
                      <div className="mt-2 p-3 bg-white rounded border border-gray-200">
                        <p className="text-sm text-gray-700">{answer}</p>
                        <button
                          onClick={() => {
                            setCurrentQuestionIndex(idx)
                            setCurrentInput(answer)
                          }}
                          className="text-xs text-indigo-600 hover:underline mt-1"
                        >
                          Edit answer
                        </button>
                      </div>
                    ) : (
                      <div className="mt-3">
                        {idx === currentQuestionIndex && (
                          <div className="flex gap-2">
                            <input
                              type="text"
                              value={currentInput}
                              onChange={(e) => setCurrentInput(e.target.value)}
                              onKeyPress={(e) => e.key === 'Enter' && handleSubmitCurrent()}
                              className="flex-1 px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-indigo-500 focus:border-transparent"
                              placeholder="Type your answer..."
                              autoFocus
                            />
                            <button
                              onClick={handleSubmitCurrent}
                              disabled={!currentInput.trim()}
                              className="px-4 py-2 bg-indigo-600 text-white rounded-lg hover:bg-indigo-700 disabled:opacity-50 disabled:cursor-not-allowed"
                            >
                              <Send className="h-4 w-4" />
                            </button>
                          </div>
                        )}
                      </div>
                    )}
                  </div>
                </div>
              </motion.div>
            )
          })}
        </div>

        {/* Progress */}
        <div className="mt-6 text-center">
          <p className="text-sm text-gray-600 mb-2">
            {answeredQuestions.length} of {questions.length} questions answered
          </p>
          <div className="w-full bg-gray-200 rounded-full h-2">
            <motion.div
              className="bg-indigo-600 h-2 rounded-full"
              initial={{ width: 0 }}
              animate={{ width: `${(answeredQuestions.length / questions.length) * 100}%` }}
            />
          </div>
        </div>

        {/* Complete Button */}
        {allQuestionsAnswered && (
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            className="mt-6 text-center"
          >
            <button
              onClick={handleComplete}
              className="px-8 py-3 bg-green-600 text-white rounded-lg font-semibold flex items-center justify-center space-x-2 hover:bg-green-700 mx-auto"
            >
              <span>Generate My System</span>
              <ArrowRight className="h-5 w-5" />
            </button>
          </motion.div>
        )}
      </div>

      {/* Tips */}
      <div className="mt-4 text-center text-sm text-gray-500">
        <p>💡 <strong>Tip:</strong> The more details you provide, the better your custom AI system will be!</p>
      </div>
    </div>
  )
}