'use client'

import { useState } from 'react'
import { motion } from 'framer-motion'
import { Sparkles, ArrowRight, Users, Cog, Monitor } from 'lucide-react'
import RequirementInput from '../components/RequirementInput'
import ClarificationConversation from '../components/ClarificationConversation'
import GenerationProgressV2 from '../components/GenerationProgressV2'
import SystemOutput from '../components/SystemOutput'
import DeploymentFlow from '../components/DeploymentFlow'

export default function Home() {
  const [currentStep, setCurrentStep] = useState<'input' | 'clarifying' | 'generating' | 'complete' | 'deploying'>('input')
  const [generatedSystem, setGeneratedSystem] = useState(null)
  const [userRequirement, setUserRequirement] = useState('')
  const [deploymentInfo, setDeploymentInfo] = useState(null)
  const [clarificationData, setClarificationData] = useState<any>(null)
  const [clarificationHistory, setClarificationHistory] = useState<any[]>([])

  const handleStartGeneration = async (requirement: string) => {
    setUserRequirement(requirement)
    setCurrentStep('clarifying')
    
    try {
      // First, get clarification questions
      const clarifyResponse = await fetch(`${process.env.NEXT_PUBLIC_API_URL || 'https://web-production-bd955.up.railway.app'}/api/clarify`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ requirement }),
      })

      if (!clarifyResponse.ok) {
        throw new Error('Clarification failed')
      }

      const clarifyResult = await clarifyResponse.json()
      
      if (clarifyResult.success) {
        setClarificationData(clarifyResult)
      } else {
        // If clarification fails, skip to generation
        handleSkipClarification()
      }
    } catch (error) {
      console.error('Clarification error:', error)
      // Skip clarification and go straight to generation
      handleSkipClarification()
    }
  }

  const handleClarificationComplete = async (conversationHistory: any[]) => {
    setClarificationHistory(conversationHistory)
    setCurrentStep('generating')
    
    // Generate with the conversation context
    await generateSystem(userRequirement, false)
  }

  const handleSkipClarification = async () => {
    setCurrentStep('generating')
    await generateSystem(userRequirement, true)
  }

  const generateSystem = async (requirement: string, skipClarification: boolean) => {
    try {
      const response = await fetch(`${process.env.NEXT_PUBLIC_API_URL || 'https://web-production-bd955.up.railway.app'}/api/generate`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ 
          requirement,
          skip_clarification: skipClarification 
        }),
      })

      if (!response.ok) {
        throw new Error('Generation failed')
      }

      const result = await response.json()
      
      if (result.success) {
        setGeneratedSystem(result.data)
        setCurrentStep('complete')
      } else {
        throw new Error(result.error || 'Unknown error')
      }
    } catch (error) {
      console.error('Generation error:', error)
      alert('Failed to generate system. Please try again.')
      setCurrentStep('input')
    }
  }

  const handleDeploy = async (apiKeys: Record<string, string>) => {
    setCurrentStep('deploying')
    
    try {
      const response = await fetch(`${process.env.NEXT_PUBLIC_API_URL || 'https://web-production-bd955.up.railway.app'}/api/deploy`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ 
          requirement: userRequirement,
          api_keys: apiKeys,
          deploy_to_railway: true
        }),
      })

      if (!response.ok) {
        const error = await response.json()
        throw new Error(error.detail || 'Deployment failed')
      }

      const result = await response.json()
      
      if (result.success) {
        setDeploymentInfo(result)
        // Show deployment success
        alert(`System deployed successfully! Visit: ${result.deployment_url}`)
      } else {
        throw new Error(result.error || 'Unknown error')
      }
    } catch (error) {
      console.error('Deployment error:', error)
      alert(`Failed to deploy: ${error instanceof Error ? error.message : 'Unknown error'}`)
      setCurrentStep('complete')
    }
  }

  return (
    <main className="min-h-screen bg-gradient-to-br from-gray-900 via-purple-900/20 to-gray-900">
      {/* Header */}
      <header className="bg-gray-900/50 backdrop-blur-sm border-b border-gray-800">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-4">
          <div className="flex items-center justify-between">
            <div className="flex items-center space-x-3">
              <Sparkles className="h-8 w-8 text-purple-400" />
              <h1 className="text-2xl font-bold text-white">CrewBuilder</h1>
              <span className="text-sm text-gray-400">AI Agent Meta-System</span>
            </div>
            <div className="flex items-center space-x-4">
              <span className="text-sm text-gray-400">V2: Proper CrewAI Patterns</span>
              <div className="flex items-center space-x-1">
                <div className="w-2 h-2 bg-green-500 rounded-full"></div>
                <span className="text-xs text-gray-400">8 Specialist Agents</span>
              </div>
            </div>
          </div>
        </div>
      </header>

      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {/* Hero Section */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          className="text-center mb-12"
        >
          <h2 className="text-4xl font-bold text-gray-900 mb-4">
            Build AI Agent Systems with 
            <span className="text-indigo-600"> Intelligence</span>
          </h2>
          <p className="text-xl text-gray-600 mb-8 max-w-3xl mx-auto">
            Describe your business automation needs in natural language. 
            Our learning-enhanced system generates, deploys, and monitors complete CrewAI systems.
          </p>
          
          {/* Features */}
          <div className="grid md:grid-cols-3 gap-6 mb-12">
            <div className="bg-white p-6 rounded-lg shadow-md">
              <Users className="h-12 w-12 text-indigo-600 mx-auto mb-4" />
              <h3 className="text-lg font-semibold mb-2">Proper CrewAI Patterns</h3>
              <p className="text-gray-600">8 specialist agents with hierarchical orchestration following best practices</p>
            </div>
            <div className="bg-white p-6 rounded-lg shadow-md">
              <Cog className="h-12 w-12 text-indigo-600 mx-auto mb-4" />
              <h3 className="text-lg font-semibold mb-2">Real Deployment</h3>
              <p className="text-gray-600">Complete infrastructure, monitoring, and hosting automation</p>
            </div>
            <div className="bg-white p-6 rounded-lg shadow-md">
              <Monitor className="h-12 w-12 text-indigo-600 mx-auto mb-4" />
              <h3 className="text-lg font-semibold mb-2">Continuous Learning</h3>
              <p className="text-gray-600">System improves with feedback and successful deployment patterns</p>
            </div>
          </div>
        </motion.div>

        {/* Main Interface */}
        <div className="bg-gray-800/50 backdrop-blur-sm rounded-xl shadow-2xl p-8 border border-gray-700">
          {currentStep === 'input' && (
            <RequirementInput onStartGeneration={handleStartGeneration} />
          )}
          
          {currentStep === 'clarifying' && (
            <ClarificationConversation
              requirement={userRequirement}
              sessionId={clarificationData?.session_id || `session_${Date.now()}`}
              onComplete={handleClarificationComplete}
              onSkip={handleSkipClarification}
            />
          )}
          
          {currentStep === 'generating' && (
            <GenerationProgressV2 requirement={userRequirement} />
          )}
          
          {currentStep === 'complete' && generatedSystem && (
            <>
              <SystemOutput 
                system={generatedSystem} 
                onStartNew={() => setCurrentStep('input')} 
              />
              <div className="mt-8">
                <DeploymentFlow
                  requirement={userRequirement}
                  onDeploy={handleDeploy}
                  isDeploying={false}
                />
              </div>
            </>
          )}
          
          {currentStep === 'deploying' && (
            <div className="text-center py-12">
              <div className="animate-spin rounded-full h-16 w-16 border-b-2 border-purple-400 mx-auto mb-4"></div>
              <h3 className="text-xl font-semibold mb-2 text-white">Deploying to Railway...</h3>
              <p className="text-gray-400">Your AI agent system is being deployed. This may take a few minutes.</p>
            </div>
          )}
        </div>
      </div>
    </main>
  )
}