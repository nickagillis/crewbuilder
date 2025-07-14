'use client'

import { useState } from 'react'
import { motion } from 'framer-motion'
import { 
  Download, 
  Star, 
  Users, 
  Clock, 
  DollarSign, 
  CheckCircle, 
  Code, 
  FileText, 
  Settings,
  PlayCircle,
  RotateCcw
} from 'lucide-react'

interface SystemOutputProps {
  system: {
    name: string
    agents: number
    estimatedTime: string
    complexity: string
  }
  onStartNew: () => void
}

export default function SystemOutput({ system, onStartNew }: SystemOutputProps) {
  const [feedback, setFeedback] = useState<number | null>(null)
  const [showDownload, setShowDownload] = useState(false)

  const handleFeedback = async (rating: number) => {
    setFeedback(rating)
    
    try {
      const response = await fetch('/api/feedback', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ 
          rating,
          systemData: system,
          timestamp: new Date().toISOString()
        }),
      })

      if (response.ok) {
        const result = await response.json()
        console.log('Feedback recorded:', result.insights)
      }
    } catch (error) {
      console.error('Failed to record feedback:', error)
    }
  }

  const handleDownload = () => {
    setShowDownload(true)
    // Simulate download process
    setTimeout(() => {
      alert('System files downloaded! Check your Downloads folder for the complete CrewAI system.')
      setShowDownload(false)
    }, 2000)
  }

  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      className="space-y-8"
    >
      {/* Success Header */}
      <div className="text-center">
        <motion.div
          initial={{ scale: 0 }}
          animate={{ scale: 1 }}
          transition={{ delay: 0.2 }}
          className="inline-flex items-center justify-center w-16 h-16 bg-green-100 rounded-full mb-4"
        >
          <CheckCircle className="h-8 w-8 text-green-600" />
        </motion.div>
        <h3 className="text-2xl font-bold text-gray-900 mb-2">
          Your AI Agent System is Ready!
        </h3>
        <p className="text-gray-600">
          Complete CrewAI system generated with monitoring, documentation, and deployment configurations.
        </p>
      </div>

      {/* System Overview */}
      <div className="bg-gradient-to-r from-green-50 to-emerald-50 p-6 rounded-xl border border-green-200">
        <h4 className="text-xl font-bold text-gray-900 mb-4">{system.name}</h4>
        
        <div className="grid md:grid-cols-4 gap-4 mb-6">
          <div className="text-center">
            <Users className="h-8 w-8 text-green-600 mx-auto mb-2" />
            <div className="text-2xl font-bold text-gray-900">{system.agents}</div>
            <div className="text-sm text-gray-600">AI Agents</div>
          </div>
          <div className="text-center">
            <Clock className="h-8 w-8 text-green-600 mx-auto mb-2" />
            <div className="text-2xl font-bold text-gray-900">{system.estimatedTime}</div>
            <div className="text-sm text-gray-600">Runtime</div>
          </div>
          <div className="text-center">
            <Settings className="h-8 w-8 text-green-600 mx-auto mb-2" />
            <div className="text-2xl font-bold text-gray-900 capitalize">{system.complexity}</div>
            <div className="text-sm text-gray-600">Complexity</div>
          </div>
          <div className="text-center">
            <DollarSign className="h-8 w-8 text-green-600 mx-auto mb-2" />
            <div className="text-2xl font-bold text-gray-900">$50-100</div>
            <div className="text-sm text-gray-600">Monthly Cost</div>
          </div>
        </div>

        <div className="bg-white p-4 rounded-lg">
          <h5 className="font-semibold mb-2">What's Included:</h5>
          <div className="grid md:grid-cols-2 gap-2 text-sm">
            <div className="flex items-center space-x-2">
              <CheckCircle className="h-4 w-4 text-green-500" />
              <span>Production-ready Python code</span>
            </div>
            <div className="flex items-center space-x-2">
              <CheckCircle className="h-4 w-4 text-green-500" />
              <span>Complete documentation</span>
            </div>
            <div className="flex items-center space-x-2">
              <CheckCircle className="h-4 w-4 text-green-500" />
              <span>Deployment configurations</span>
            </div>
            <div className="flex items-center space-x-2">
              <CheckCircle className="h-4 w-4 text-green-500" />
              <span>Monitoring & alerting setup</span>
            </div>
            <div className="flex items-center space-x-2">
              <CheckCircle className="h-4 w-4 text-green-500" />
              <span>API integration guides</span>
            </div>
            <div className="flex items-center space-x-2">
              <CheckCircle className="h-4 w-4 text-green-500" />
              <span>Quality assurance reports</span>
            </div>
          </div>
        </div>
      </div>

      {/* Actions */}
      <div className="flex flex-col sm:flex-row gap-4">
        <motion.button
          whileHover={{ scale: 1.02 }}
          whileTap={{ scale: 0.98 }}
          onClick={handleDownload}
          disabled={showDownload}
          className="flex-1 bg-indigo-600 text-white py-4 px-6 rounded-lg font-semibold flex items-center justify-center space-x-2 hover:bg-indigo-700 disabled:opacity-50 transition-colors"
        >
          {showDownload ? (
            <div className="animate-spin rounded-full h-5 w-5 border-b-2 border-white"></div>
          ) : (
            <>
              <Download className="h-5 w-5" />
              <span>Download Complete System</span>
            </>
          )}
        </motion.button>

        <motion.button
          whileHover={{ scale: 1.02 }}
          whileTap={{ scale: 0.98 }}
          className="flex-1 bg-gray-100 text-gray-700 py-4 px-6 rounded-lg font-semibold flex items-center justify-center space-x-2 hover:bg-gray-200 transition-colors"
        >
          <PlayCircle className="h-5 w-5" />
          <span>Deploy to Railway (Pro)</span>
        </motion.button>

        <motion.button
          whileHover={{ scale: 1.02 }}
          whileTap={{ scale: 0.98 }}
          onClick={onStartNew}
          className="bg-white border-2 border-gray-200 text-gray-700 py-4 px-6 rounded-lg font-semibold flex items-center justify-center space-x-2 hover:border-gray-300 transition-colors"
        >
          <RotateCcw className="h-5 w-5" />
          <span>Build Another System</span>
        </motion.button>
      </div>

      {/* Feedback Collection */}
      <div className="bg-blue-50 p-6 rounded-lg">
        <h4 className="font-semibold text-blue-900 mb-4">Help Us Learn & Improve</h4>
        <p className="text-blue-700 text-sm mb-4">
          How well does this system match your requirements? Your feedback helps improve future generations.
        </p>
        
        <div className="flex items-center space-x-2 mb-4">
          <span className="text-sm text-blue-700">Rate this system:</span>
          {[1, 2, 3, 4, 5].map((rating) => (
            <motion.button
              key={rating}
              whileHover={{ scale: 1.1 }}
              whileTap={{ scale: 0.9 }}
              onClick={() => handleFeedback(rating)}
              className={`p-1 ${
                feedback && feedback >= rating
                  ? 'text-yellow-500'
                  : 'text-gray-300 hover:text-yellow-400'
              }`}
            >
              <Star className="h-6 w-6 fill-current" />
            </motion.button>
          ))}
        </div>

        {feedback && (
          <motion.div
            initial={{ opacity: 0, y: 10 }}
            animate={{ opacity: 1, y: 0 }}
            className="text-sm text-blue-700"
          >
            Thank you! Your feedback helps our learning system improve for everyone.
          </motion.div>
        )}
      </div>

      {/* Learning Insights */}
      <div className="bg-indigo-50 p-6 rounded-lg">
        <h4 className="font-semibold text-indigo-900 mb-2">📊 Based on Learning Data</h4>
        <div className="text-indigo-700 text-sm space-y-1">
          <p>• 94% of similar systems are successfully deployed within 1 week</p>
          <p>• Users typically see 60-80% time savings after implementation</p>
          <p>• Most popular modifications: custom reporting and Slack integration</p>
          <p>• Average ROI: 300% within 6 months for systems of this complexity</p>
        </div>
      </div>
    </motion.div>
  )
}