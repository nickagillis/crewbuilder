'use client'

import { useState } from 'react'
import { ArrowRight, Key, Rocket, CheckCircle, AlertCircle } from 'lucide-react'

interface DeploymentFlowProps {
  requirement: string
  onDeploy: (apiKeys: Record<string, string>) => Promise<void>
  isDeploying: boolean
}

export default function DeploymentFlow({ requirement, onDeploy, isDeploying }: DeploymentFlowProps) {
  const [apiKeys, setApiKeys] = useState({
    OPENAI_API_KEY: '',
  })
  const [showApiKeyForm, setShowApiKeyForm] = useState(false)
  const [error, setError] = useState('')

  const handleApiKeyChange = (key: string, value: string) => {
    setApiKeys(prev => ({ ...prev, [key]: value }))
    setError('')
  }

  const handleDeploy = async () => {
    if (!apiKeys.OPENAI_API_KEY) {
      setError('OpenAI API key is required for deployment')
      return
    }

    try {
      await onDeploy(apiKeys)
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Deployment failed')
    }
  }

  return (
    <div className="space-y-6">
      {/* Deployment Option */}
      <div className="bg-gradient-to-r from-purple-500/10 to-pink-500/10 rounded-xl p-6 border border-purple-500/20">
        <h3 className="text-xl font-semibold mb-4 flex items-center gap-2">
          <Rocket className="w-6 h-6 text-purple-400" />
          Deploy to Railway
        </h3>
        
        <p className="text-gray-300 mb-4">
          Deploy your generated AI agent system directly to Railway with one click. 
          Your agents will be live and running in minutes!
        </p>

        {!showApiKeyForm ? (
          <button
            onClick={() => setShowApiKeyForm(true)}
            className="bg-gradient-to-r from-purple-500 to-pink-500 text-white px-6 py-3 rounded-lg 
                     hover:from-purple-600 hover:to-pink-600 transition-all duration-200 
                     flex items-center gap-2 font-medium"
          >
            Deploy System
            <ArrowRight className="w-5 h-5" />
          </button>
        ) : (
          <div className="space-y-4">
            {/* API Key Input */}
            <div>
              <label htmlFor="openai-key" className="block text-sm font-medium text-gray-300 mb-2">
                <Key className="w-4 h-4 inline mr-1" />
                OpenAI API Key
              </label>
              <input
                id="openai-key"
                type="password"
                value={apiKeys.OPENAI_API_KEY}
                onChange={(e) => handleApiKeyChange('OPENAI_API_KEY', e.target.value)}
                placeholder="sk-..."
                className="w-full px-4 py-2 bg-gray-800 border border-gray-700 rounded-lg 
                         focus:border-purple-500 focus:ring-1 focus:ring-purple-500 
                         text-white placeholder-gray-500"
              />
              <p className="text-xs text-gray-400 mt-1">
                Your API key will be securely stored in your Railway deployment
              </p>
            </div>

            {error && (
              <div className="flex items-center gap-2 text-red-400 text-sm">
                <AlertCircle className="w-4 h-4" />
                {error}
              </div>
            )}

            {/* Deploy Button */}
            <button
              onClick={handleDeploy}
              disabled={isDeploying || !apiKeys.OPENAI_API_KEY}
              className={`w-full py-3 rounded-lg font-medium transition-all duration-200 
                       flex items-center justify-center gap-2
                       ${isDeploying || !apiKeys.OPENAI_API_KEY
                         ? 'bg-gray-700 text-gray-400 cursor-not-allowed'
                         : 'bg-gradient-to-r from-purple-500 to-pink-500 text-white hover:from-purple-600 hover:to-pink-600'
                       }`}
            >
              {isDeploying ? (
                <>
                  <div className="animate-spin rounded-full h-5 w-5 border-b-2 border-white"></div>
                  Deploying to Railway...
                </>
              ) : (
                <>
                  <Rocket className="w-5 h-5" />
                  Deploy Now
                </>
              )}
            </button>
          </div>
        )}
      </div>

      {/* Benefits */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
        <div className="bg-gray-800/50 rounded-lg p-4 border border-gray-700">
          <CheckCircle className="w-5 h-5 text-green-400 mb-2" />
          <h4 className="font-medium mb-1">Live in Minutes</h4>
          <p className="text-sm text-gray-400">
            Your AI agents will be running on Railway's infrastructure immediately
          </p>
        </div>
        <div className="bg-gray-800/50 rounded-lg p-4 border border-gray-700">
          <CheckCircle className="w-5 h-5 text-green-400 mb-2" />
          <h4 className="font-medium mb-1">Fully Managed</h4>
          <p className="text-sm text-gray-400">
            Automatic scaling, monitoring, and maintenance included
          </p>
        </div>
        <div className="bg-gray-800/50 rounded-lg p-4 border border-gray-700">
          <CheckCircle className="w-5 h-5 text-green-400 mb-2" />
          <h4 className="font-medium mb-1">Cost Effective</h4>
          <p className="text-sm text-gray-400">
            Pay only for what you use, starting at $5/month
          </p>
        </div>
      </div>
    </div>
  )
}