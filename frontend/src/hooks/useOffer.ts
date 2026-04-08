import { useCopilotAction, useCoAgent } from '@copilotkit/react-core'
import { generateOfferMarkdown } from '../lib/offerMarkdown'

export interface OfferParams {
  project_description: string
  services_list: string
  project_scope: string
}

interface OfferState {
  offerContent: string
  hasOffer: boolean
  projectDescription: string
  servicesList: string
  projectScope: string
}

const initialState: OfferState = {
  offerContent: '',
  hasOffer: false,
  projectDescription: '',
  servicesList: '',
  projectScope: '',
}

export function useOffer() {
  const { state, setState } = useCoAgent<OfferState>({
    name: 'default',
    initialState,
  })

  useCopilotAction({
    name: 'preview_offer',
    description: 'Display a proposal draft in the markdown editor on the left panel',
    parameters: [
      {
        name: 'project_description',
        type: 'string',
        description: '2-4 sentence project description inferred from the conversation',
        required: true,
      },
      {
        name: 'services_list',
        type: 'string',
        description: 'Comma-separated list of recommended Notch services',
        required: true,
      },
      {
        name: 'project_scope',
        type: 'string',
        description: 'Project scope estimate: small, medium, or large',
        required: true,
      },
    ],
    handler: async ({ project_description, services_list, project_scope }) => {
      const markdown = generateOfferMarkdown(
        project_description,
        services_list,
        project_scope,
      )
      setState({
        offerContent: markdown,
        hasOffer: true,
        projectDescription: project_description,
        servicesList: services_list,
        projectScope: project_scope,
      })
      return 'Proposal draft displayed to user in the editor on the left.'
    },
  })

  return {
    offerContent: state.offerContent,
    setOfferContent: (content: string) => setState({ ...state, offerContent: content }),
    hasOffer: state.hasOffer,
    offerParams: state.hasOffer
      ? {
          project_description: state.projectDescription,
          services_list: state.servicesList,
          project_scope: state.projectScope,
        }
      : null,
  }
}
