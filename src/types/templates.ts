
export interface ResumeTemplateMeta {
  id: string;
  name: string;
  description: string;
  thumbnailUrl: string;
  dataAiHint: string;
}

export const availableTemplates: ResumeTemplateMeta[] = [
  {
    id: 'classic',
    name: 'Classic Professional',
    description: 'A timeless, elegant design suitable for all industries.',
    thumbnailUrl: 'https://placehold.co/200x280.png',
    dataAiHint: 'resume professional'
  },
  {
    id: 'modern',
    name: 'Modern Minimalist',
    description: 'Clean lines and a focus on content, perfect for tech roles.',
    thumbnailUrl: 'https://placehold.co/200x280.png',
    dataAiHint: 'resume modern'
  },
  {
    id: 'creative',
    name: 'Creative Column',
    description: 'A stylish two-column layout for creative professionals.',
    thumbnailUrl: 'https://placehold.co/200x280.png',
    dataAiHint: 'resume creative'
  },
  {
    id: 'academic',
    name: 'Academic CV',
    description: 'Detailed, comprehensive, ideal for research and academic roles.',
    thumbnailUrl: 'https://placehold.co/200x280.png',
    dataAiHint: 'cv academic'
  },
  {
    id: 'compact',
    name: 'Compact Info',
    description: 'Space-saving design to pack more information, great for experienced pros.',
    thumbnailUrl: 'https://placehold.co/200x280.png',
    dataAiHint: 'resume compact'
  }
];
