"use client";

import React, { useState } from 'react';
import { Button } from '@/components/ui/button';
import { Textarea } from '@/components/ui/textarea';
import { Card, CardContent, CardDescription, CardFooter, CardHeader, CardTitle } from '@/components/ui/card';
import { Alert, AlertDescription, AlertTitle } from "@/components/ui/alert";
import { enhanceResumeWithJobDescription, EnhanceResumeInput } from '@/ai/flows/enhance-resume';
import { Loader2, Sparkles, FileText, ClipboardCopy, Check } from 'lucide-react';
import { useToast } from "@/hooks/use-toast";

interface AIEnhancementProps {
  currentResumeText: string;
}

export const AIEnhancement: React.FC<AIEnhancementProps> = ({ currentResumeText }) => {
  const [jobDescription, setJobDescription] = useState('');
  const [enhancedContent, setEnhancedContent] = useState<{ enhancedResume: string; summary: string } | null>(null);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [isCopiedResume, setIsCopiedResume] = useState(false);
  const [isCopiedSummary, setIsCopiedSummary] = useState(false);
  const { toast } = useToast();

  const handleEnhance = async () => {
    if (!currentResumeText.trim()) {
      setError('Please input your resume details first in the "Input Resume" tab.');
      return;
    }
    if (!jobDescription.trim()) {
      setError('Please provide a job description to enhance your resume.');
      return;
    }

    setIsLoading(true);
    setError(null);
    setEnhancedContent(null);

    try {
      const input: EnhanceResumeInput = {
        resumeContent: currentResumeText,
        jobDescription: jobDescription,
      };
      const result = await enhanceResumeWithJobDescription(input);
      setEnhancedContent(result);
    } catch (e) {
      console.error('Error enhancing resume:', e);
      setError('Failed to enhance resume. Please try again.');
      toast({
        title: "Error",
        description: "Failed to enhance resume. Please try again.",
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
      toast({ title: "Copied!", description: `${type === 'resume' ? 'Enhanced resume' : 'Summary'} copied to clipboard.` });
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
        <CardTitle className="flex items-center"><Sparkles className="mr-2 h-6 w-6 text-accent" /> AI Resume Enhancement</CardTitle>
        <CardDescription>Paste a job description below. Our AI will analyze your current resume and suggest improvements to tailor it for the role.</CardDescription>
      </CardHeader>
      <CardContent className="space-y-4">
        <div>
          <label htmlFor="jobDescriptionEnhance" className="block text-sm font-medium mb-1">Job Description</label>
          <Textarea
            id="jobDescriptionEnhance"
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
        <Button onClick={handleEnhance} disabled={isLoading} className="bg-accent hover:bg-accent/90 text-accent-foreground">
          {isLoading ? <Loader2 className="mr-2 h-4 w-4 animate-spin" /> : <Sparkles className="mr-2 h-4 w-4" />}
          Enhance Resume
        </Button>
      </CardFooter>

      {enhancedContent && (
        <div className="p-6 space-y-6">
          <Separator />
          <div>
            <div className="flex justify-between items-center mb-2">
              <h3 className="text-xl font-semibold flex items-center"><FileText className="mr-2 h-5 w-5 text-primary" /> Suggested Enhanced Resume</h3>
              <Button variant="ghost" size="sm" onClick={() => copyToClipboard(enhancedContent.enhancedResume, 'resume')}>
                {isCopiedResume ? <Check className="mr-2 h-4 w-4 text-green-500" /> : <ClipboardCopy className="mr-2 h-4 w-4" />}
                Copy
              </Button>
            </div>
            <Card className="bg-secondary/30 max-h-96 overflow-y-auto">
              <CardContent className="p-4">
                <pre className="whitespace-pre-wrap text-sm font-mono">{enhancedContent.enhancedResume}</pre>
              </CardContent>
            </Card>
            <p className="mt-2 text-xs text-muted-foreground">Review the suggestions and manually update your resume in the "Input Resume" tab.</p>
          </div>
          
          <div>
             <div className="flex justify-between items-center mb-2">
                <h3 className="text-xl font-semibold flex items-center"><FileText className="mr-2 h-5 w-5 text-primary" /> Summary of Changes</h3>
                <Button variant="ghost" size="sm" onClick={() => copyToClipboard(enhancedContent.summary, 'summary')}>
                  {isCopiedSummary ? <Check className="mr-2 h-4 w-4 text-green-500" /> : <ClipboardCopy className="mr-2 h-4 w-4" />}
                  Copy
                </Button>
              </div>
            <Card className="bg-secondary/30">
              <CardContent className="p-4">
                <pre className="whitespace-pre-wrap text-sm">{enhancedContent.summary}</pre>
              </CardContent>
            </Card>
          </div>
        </div>
      )}
    </Card>
  );
};
