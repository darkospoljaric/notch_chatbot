import { CopilotKit } from '@copilotkit/react-core'
import MarkdownEditor from './components/MarkdownEditor'
import ChatPanel from './components/ChatPanel'
import { useOffer } from './hooks/useOffer'

function AppContent() {
  const { offerContent, setOfferContent, hasOffer, offerParams } = useOffer()

  return (
    <div className="flex h-screen bg-white">
      {/* Left column — Offer draft */}
      <div className="w-1/2 flex flex-col min-h-0">
        <MarkdownEditor
          content={offerContent}
          onChange={setOfferContent}
          hasOffer={hasOffer}
          offerParams={offerParams}
        />
      </div>

      {/* Right column — Chat */}
      <div className="w-1/2 flex flex-col min-h-0 border-l border-gray-200">
        <ChatPanel />
      </div>
    </div>
  )
}

export default function App() {
  return (
    <CopilotKit runtimeUrl="/api/ag-ui">
      <AppContent />
    </CopilotKit>
  )
}
