'use client'

import { useState } from 'react'
import { motion } from 'framer-motion'
import { Sparkles, ArrowRight, Users, Cog, Monitor } from 'lucide-react'
import RequirementInput from '../components/RequirementInput'
import GenerationProgress from '../components/GenerationProgress'
import SystemOutput from '../components/SystemOutput'

export default function Home() {
  const [currentStep, setCurrentStep] = useState<'input' | 'generating' | 'complete'>('input')
  const [generatedSystem, setGeneratedSystem] = useState(null)
  const [userRequirement, setUserRequirement] = useState('')

  const handleStartGeneration = async (requirement: string) => {
    setUserRequirement(requirement)
    setCurrentStep('generating')
    
    try {
      const response = await fetch('/api/generate', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ requirement }),
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
      // Handle error state
      alert('Failed to generate system. Please try again.')
      setCurrentStep('input')
    }
  }

  return (
    <main className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100">
      {/* Header */}
      <header className="bg-white shadow-sm">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-4">
          <div className="flex items-center justify-between">
            <div className="flex items-center space-x-3">
              <Sparkles className="h-8 w-8 text-indigo-600" />
              <h1 className="text-2xl font-bold text-gray-900">CrewBuilder</h1>
              <span className="text-sm text-gray-500">AI Agent Meta-System</span>
            </div>
            <div className="flex items-center space-x-4">
              <span className="text-sm text-gray-600">Phase 2: Learning-Enhanced</span>
              <div className="flex items-center space-x-1">
                <div className="w-2 h-2 bg-green-500 rounded-full"></div>
                <span className="text-xs text-gray-500">10 Agents Active</span>
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
              <h3 className="text-lg font-semibold mb-2">Smart Generation</h3>
              <p className="text-gray-600">10-agent pipeline learns from every interaction to generate better systems</p>
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
        <div className="bg-white rounded-xl shadow-lg p-8">
          {currentStep === 'input' && (
            <RequirementInput onStartGeneration={handleStartGeneration} />
          )}
          
          {currentStep === 'generating' && (
            <GenerationProgress requirement={userRequirement} />
          )}
          
          {currentStep === 'complete' && generatedSystem && (
            <SystemOutput 
              system={generatedSystem} 
              onStartNew={() => setCurrentStep('input')} 
            />
          )}
        </div>
      </div>
    </main>
  )
}