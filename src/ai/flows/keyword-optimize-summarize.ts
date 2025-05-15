// src/ai/flows/keyword-optimize-summarize.ts
'use server';
/**
 * @fileOverview A flow to analyze a resume, optimize it with relevant keywords based on a provided job description, and provide a concise summary.
 *
 * - keywordOptimizeAndSummarize - A function that handles the resume analysis, optimization, and summarization process.
 * - KeywordOptimizeAndSummarizeInput - The input type for the keywordOptimizeAndSummarize function.
 * - KeywordOptimizeAndSummarizeOutput - The return type for the keywordOptimizeAndSummarize function.
 */

import {ai} from '@/ai/genkit';
import {z} from 'genkit';

const KeywordOptimizeAndSummarizeInputSchema = z.object({
  resumeText: z.string().describe('The text content of the resume.'),
  jobDescription: z.string().describe('The job description to tailor the resume to.'),
});
export type KeywordOptimizeAndSummarizeInput = z.infer<
  typeof KeywordOptimizeAndSummarizeInputSchema
>;

const KeywordOptimizeAndSummarizeOutputSchema = z.object({
  optimizedResume: z
    .string()
    .describe('The resume content optimized with relevant keywords.'),
  summary: z.string().describe('A concise summary of the resume.'),
});
export type KeywordOptimizeAndSummarizeOutput = z.infer<
  typeof KeywordOptimizeAndSummarizeOutputSchema
>;

export async function keywordOptimizeAndSummarize(
  input: KeywordOptimizeAndSummarizeInput
): Promise<KeywordOptimizeAndSummarizeOutput> {
  return keywordOptimizeAndSummarizeFlow(input);
}

const prompt = ai.definePrompt({
  name: 'keywordOptimizeAndSummarizePrompt',
  input: {schema: KeywordOptimizeAndSummarizeInputSchema},
  output: {schema: KeywordOptimizeAndSummarizeOutputSchema},
  prompt: `You are an expert resume optimizer.

  You will analyze the resume provided, and rewrite it to include keywords from the job description to tailor it to the role.
  You will also provide a concise summary of the resume.

  Resume:
  {{resumeText}}

  Job Description:
  {{jobDescription}}

  Optimized Resume:
  Summary: `,
});

const keywordOptimizeAndSummarizeFlow = ai.defineFlow(
  {
    name: 'keywordOptimizeAndSummarizeFlow',
    inputSchema: KeywordOptimizeAndSummarizeInputSchema,
    outputSchema: KeywordOptimizeAndSummarizeOutputSchema,
  },
  async input => {
    const {output} = await prompt(input);
    return output!;
  }
);
