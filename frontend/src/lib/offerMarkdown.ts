export function generateOfferMarkdown(
  description: string,
  services: string,
  scope: string,
): string {
  const pricing: Record<string, string> = {
    small: '$15k–$35k',
    medium: '$35k–$100k',
    large: '$100k+',
  }
  const estimate = pricing[scope] ?? pricing['medium']

  return `# Project Proposal

## Project Overview
${description}

## Recommended Services
${services}

## Team Composition
- Project Manager
- Senior Software Engineers
- UI/UX Designer
- QA Specialist
- DevOps Engineer (as needed)

## Investment Estimate
**${estimate}**

*Final pricing confirmed after consultation.*

## Next Steps
1. Review this proposal
2. Schedule a consultation call
3. Receive detailed project plan
4. Project kickoff

---
*This proposal is orientational and non-binding.*`
}
