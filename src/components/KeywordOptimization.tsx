"use client";

import React, { useState } from 'react';
import { Button } from '@/components/ui/button';
import { Textarea } from '@/components/ui/textarea';
import { Card, CardContent, CardDescription, CardFooter, CardHeader, CardTitle } from '@/components/ui/card';
import { Alert, AlertDescription, AlertTitle } from "@/components/ui/alert";
import { keywordOptimizeAndSummarize, KeywordOptimizeAndSummarizeInput } from '@/ai/flows/keyword-optimize-summarize';
import { Loader2, SearchCheck, FileText, ClipboardCopy, Check } from 'lucide-react';
import { useToast } from "@/hooks/use-toast";

interface KeywordOptimizationProps {
  currentResumeText: string;
}

export const KeywordOptimization: React.FC<KeywordOptimizationProps> = ({ currentResumeText }) => {
  const [jobDescription, setJobDescription] = useState('');
  const [optimizedResult, setOptimizedResult] = useState<{ optimizedResume: string; summary: string } | null>(null);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [isCopiedResume, setIsCopiedResume] = useState(false);
  const [isCopiedSummary, setIsCopiedSummary] = useState(false);
  const { toast } = useToast();

  const handleOptimize = async () => {
    if (!currentResumeText.trim()) {
      setError('Please input your resume details first in the "Input Resume" tab.');
      return;
    }
    if (!jobDescription.trim()) {
      setError('Please provide a job description for keyword optimization.');
      return;
    }

    setIsLoading(true);
    setError(null);
    setOptimizedResult(null);

    try {
      const input: KeywordOptimizeAndSummarizeInput = {
        resumeText: currentResumeText,
        jobDescription: jobDescription,
      };
      const result = await keywordOptimizeAndSummarize(input);
      setOptimizedResult(result);
    } catch (e) {
      console.error('Error optimizing resume:', e);
      setError('Failed to optimize resume. Please try again.');
       toast({
        title: "Error",
        description: "Failed to optimize resume. Please try again.",
        variant: "destructive",
      });
    } finally {
      setIsLoading(false);
    }
  };
  
  const copyToClipboard = (text: string, type: 'resume' | 'summary') => {
    navigator.clipboard.writeText(text).then(() => {
      if (type === 'resume') setIsCopiedResume(true);
      if (type === 'summary') setIsCopiedSummary(true);
      toast({ title: "Copied!", description: `${type === 'resume' ? 'Optimized resume' : 'Summary'} copied to clipboard.` });
      setTimeout(() => {
        if (type === 'resume') setIsCopiedResume(false);
        if (type === 'summary') setIsCopiedSummary(false);
      }, 2000);
    }).catch(err => {
      toast({ title: "Copy Failed", description: "Could not copy text to clipboard.", variant: "destructive" });
    });
  };


  return (
    <Card className="shadow-lg">
      <CardHeader>
        <CardTitle className="flex items-center"><SearchCheck className="mr-2 h-6 w-6 text-accent" /> Keyword Optimization & Summarization</CardTitle>
        <CardDescription>Provide a job description to optimize your resume with relevant keywords and generate a concise summary.</CardDescription>
      </CardHeader>
      <CardContent className="space-y-4">
        <div>
          <label htmlFor="jobDescriptionOptimize" className="block text-sm font-medium mb-1">Job Description</label>
          <Textarea
            id="jobDescriptionOptimize"
            placeholder="Paste the job description here..."
            value={jobDescription}
            onChange={(e) => setJobDescription(e.target.value)}
            rows={8}
            className="focus:ring-accent focus:border-accent"
          />
        </div>
        {error && (
          <Alert variant="destructive">
            <AlertTitle>Error</AlertTitle>
            <AlertDescription>{error}</AlertDescription>
          </Alert>
        )}
      </CardContent>
      <CardFooter>
        <Button onClick={handleOptimize} disabled={isLoading} className="bg-accent hover:bg-accent/90 text-accent-foreground">
          {isLoading ? <Loader2 className="mr-2 h-4 w-4 animate-spin" /> : <SearchCheck className="mr-2 h-4 w-4" />}
          Optimize & Summarize
        </Button>
      </CardFooter>

      {optimizedResult && (
        <div className="p-6 space-y-6">
          <Separator />
          <div>
            <div className="flex justify-between items-center mb-2">
              <h3 className="text-xl font-semibold flex items-center"><FileText className="mr-2 h-5 w-5 text-primary" /> Optimized Resume</h3>
               <Button variant="ghost" size="sm" onClick={() => copyToClipboard(optimizedResult.optimizedResume, 'resume')}>
                {isCopiedResume ? <Check className="mr-2 h-4 w-4 text-green-500" /> : <ClipboardCopy className="mr-2 h-4 w-4" />}
                Copy
              </Button>
            </div>
            <Card className="bg-secondary/30 max-h-96 overflow-y-auto">
              <CardContent className="p-4">
                <pre className="whitespace-pre-wrap text-sm font-mono">{optimizedResult.optimizedResume}</pre>
              </CardContent>
            </Card>
             <p className="mt-2 text-xs text-muted-foreground">Review the optimized version and manually update your resume in the "Input Resume" tab.</p>
          </div>
          
          <div>
            <div className="flex justify-between items-center mb-2">
              <h3 className="text-xl font-semibold flex items-center"><FileText className="mr-2 h-5 w-5 text-primary" /> AI Generated Summary</h3>
               <Button variant="ghost" size="sm" onClick={() => copyToClipboard(optimizedResult.summary, 'summary')}>
                {isCopiedSummary ? <Check className="mr-2 h-4 w-4 text-green-500" /> : <ClipboardCopy className="mr-2 h-4 w-4" />}
                Copy
              </Button>
            </div>
            <Card className="bg-secondary/30">
              <CardContent className="p-4">
                <pre className="whitespace-pre-wrap text-sm">{optimizedResult.summary}</pre>
              </CardContent>
            </Card>
             <p className="mt-2 text-xs text-muted-foreground">You can use this summary in your resume or LinkedIn profile.</p>
          </div>
        </div>
      )}
    </Card>
  );
};
