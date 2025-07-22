'use client'

import { useState } from 'react'
import { motion } from 'framer-motion'
import { MessageCircle, CheckCircle, ArrowRight, Sparkles } from 'lucide-react'

interface Question {
  question: string
  context: string
  options: string[]
  type: 'open' | 'multiple_choice' | 'yes_no'
}

interface ClarificationFlowProps {
  questions: Question[]
  sessionId: string
  onComplete: (responses: Record<string, string>) => void
  onSkip: () => void
}

export default function ClarificationFlow({ 
  questions, 
  sessionId, 
  onComplete,
  onSkip 
}: ClarificationFlowProps) {
  const [currentQuestionIndex, setCurrentQuestionIndex] = useState(0)
  const [responses, setResponses] = useState<Record<string, string>>({})
  const [currentAnswer, setCurrentAnswer] = useState('')

  const currentQuestion = questions[currentQuestionIndex]
  const progress = ((currentQuestionIndex + 1) / questions.length) * 100

  const handleNext = () => {
    if (currentAnswer.trim()) {
      const newResponses = {
        ...responses,
        [`question_${currentQuestionIndex}`]: currentAnswer
      }
      setResponses(newResponses)
      
      if (currentQuestionIndex < questions.length - 1) {
        setCurrentQuestionIndex(currentQuestionIndex + 1)
        setCurrentAnswer('')
      } else {
        onComplete(newResponses)
      }
    }
  }

  const handlePrevious = () => {
    if (currentQuestionIndex > 0) {
      setCurrentQuestionIndex(currentQuestionIndex - 1)
      setCurrentAnswer(responses[`question_${currentQuestionIndex - 1}`] || '')
    }
  }

  return (
    <div className="max-w-3xl mx-auto">
      {/* Header */}
      <div className="text-center mb-8">
        <div className="flex items-center justify-center mb-4">
          <Sparkles className="h-8 w-8 text-indigo-600 mr-2" />
          <h2 className="text-3xl font-bold text-gray-900">Let's Refine Your Requirements</h2>
        </div>
        <p className="text-gray-600">
          Our AI needs a bit more information to build the perfect system for you
        </p>
      </div>

      {/* Progress Bar */}
      <div className="mb-8">
        <div className="flex justify-between items-center mb-2">
          <span className="text-sm text-gray-600">Question {currentQuestionIndex + 1} of {questions.length}</span>
          <button
            onClick={onSkip}
            className="text-sm text-gray-500 hover:text-gray-700 underline"
          >
            Skip clarification
          </button>
        </div>
        <div className="w-full bg-gray-200 rounded-full h-2">
          <motion.div
            className="bg-indigo-600 h-2 rounded-full"
            initial={{ width: 0 }}
            animate={{ width: `${progress}%` }}
            transition={{ duration: 0.3 }}
          />
        </div>
      </div>

      {/* Question Card */}
      <motion.div
        key={currentQuestionIndex}
        initial={{ opacity: 0, x: 20 }}
        animate={{ opacity: 1, x: 0 }}
        exit={{ opacity: 0, x: -20 }}
        className="bg-white rounded-lg shadow-lg p-8 mb-6"
      >
        <div className="flex items-start mb-6">
          <MessageCircle className="h-6 w-6 text-indigo-600 mt-1 mr-3 flex-shrink-0" />
          <div className="flex-1">
            <h3 className="text-xl font-semibold text-gray-900 mb-2">
              {currentQuestion.question}
            </h3>
            <p className="text-gray-600 text-sm">
              {currentQuestion.context}
            </p>
          </div>
        </div>

        {/* Answer Input */}
        <div className="space-y-4">
          {currentQuestion.type === 'open' && (
            <textarea
              value={currentAnswer}
              onChange={(e) => setCurrentAnswer(e.target.value)}
              className="w-full h-32 px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-indigo-500 focus:border-transparent resize-none"
              placeholder="Type your answer here..."
              autoFocus
            />
          )}
          
          {currentQuestion.type === 'multiple_choice' && currentQuestion.options.length > 0 && (
            <div className="space-y-2">
              {currentQuestion.options.map((option, idx) => (
                <label
                  key={idx}
                  className="flex items-center p-4 border rounded-lg cursor-pointer hover:bg-gray-50"
                >
                  <input
                    type="radio"
                    value={option}
                    checked={currentAnswer === option}
                    onChange={(e) => setCurrentAnswer(e.target.value)}
                    className="mr-3"
                  />
                  <span>{option}</span>
                </label>
              ))}
            </div>
          )}
          
          {currentQuestion.type === 'yes_no' && (
            <div className="flex gap-4">
              <button
                onClick={() => setCurrentAnswer('Yes')}
                className={`flex-1 p-4 rounded-lg border-2 ${
                  currentAnswer === 'Yes' 
                    ? 'border-indigo-600 bg-indigo-50' 
                    : 'border-gray-300 hover:border-gray-400'
                }`}
              >
                Yes
              </button>
              <button
                onClick={() => setCurrentAnswer('No')}
                className={`flex-1 p-4 rounded-lg border-2 ${
                  currentAnswer === 'No' 
                    ? 'border-indigo-600 bg-indigo-50' 
                    : 'border-gray-300 hover:border-gray-400'
                }`}
              >
                No
              </button>
            </div>
          )}
        </div>
      </motion.div>

      {/* Navigation */}
      <div className="flex justify-between">
        <button
          onClick={handlePrevious}
          disabled={currentQuestionIndex === 0}
          className="px-6 py-3 text-gray-600 hover:text-gray-900 disabled:opacity-50 disabled:cursor-not-allowed"
        >
          Previous
        </button>
        
        <motion.button
          onClick={handleNext}
          disabled={!currentAnswer.trim()}
          whileHover={{ scale: 1.02 }}
          whileTap={{ scale: 0.98 }}
          className="px-8 py-3 bg-indigo-600 text-white rounded-lg font-semibold flex items-center space-x-2 hover:bg-indigo-700 disabled:opacity-50 disabled:cursor-not-allowed"
        >
          <span>{currentQuestionIndex === questions.length - 1 ? 'Complete' : 'Next'}</span>
          {currentQuestionIndex === questions.length - 1 ? (
            <CheckCircle className="h-5 w-5" />
          ) : (
            <ArrowRight className="h-5 w-5" />
          )}
        </motion.button>
      </div>

      {/* Marketing Opportunity! */}
      <div className="mt-8 text-center text-sm text-gray-500">
        <p>💡 <strong>Did you know?</strong> Systems with clarified requirements have 73% higher success rates!</p>
      </div>
    </div>
  )
}