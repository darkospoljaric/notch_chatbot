import { useState } from 'react'
import MDEditor from '@uiw/react-md-editor'
import SendOfferModal from './SendOfferModal'
import type { OfferParams } from '../hooks/useOffer'

interface Props {
  content: string
  onChange: (value: string) => void
  hasOffer: boolean
  offerParams: OfferParams | null
}

export default function MarkdownEditor({ content, onChange, hasOffer, offerParams }: Props) {
  const [showModal, setShowModal] = useState(false)

  return (
    <div className="flex flex-col h-full bg-white border-r border-gray-200">
      {/* Header */}
      <div className="flex items-center justify-between px-4 py-3 border-b border-gray-200 bg-gray-50">
        <div className="flex items-center gap-2">
          <span className="text-gray-500">📄</span>
          <span className="font-medium text-gray-700 text-sm">Offer Draft</span>
          {hasOffer && (
            <span className="text-xs bg-blue-100 text-blue-700 px-2 py-0.5 rounded-full">
              Ready
            </span>
          )}
        </div>
      </div>

      {/* Editor area */}
      <div className="flex-1 overflow-hidden" data-color-mode="light">
        {hasOffer ? (
          <MDEditor
            value={content}
            onChange={(val) => onChange(val ?? '')}
            height="100%"
            preview="live"
            style={{ height: '100%', borderRadius: 0, border: 'none' }}
          />
        ) : (
          <div className="flex flex-col items-center justify-center h-full text-center px-8 text-gray-400">
            <div className="text-5xl mb-4">📋</div>
            <p className="text-lg font-medium mb-2">No proposal yet</p>
            <p className="text-sm">
              Chat with the assistant about your project. Once it has enough context, a
              draft proposal will appear here automatically.
            </p>
          </div>
        )}
      </div>

      {/* Footer with Send button */}
      <div className="px-4 py-3 border-t border-gray-200 bg-gray-50">
        <button
          onClick={() => setShowModal(true)}
          disabled={!hasOffer}
          className="w-full px-4 py-2 bg-blue-600 text-white rounded-lg font-medium hover:bg-blue-700 disabled:opacity-40 disabled:cursor-not-allowed transition-colors"
        >
          Send Offer
        </button>
      </div>

      {showModal && offerParams && (
        <SendOfferModal
          offerParams={offerParams}
          onClose={() => setShowModal(false)}
        />
      )}
    </div>
  )
}
