// CrewBuilder Frontend - API Key Management Component
// Example of how users would provide API keys through web interface

import React, { useState, useEffect } from 'react'

interface APIKeySettingsProps {
  userId: string
  onKeysUpdated: (keys: Record<string, string>) => void
}

interface KeyStatus {
  has_openai_key?: boolean
  has_anthropic_key?: boolean
  openai?: boolean
  anthropic?: boolean
}

// API Key Management Component
export const APIKeySettings = ({ userId, onKeysUpdated }: APIKeySettingsProps) => {
  const [openaiKey, setOpenaiKey] = useState('')
  const [anthropicKey, setAnthropicKey] = useState('')
  const [showKeys, setShowKeys] = useState(false)
  const [saving, setSaving] = useState(false)
  const [keyStatus, setKeyStatus] = useState<KeyStatus>({})

  useEffect(() => {
    checkKeyStatus()
  }, [userId])

  const checkKeyStatus = async () => {
    try {
      const response = await fetch(`/api/user-keys/${userId}`)
      const status = await response.json()
      setKeyStatus(status)
    } catch (error) {
      console.error('Error checking key status:', error)
    }
  }

  const handleSaveKeys = async () => {
    setSaving(true)
    try {
      const response = await fetch('/api/user-keys', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          user_id: userId,
          openai_key: openaiKey || undefined,
          anthropic_key: anthropicKey || undefined
        })
      })

      if (response.ok) {
        const result = await response.json()
        console.log('Keys saved:', result)
        setOpenaiKey('')
        setAnthropicKey('')
        checkKeyStatus()
        onKeysUpdated?.(result)
      } else {
        console.error('Failed to save keys')
      }
    } catch (error) {
      console.error('Error saving keys:', error)
    } finally {
      setSaving(false)
    }
  }

  return (
    <div className="api-keys-settings p-6 bg-white rounded-lg shadow-lg">
      <h3 className="text-xl font-semibold mb-4">API Configuration</h3>
      
      {/* Current Status */}
      <div className="mb-6 p-4 bg-gray-50 rounded">
        <h4 className="font-medium mb-2">Current Status:</h4>
        <div className="space-y-1">
          <div className="flex items-center">
            <span className={`w-3 h-3 rounded-full mr-2 ${keyStatus.has_openai_key ? 'bg-green-500' : 'bg-gray-300'}`}></span>
            <span>OpenAI API Key {keyStatus.has_openai_key ? '✓ Connected' : '○ Not configured'}</span>
          </div>
          <div className="flex items-center">
            <span className={`w-3 h-3 rounded-full mr-2 ${keyStatus.has_anthropic_key ? 'bg-green-500' : 'bg-gray-300'}`}></span>
            <span>Anthropic API Key {keyStatus.has_anthropic_key ? '✓ Connected' : '○ Not configured'}</span>
          </div>
        </div>
      </div>

      {/* API Key Inputs */}
      <div className="space-y-4">
        <div>
          <label className="block text-sm font-medium mb-2">
            OpenAI API Key (Recommended)
          </label>
          <div className="relative">
            <input
              type={showKeys ? 'text' : 'password'}
              value={openaiKey}
              onChange={(e) => setOpenaiKey(e.target.value)}
              placeholder="sk-your-openai-api-key-here"
              className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
            />
          </div>
          <p className="text-xs text-gray-500 mt-1">
            Get your key from <a href="https://platform.openai.com/api-keys" target="_blank" className="text-blue-500">OpenAI Platform</a>
          </p>
        </div>

        <div>
          <label className="block text-sm font-medium mb-2">
            Anthropic API Key (Alternative)
          </label>
          <input
            type={showKeys ? 'text' : 'password'}
            value={anthropicKey}
            onChange={(e) => setAnthropicKey(e.target.value)}
            placeholder="sk-ant-your-anthropic-api-key-here"
            className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
          />
          <p className="text-xs text-gray-500 mt-1">
            Get your key from <a href="https://console.anthropic.com/" target="_blank" className="text-blue-500">Anthropic Console</a>
          </p>
        </div>

        {/* Show/Hide Toggle */}
        <div className="flex items-center">
          <input
            type="checkbox"
            id="showKeys"
            checked={showKeys}
            onChange={(e) => setShowKeys(e.target.checked)}
            className="mr-2"
          />
          <label htmlFor="showKeys" className="text-sm text-gray-600">
            Show API keys
          </label>
        </div>

        {/* Save Button */}
        <button
          onClick={handleSaveKeys}
          disabled={saving || (!openaiKey && !anthropicKey)}
          className="w-full bg-blue-600 text-white py-2 px-4 rounded-md hover:bg-blue-700 disabled:bg-gray-400 disabled:cursor-not-allowed"
        >
          {saving ? 'Saving...' : 'Save API Keys'}
        </button>
      </div>

      {/* Security Notice */}
      <div className="mt-6 p-4 bg-blue-50 rounded-md">
        <h4 className="font-medium text-blue-800 mb-2">🔒 Security & Privacy</h4>
        <ul className="text-sm text-blue-700 space-y-1">
          <li>• Keys are encrypted before storage</li>
          <li>• Only you can see or use your keys</li>
          <li>• Keys are never logged or shared</li>
          <li>• You can delete keys anytime</li>
        </ul>
      </div>

      {/* Cost Information */}
      <div className="mt-4 p-4 bg-yellow-50 rounded-md">
        <h4 className="font-medium text-yellow-800 mb-2">💡 Cost Information</h4>
        <ul className="text-sm text-yellow-700 space-y-1">
          <li>• Using your key: ~$0.02-$0.05 per generation</li>
          <li>• Without key: Free but limited analysis</li>
          <li>• OpenAI new accounts get $5 free credit</li>
          <li>• Set usage limits in your OpenAI dashboard</li>
        </ul>
      </div>
    </div>
  )
}

