'use client'

import { useState } from 'react'
import { motion } from 'framer-motion'
import { ArrowRight, Lightbulb, Building, TrendingUp } from 'lucide-react'

interface RequirementInputProps {
  onStartGeneration: (requirement: string) => void
}

export default function RequirementInput({ onStartGeneration }: RequirementInputProps) {
  const [requirement, setRequirement] = useState('')
  const [isLoading, setIsLoading] = useState(false)

  // Example prompts based on learning data (simulated)
  const examplePrompts = [
    {
      icon: <Building className="h-5 w-5" />,
      title: "Customer Service Automation",
      prompt: "I need to automate customer service emails: categorize inquiries, generate responses, escalate complex issues, and track satisfaction scores."
    },
    {
      icon: <TrendingUp className="h-5 w-5" />,
      title: "Content Marketing Pipeline", 
      prompt: "Automate content creation: research trending topics, generate blog posts, optimize for SEO, schedule social media, and track performance."
    },
    {
      icon: <Lightbulb className="h-5 w-5" />,
      title: "Sales Intelligence System",
      prompt: "Build a sales automation system: lead qualification, competitor analysis, proposal generation, and pipeline tracking with CRM integration."
    }
  ]

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault()
    if (requirement.trim()) {
      setIsLoading(true)
      onStartGeneration(requirement)
    }
  }

  const useExamplePrompt = (prompt: string) => {
    setRequirement(prompt)
  }

  return (
    <div className="space-y-8">
      <div className="text-center">
        <h3 className="text-2xl font-bold text-gray-900 mb-4">
          Describe Your Business Automation Need
        </h3>
        <p className="text-gray-600 mb-8">
          Our learning system will analyze your requirements and generate a complete AI agent system.
          Be as specific as possible about your workflow and goals.
        </p>
      </div>

      {/* Example Prompts */}
      <div className="mb-8">
        <h4 className="text-lg font-semibold text-gray-900 mb-4">Popular Automation Examples</h4>
        <div className="grid md:grid-cols-3 gap-4">
          {examplePrompts.map((example, index) => (
            <motion.div
              key={index}
              whileHover={{ scale: 1.02 }}
              className="bg-gray-50 p-4 rounded-lg border-2 border-transparent hover:border-indigo-200 cursor-pointer transition-all"
              onClick={() => useExamplePrompt(example.prompt)}
            >
              <div className="flex items-center space-x-2 mb-2">
                <div className="text-indigo-600">{example.icon}</div>
                <h5 className="font-medium text-gray-900">{example.title}</h5>
              </div>
              <p className="text-sm text-gray-600 line-clamp-3">{example.prompt}</p>
            </motion.div>
          ))}
        </div>
      </div>

      {/* Input Form */}
      <form onSubmit={handleSubmit} className="space-y-6">
        <div>
          <label htmlFor="requirement" className="block text-sm font-medium text-gray-700 mb-2">
            Business Requirement
          </label>
          <textarea
            id="requirement"
            value={requirement}
            onChange={(e) => setRequirement(e.target.value)}
            className="w-full h-32 px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-indigo-500 focus:border-transparent resize-none"
            placeholder="Example: I run a digital marketing agency and want to automate content creation. I need a system that can research trending topics, generate blog posts, optimize them for SEO, schedule social media posts, and track performance metrics across different platforms..."
            required
          />
          <div className="flex justify-between items-center mt-2">
            <span className="text-sm text-gray-500">
              {requirement.length} characters
            </span>
            <span className="text-sm text-gray-500">
              Tip: Include your industry, specific workflows, and desired outcomes
            </span>
          </div>
        </div>

        <motion.button
          type="submit"
          disabled={!requirement.trim() || isLoading}
          whileHover={{ scale: 1.02 }}
          whileTap={{ scale: 0.98 }}
          className="w-full bg-indigo-600 text-white py-4 px-6 rounded-lg font-semibold text-lg flex items-center justify-center space-x-2 hover:bg-indigo-700 disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
        >
          {isLoading ? (
            <div className="animate-spin rounded-full h-6 w-6 border-b-2 border-white"></div>
          ) : (
            <>
              <span>Generate AI Agent System</span>
              <ArrowRight className="h-5 w-5" />
            </>
          )}
        </motion.button>
      </form>

      {/* Learning Insights */}
      <div className="bg-indigo-50 p-6 rounded-lg">
        <h4 className="font-semibold text-indigo-900 mb-2">💡 Smart Suggestions</h4>
        <p className="text-indigo-700 text-sm">
          Based on successful patterns: Users in your industry typically benefit from systems that include 
          automated data collection, intelligent analysis, and multi-channel distribution. 
          Consider mentioning your current tools and integration needs.
        </p>
      </div>
    </div>
  )
}