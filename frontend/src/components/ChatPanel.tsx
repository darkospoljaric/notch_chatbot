import { CopilotChat } from '@copilotkit/react-ui'
import '@copilotkit/react-ui/styles.css'

export default function ChatPanel() {
  return (
    <div className="flex flex-col h-full">
      {/* Header */}
      <div className="flex items-center gap-2 px-4 py-3 border-b border-gray-200 bg-gray-50">
        <span className="text-gray-500">💬</span>
        <span className="font-medium text-gray-700 text-sm">Chat with Notch</span>
      </div>

      {/* Chat */}
      <div className="flex-1 overflow-hidden">
        <CopilotChat
          instructions="You are a helpful assistant for Notch, a software development agency. Help prospects understand Notch's services, share case studies, and guide them toward scheduling a call or requesting a proposal. Keep responses concise (2-3 sentences). When you have enough project context, call the preview_offer action to populate the proposal editor on the left."
          labels={{
            title: 'Notch Assistant',
            initial: "Hi! I'm here to help you explore Notch's services. What kind of project are you considering?",
          }}
          className="h-full"
        />
      </div>
    </div>
  )
}