// Enhanced Generation Form with API Key Options
interface GenerationFormProps {
  userId: string
}

export const GenerationForm = ({ userId }: GenerationFormProps) => {
  const [requirement, setRequirement] = useState('')
  const [apiMode, setApiMode] = useState<string>('auto') // auto, fallback, own_key, session_key
  const [sessionKey, setSessionKey] = useState('')
  const [preferredModel, setPreferredModel] = useState('openai')
  const [generating, setGenerating] = useState(false)
  const [result, setResult] = useState<any>(null)

  const handleGenerate = async () => {
    setGenerating(true)
    setResult(null)

    try {
      const requestBody = {
        requirement,
        preferred_model: apiMode === 'fallback' ? 'fallback' : preferredModel
      }

      // Add session key if provided
      if (apiMode === 'session_key' && sessionKey) {
        requestBody.user_api_key = sessionKey
      }

      const response = await fetch('/api/generate', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(requestBody)
      })

      const generationResult = await response.json()
      setResult(generationResult)

    } catch (error) {
      console.error('Generation error:', error)
      setResult({ success: false, error: error.message })
    } finally {
      setGenerating(false)
    }
  }

  return (
    <div className="generation-form max-w-4xl mx-auto p-6">
      <h2 className="text-2xl font-bold mb-6">Generate AI Agent System</h2>

      {/* Business Requirement Input */}
      <div className="mb-6">
        <label className="block text-sm font-medium mb-2">
          Describe your business automation needs:
        </label>
        <textarea
          value={requirement}
          onChange={(e) => setRequirement(e.target.value)}
          placeholder="Example: I need to automate content creation for my digital marketing agency. The system should research trending topics, generate blog posts, optimize for SEO, and schedule social media posts..."
          rows={4}
          className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
        />
      </div>

      {/* API Mode Selection */}
      <div className="mb-6">
        <label className="block text-sm font-medium mb-3">AI Model Options:</label>
        <div className="space-y-3">
          <label className="flex items-center p-3 border rounded-md cursor-pointer hover:bg-gray-50">
            <input
              type="radio"
              value="auto"
              checked={apiMode === 'auto'}
              onChange={(e) => setApiMode(e.target.value)}
              className="mr-3"
            />
            <div>
              <div className="font-medium">🎯 Smart Mode (Recommended)</div>
              <div className="text-sm text-gray-600">Uses your saved API keys for enhanced analysis, falls back to basic mode</div>
            </div>
          </label>

          <label className="flex items-center p-3 border rounded-md cursor-pointer hover:bg-gray-50">
            <input
              type="radio"
              value="session_key"
              checked={apiMode === 'session_key'}
              onChange={(e) => setApiMode(e.target.value)}
              className="mr-3"
            />
            <div className="flex-1">
              <div className="font-medium">🔑 Use My API Key (One-time)</div>
              <div className="text-sm text-gray-600">Provide your API key for this generation only</div>
              {apiMode === 'session_key' && (
                <input
                  type="password"
                  value={sessionKey}
                  onChange={(e) => setSessionKey(e.target.value)}
                  placeholder="sk-your-api-key-here"
                  className="mt-2 w-full px-3 py-2 border border-gray-300 rounded-md text-sm"
                />
              )}
            </div>
          </label>

          <label className="flex items-center p-3 border rounded-md cursor-pointer hover:bg-gray-50">
            <input
              type="radio"
              value="fallback"
              checked={apiMode === 'fallback'}
              onChange={(e) => setApiMode(e.target.value)}
              className="mr-3"
            />
            <div>
              <div className="font-medium">⚡ Quick Mode (Free)</div>
              <div className="text-sm text-gray-600">Fast generation using smart templates and patterns</div>
            </div>
          </label>
        </div>
      </div>

      {/* Model Selection */}
      {(apiMode === 'auto' || apiMode === 'session_key') && (
        <div className="mb-6">
          <label className="block text-sm font-medium mb-2">Preferred AI Model:</label>
          <select
            value={preferredModel}
            onChange={(e) => setPreferredModel(e.target.value)}
            className="px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
          >
            <option value="openai">OpenAI GPT-4 (Most Accurate)</option>
            <option value="anthropic">Anthropic Claude (Alternative)</option>
          </select>
        </div>
      )}

      {/* Generate Button */}
      <button
        onClick={handleGenerate}
        disabled={!requirement.trim() || generating}
        className="w-full bg-gradient-to-r from-blue-600 to-purple-600 text-white py-3 px-6 rounded-md font-medium hover:from-blue-700 hover:to-purple-700 disabled:bg-gray-400 disabled:cursor-not-allowed"
      >
        {generating ? 'Generating AI Agent System...' : 'Generate System →'}
      </button>

      {/* Results Display */}
      {result && (
        <div className="mt-8 p-6 border rounded-lg">
          {result.success ? (
            <div>
              <div className="flex items-center mb-4">
                <span className="text-green-600 text-xl mr-2">✅</span>
                <h3 className="text-lg font-semibold">System Generated Successfully!</h3>
                <span className="ml-auto text-sm bg-blue-100 text-blue-800 px-2 py-1 rounded">
                  {result.api_mode} mode
                </span>
              </div>
              
              <div className="grid md:grid-cols-2 gap-4">
                <div>
                  <h4 className="font-medium mb-2">System Overview</h4>
                  <ul className="text-sm space-y-1">
                    <li><strong>Name:</strong> {result.data.systemName}</li>
                    <li><strong>Complexity:</strong> {result.data.complexity}</li>
                    <li><strong>Agents:</strong> {result.data.agents}</li>
                    <li><strong>Runtime:</strong> {result.data.estimatedTime}</li>
                  </ul>
                </div>
                <div>
                  <h4 className="font-medium mb-2">Cost Estimate</h4>
                  <ul className="text-sm space-y-1">
                    <li><strong>Generation:</strong> {result.cost_info?.estimated_api_cost}</li>
                    <li><strong>System Cost:</strong> {result.cost_info?.generation_cost}</li>
                    <li><strong>Monthly:</strong> {result.cost_info?.total_monthly_estimate}</li>
                  </ul>
                </div>
              </div>
            </div>
          ) : (
            <div className="text-red-600">
              <span className="text-xl mr-2">❌</span>
              Error: {result.error}
            </div>
          )}
        </div>
      )}
    </div>
  )
}

export default GenerationForm
