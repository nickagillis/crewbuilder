'use client'

import { useState, useEffect } from 'react'
import { motion } from 'framer-motion'
import { CheckCircle, Clock, Cog, Brain, Code, Shield, FileText, Cloud, Rocket, Eye } from 'lucide-react'

interface GenerationProgressProps {
  requirement: string
}

export default function GenerationProgress({ requirement }: GenerationProgressProps) {
  const [currentStep, setCurrentStep] = useState(0)
  const [completedSteps, setCompletedSteps] = useState<number[]>([])

  // 10-agent pipeline steps
  const steps = [
    { 
      name: "Requirements Analyst", 
      icon: <Brain className="h-5 w-5" />,
      description: "Analyzing business requirements and technical specifications",
      estimatedTime: "30s"
    },
    { 
      name: "System Architect", 
      icon: <Cog className="h-5 w-5" />,
      description: "Designing optimal crew architecture and agent specifications",
      estimatedTime: "45s"
    },
    { 
      name: "Code Generator", 
      icon: <Code className="h-5 w-5" />,
      description: "Converting architecture to production-ready Python code",
      estimatedTime: "60s"
    },
    { 
      name: "Quality Assurance", 
      icon: <Shield className="h-5 w-5" />,
      description: "Validating code quality, security, and performance",
      estimatedTime: "30s"
    },
    { 
      name: "API Detective", 
      icon: <Eye className="h-5 w-5" />,
      description: "Identifying APIs, cost analysis, and integration planning",
      estimatedTime: "45s"
    },
    { 
      name: "Documentation Specialist", 
      icon: <FileText className="h-5 w-5" />,
      description: "Generating user guides and technical documentation",
      estimatedTime: "40s"
    },
    { 
      name: "Infrastructure Analyst", 
      icon: <Cloud className="h-5 w-5" />,
      description: "Evaluating hosting platforms and infrastructure needs",
      estimatedTime: "35s"
    },
    { 
      name: "Deployment Engineer", 
      icon: <Rocket className="h-5 w-5" />,
      description: "Creating automated deployment configurations",
      estimatedTime: "50s"
    },
    { 
      name: "Hosting Assistant", 
      icon: <Cloud className="h-5 w-5" />,
      description: "Setting up platform guidance and user onboarding",
      estimatedTime: "25s"
    },
    { 
      name: "Monitoring Engineer", 
      icon: <Eye className="h-5 w-5" />,
      description: "Implementing comprehensive monitoring and alerting",
      estimatedTime: "40s"
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
    }, 500) // Progress every 500ms for demo

    return () => clearInterval(timer)
  }, [steps.length])

  const isCompleted = (index: number) => completedSteps.includes(index)
  const isCurrent = (index: number) => currentStep === index && !isCompleted(index)

  return (
    <div className="space-y-8">
      <div className="text-center">
        <h3 className="text-2xl font-bold text-gray-900 mb-4">
          Generating Your AI Agent System
        </h3>
        <p className="text-gray-600 mb-2">
          Our 10-agent pipeline is analyzing your requirements and building a complete system
        </p>
        <div className="bg-gray-100 p-3 rounded-lg max-w-3xl mx-auto">
          <p className="text-sm text-gray-700 italic">
            "{requirement}"
          </p>
        </div>
      </div>

      {/* Progress Overview */}
      <div className="bg-gradient-to-r from-indigo-50 to-blue-50 p-6 rounded-lg">
        <div className="flex items-center justify-between mb-4">
          <h4 className="font-semibold text-gray-900">Generation Progress</h4>
          <span className="text-sm text-gray-600">
            {completedSteps.length} of {steps.length} agents complete
          </span>
        </div>
        <div className="w-full bg-gray-200 rounded-full h-2">
          <motion.div
            className="bg-indigo-600 h-2 rounded-full"
            initial={{ width: 0 }}
            animate={{ width: `${(completedSteps.length / steps.length) * 100}%` }}
            transition={{ duration: 0.5 }}
          />
        </div>
      </div>

      {/* Agent Steps */}
      <div className="space-y-4">
        {steps.map((step, index) => (
          <motion.div
            key={index}
            initial={{ opacity: 0, x: -20 }}
            animate={{ opacity: 1, x: 0 }}
            transition={{ delay: index * 0.1 }}
            className={`flex items-center space-x-4 p-4 rounded-lg border-2 transition-all ${
              isCompleted(index)
                ? 'bg-green-50 border-green-200'
                : isCurrent(index)
                ? 'bg-blue-50 border-blue-200'
                : 'bg-gray-50 border-gray-200'
            }`}
          >
            <div className={`flex-shrink-0 p-2 rounded-full ${
              isCompleted(index)
                ? 'bg-green-100 text-green-600'
                : isCurrent(index)
                ? 'bg-blue-100 text-blue-600'
                : 'bg-gray-100 text-gray-400'
            }`}>
              {isCompleted(index) ? (
                <CheckCircle className="h-5 w-5" />
              ) : isCurrent(index) ? (
                <motion.div
                  animate={{ rotate: 360 }}
                  transition={{ duration: 2, repeat: Infinity, ease: "linear" }}
                >
                  {step.icon}
                </motion.div>
              ) : (
                step.icon
              )}
            </div>
            
            <div className="flex-1">
              <div className="flex items-center justify-between">
                <h5 className={`font-medium ${
                  isCompleted(index) ? 'text-green-900' : 
                  isCurrent(index) ? 'text-blue-900' : 'text-gray-500'
                }`}>
                  {step.name}
                </h5>
                <span className="text-xs text-gray-500">
                  {step.estimatedTime}
                </span>
              </div>
              <p className={`text-sm ${
                isCompleted(index) ? 'text-green-700' : 
                isCurrent(index) ? 'text-blue-700' : 'text-gray-400'
              }`}>
                {step.description}
              </p>
            </div>

            {isCurrent(index) && (
              <motion.div
                animate={{ opacity: [0.5, 1, 0.5] }}
                transition={{ duration: 1.5, repeat: Infinity }}
                className="flex-shrink-0"
              >
                <Clock className="h-4 w-4 text-blue-600" />
              </motion.div>
            )}
          </motion.div>
        ))}
      </div>

      {/* Learning Insights */}
      <div className="bg-indigo-50 p-6 rounded-lg">
        <h4 className="font-semibold text-indigo-900 mb-2">🧠 Learning Insights</h4>
        <p className="text-indigo-700 text-sm mb-2">
          Based on similar requirements, this system will likely include:
        </p>
        <ul className="text-indigo-700 text-sm space-y-1">
          <li>• 4-6 specialized agents for workflow automation</li>
          <li>• Integration with popular business tools (CRM, email, analytics)</li>
          <li>• Estimated 15-30 minute runtime per automation cycle</li>
          <li>• 87% success rate for similar business automation systems</li>
        </ul>
      </div>
    </div>
  )
}