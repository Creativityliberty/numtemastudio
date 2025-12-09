import Button from '@/components/common/Button'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/common/Card'
import Input from '@/components/common/Input'
import { Bell, Key, Lock, Palette, Save } from 'lucide-react'
import React, { useState } from 'react'

const SettingsPage: React.FC = () => {
  const [settings, setSettings] = useState({
    apiKey: '••••••••••••••••',
    apiUrl: 'http://localhost:8000',
    theme: 'dark',
    notifications: true,
    autoSave: true,
  })

  const [isSaved, setIsSaved] = useState(false)

  const handleSave = () => {
    setIsSaved(true)
    setTimeout(() => setIsSaved(false), 2000)
  }

  return (
    <div className="space-y-8 p-8">
      {/* Header */}
      <div>
        <h1 className="text-4xl font-bold text-slate-100">Settings</h1>
        <p className="mt-2 text-slate-400">Manage your preferences and configuration</p>
      </div>

      {/* API Configuration */}
      <Card>
        <CardHeader>
          <CardTitle className="flex items-center gap-2">
            <Key size={24} />
            API Configuration
          </CardTitle>
          <CardDescription>Configure your API settings</CardDescription>
        </CardHeader>
        <CardContent className="space-y-4">
          <Input
            label="API URL"
            value={settings.apiUrl}
            onChange={(e) => setSettings({ ...settings, apiUrl: e.target.value })}
            placeholder="http://localhost:8000"
          />
          <div>
            <label className="mb-2 block text-sm font-medium text-slate-200">API Key</label>
            <div className="flex gap-2">
              <Input
                type="password"
                value={settings.apiKey}
                onChange={(e) => setSettings({ ...settings, apiKey: e.target.value })}
                placeholder="Your API key"
              />
              <Button variant="secondary" size="md">
                Regenerate
              </Button>
            </div>
          </div>
        </CardContent>
      </Card>

      {/* Appearance */}
      <Card>
        <CardHeader>
          <CardTitle className="flex items-center gap-2">
            <Palette size={24} />
            Appearance
          </CardTitle>
          <CardDescription>Customize how the app looks</CardDescription>
        </CardHeader>
        <CardContent className="space-y-4">
          <div>
            <label className="mb-2 block text-sm font-medium text-slate-200">Theme</label>
            <select
              value={settings.theme}
              onChange={(e) => setSettings({ ...settings, theme: e.target.value })}
              className="w-full rounded-lg border border-slate-600 bg-slate-800/50 px-4 py-2 text-slate-100 transition-all focus:border-indigo-500 focus:outline-none focus:ring-2 focus:ring-indigo-500/20"
            >
              <option value="dark">Dark</option>
              <option value="light">Light</option>
              <option value="auto">Auto (System)</option>
            </select>
          </div>
        </CardContent>
      </Card>

      {/* Notifications */}
      <Card>
        <CardHeader>
          <CardTitle className="flex items-center gap-2">
            <Bell size={24} />
            Notifications
          </CardTitle>
          <CardDescription>Control notification preferences</CardDescription>
        </CardHeader>
        <CardContent className="space-y-4">
          <label className="flex items-center gap-3">
            <input
              type="checkbox"
              checked={settings.notifications}
              onChange={(e) => setSettings({ ...settings, notifications: e.target.checked })}
              className="h-4 w-4 rounded border-slate-600 bg-slate-800 text-indigo-600"
            />
            <span className="text-sm text-slate-100">Enable notifications</span>
          </label>
          <label className="flex items-center gap-3">
            <input
              type="checkbox"
              checked={settings.autoSave}
              onChange={(e) => setSettings({ ...settings, autoSave: e.target.checked })}
              className="h-4 w-4 rounded border-slate-600 bg-slate-800 text-indigo-600"
            />
            <span className="text-sm text-slate-100">Auto-save changes</span>
          </label>
        </CardContent>
      </Card>

      {/* Security */}
      <Card>
        <CardHeader>
          <CardTitle className="flex items-center gap-2">
            <Lock size={24} />
            Security
          </CardTitle>
          <CardDescription>Manage security settings</CardDescription>
        </CardHeader>
        <CardContent className="space-y-4">
          <Button variant="secondary" size="md" className="w-full">
            Change Password
          </Button>
          <Button variant="outline" size="md" className="w-full">
            Two-Factor Authentication
          </Button>
          <Button variant="danger" size="md" className="w-full">
            Logout All Sessions
          </Button>
        </CardContent>
      </Card>

      {/* Save Button */}
      <div className="flex gap-3">
        <Button
          variant="primary"
          size="lg"
          icon={<Save size={20} />}
          onClick={handleSave}
        >
          Save Settings
        </Button>
        {isSaved && (
          <div className="flex items-center gap-2 rounded-lg bg-green-500/20 px-4 py-2 text-green-400">
            <div className="h-2 w-2 rounded-full bg-green-400" />
            Settings saved successfully
          </div>
        )}
      </div>

      {/* About */}
      <Card>
        <CardHeader>
          <CardTitle>About</CardTitle>
        </CardHeader>
        <CardContent className="space-y-2">
          <div className="flex justify-between">
            <span className="text-slate-400">Version</span>
            <span className="text-slate-100">1.0.0</span>
          </div>
          <div className="flex justify-between">
            <span className="text-slate-400">Build</span>
            <span className="text-slate-100">2025.12</span>
          </div>
          <div className="flex justify-between">
            <span className="text-slate-400">Environment</span>
            <span className="text-slate-100">Production</span>
          </div>
        </CardContent>
      </Card>
    </div>
  )
}

export default SettingsPage
