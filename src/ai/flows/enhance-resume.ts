'use server';

/**
 * @fileOverview Enhances a resume based on a job description.
 *
 * - enhanceResumeWithJobDescription - A function that enhances the resume content.
 * - EnhanceResumeInput - The input type for the enhanceResumeWithJobDescription function.
 * - EnhanceResumeOutput - The return type for the enhanceResumeWithJobDescription function.
 */

import {ai} from '@/ai/genkit';
import {z} from 'genkit';

const EnhanceResumeInputSchema = z.object({
  resumeContent: z
    .string()
    .describe('The content of the resume to be enhanced.'),
  jobDescription: z
    .string()
    .describe('The job description used to enhance the resume.'),
});
export type EnhanceResumeInput = z.infer<typeof EnhanceResumeInputSchema>;

const EnhanceResumeOutputSchema = z.object({
  enhancedResume: z
    .string()
    .describe('The enhanced resume content based on the job description.'),
  summary: z
    .string()
    .describe('A summary of the changes made to the resume.'),
});
export type EnhanceResumeOutput = z.infer<typeof EnhanceResumeOutputSchema>;

export async function enhanceResumeWithJobDescription(
  input: EnhanceResumeInput
): Promise<EnhanceResumeOutput> {
  return enhanceResumeFlow(input);
}

const enhanceResumePrompt = ai.definePrompt({
  name: 'enhanceResumePrompt',
  input: {schema: EnhanceResumeInputSchema},
  output: {schema: EnhanceResumeOutputSchema},
  prompt: `You are an expert resume writer. Given the following resume content and job description, suggest improvements to the resume content based on the job description, focusing on relevant skills and experience.

Resume Content: {{{resumeContent}}}

Job Description: {{{jobDescription}}}

Please provide the enhanced resume content, and a summary of changes made.

Output in a JSON format:
{
    "enhancedResume": "The enhanced resume content.",
    "summary": "A summary of the changes made to the resume."
}
`,
});

const enhanceResumeFlow = ai.defineFlow(
  {
    name: 'enhanceResumeFlow',
    inputSchema: EnhanceResumeInputSchema,
    outputSchema: EnhanceResumeOutputSchema,
  },
  async input => {
    const {output} = await enhanceResumePrompt(input);
    return output!;
  }
);
