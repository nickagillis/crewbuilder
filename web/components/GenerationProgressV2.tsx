'use client'

import { useState, useEffect } from 'react'
import { motion } from 'framer-motion'
import { CheckCircle, Loader, AlertCircle, Search, Code, Shield, FileText, Rocket, MessageSquare } from 'lucide-react'

interface GenerationProgressProps {
  requirement: string
}

interface Step {
  name: string
  icon: React.ReactNode
  description: string
  estimatedTime: string
}

export default function GenerationProgressV2({ requirement }: GenerationProgressProps) {
  const [currentStep, setCurrentStep] = useState(0)
  const [completedSteps, setCompletedSteps] = useState<number[]>([])
  const [error, setError] = useState<string | null>(null)

  // New simplified stages following CrewBuilder V2
  const steps: Step[] = [
    { 
      name: "Clarification & API Verification", 
      icon: <MessageSquare className="h-5 w-5" />,
      description: "Understanding requirements and verifying API availability",
      estimatedTime: "20s"
    },
    { 
      name: "Architecture Design", 
      icon: <Search className="h-5 w-5" />,
      description: "Designing CrewAI architecture with proper patterns",
      estimatedTime: "15s"
    },
    { 
      name: "Task Flow Design", 
      icon: <Code className="h-5 w-5" />,
      description: "Creating detailed task definitions and dependencies",
      estimatedTime: "15s"
    },
    { 
      name: "Code Generation", 
      icon: <Code className="h-5 w-5" />,
      description: "Generating production-ready CrewAI code",
      estimatedTime: "20s"
    },
    { 
      name: "Quality Review", 
      icon: <Shield className="h-5 w-5" />,
      description: "Validating code quality and best practices",
      estimatedTime: "10s"
    },
    { 
      name: "Documentation & Deployment", 
      icon: <FileText className="h-5 w-5" />,
      description: "Creating docs and deployment configuration",
      estimatedTime: "15s"
    }
  ]

  useEffect(() => {
    const timer = setInterval(() => {
      setCurrentStep(prev => {
        if (prev < steps.length - 1) {
          setCompletedSteps(completed => [...completed, prev])
          return prev + 1
        } else {
          setCompletedSteps(completed => [...completed, prev])
          clearInterval(timer)
          return prev
        }
      })
    }, 15000) // 15 seconds per step (total ~90 seconds)

    return () => clearInterval(timer)
  }, [steps.length])

  const isCompleted = (index: number) => completedSteps.includes(index)
  const isCurrent = (index: number) => currentStep === index && !isCompleted(index)

  return (
    <div className="max-w-4xl mx-auto">
      <div className="text-center mb-8">
        <h2 className="text-3xl font-bold text-white mb-2">
          Building Your AI Agent System
        </h2>
        <p className="text-gray-400">
          Using CrewAI hierarchical orchestration with 8 specialized agents
        </p>
      </div>

      {/* Progress bar */}
      <div className="mb-8">
        <div className="bg-gray-700 h-2 rounded-full overflow-hidden">
          <motion.div
            className="bg-gradient-to-r from-purple-500 to-indigo-500 h-full"
            initial={{ width: "0%" }}
            animate={{ width: `${((completedSteps.length) / steps.length) * 100}%` }}
            transition={{ duration: 0.5 }}
          />
        </div>
        <div className="flex justify-between mt-2">
          <span className="text-sm text-gray-400">
            {completedSteps.length} of {steps.length} stages complete
          </span>
          <span className="text-sm text-gray-400">
            ~{Math.max(0, (steps.length - completedSteps.length) * 15)}s remaining
          </span>
        </div>
      </div>

      {/* Current requirement */}
      <div className="bg-gray-800/50 backdrop-blur-sm rounded-lg p-4 mb-8 border border-gray-700">
        <p className="text-sm text-gray-400 mb-1">Building system for:</p>
        <p className="text-white">{requirement}</p>
      </div>

      {/* Steps */}
      <div className="space-y-4">
        {steps.map((step, index) => (
          <motion.div
            key={index}
            initial={{ opacity: 0, x: -20 }}
            animate={{ opacity: 1, x: 0 }}
            transition={{ delay: index * 0.1 }}
            className={`relative flex items-start p-4 rounded-lg border-2 transition-all ${
              isCompleted(index)
                ? 'bg-green-900/20 border-green-600'
                : isCurrent(index)
                ? 'bg-indigo-900/20 border-indigo-600'
                : 'bg-gray-800/20 border-gray-700'
            }`}
          >
            {/* Status icon */}
            <div className={`flex-shrink-0 w-10 h-10 rounded-full flex items-center justify-center mr-4 ${
              isCompleted(index)
                ? 'bg-green-600'
                : isCurrent(index)
                ? 'bg-indigo-600'
                : 'bg-gray-700'
            }`}>
              {isCompleted(index) ? (
                <CheckCircle className="h-5 w-5 text-white" />
              ) : isCurrent(index) ? (
                <Loader className="h-5 w-5 text-white animate-spin" />
              ) : (
                <div className="text-gray-400">{step.icon}</div>
              )}
            </div>

            {/* Step content */}
            <div className="flex-1">
              <h3 className={`font-semibold mb-1 ${
                isCompleted(index) || isCurrent(index) ? 'text-white' : 'text-gray-400'
              }`}>
                {step.name}
              </h3>
              <p className={`text-sm ${
                isCompleted(index) || isCurrent(index) ? 'text-gray-300' : 'text-gray-500'
              }`}>
                {step.description}
              </p>
              {isCurrent(index) && (
                <motion.div
                  initial={{ opacity: 0 }}
                  animate={{ opacity: 1 }}
                  className="mt-2 flex items-center text-xs text-indigo-400"
                >
                  <Loader className="h-3 w-3 mr-1 animate-spin" />
                  Estimated: {step.estimatedTime}
                </motion.div>
              )}
            </div>
          </motion.div>
        ))}
      </div>

      {/* Completion message */}
      {completedSteps.length === steps.length && !error && (
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          className="mt-8 text-center"
        >
          <div className="inline-flex items-center justify-center w-16 h-16 bg-green-600 rounded-full mb-4">
            <CheckCircle className="h-8 w-8 text-white" />
          </div>
          <h3 className="text-2xl font-bold text-white mb-2">System Generation Complete!</h3>
          <p className="text-gray-400">Your CrewAI system is ready for deployment</p>
        </motion.div>
      )}

      {/* Error state */}
      {error && (
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          className="mt-8 bg-red-900/20 border border-red-600 rounded-lg p-4"
        >
          <div className="flex items-start">
            <AlertCircle className="h-5 w-5 text-red-500 mr-2 flex-shrink-0 mt-0.5" />
            <div>
              <h4 className="font-semibold text-red-400 mb-1">Generation Failed</h4>
              <p className="text-sm text-gray-300">{error}</p>
            </div>
          </div>
        </motion.div>
      )}
    </div>
  )
}