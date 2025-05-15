
"use client";

import React, { useState, useRef, useEffect } from 'react';
import { Header } from '@/components/Header';
import { ResumeForm } from '@/components/ResumeForm';
import { AIEnhancement } from '@/components/AIEnhancement';
import { KeywordOptimization } from '@/components/KeywordOptimization';
import { TemplatePreview } from '@/components/TemplatePreview';
import { PdfExportButton } from '@/components/PdfExportButton';
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs';
import { ResumeData, initialResumeData, resumeDataToText } from '@/types/resume';
import { ScrollArea } from "@/components/ui/scroll-area";
import { TemplateSelector } from '@/components/TemplateSelector';
import { availableTemplates } from '@/types/templates';
import { Loader2 } from 'lucide-react';


const LOCAL_STORAGE_KEY = 'resuMasterAiData';
const LOCAL_STORAGE_TEMPLATE_KEY = 'resuMasterAiSelectedTemplate';

export default function HomePage() {
  const [resumeData, setResumeData] = useState<ResumeData>(initialResumeData);
  const [currentResumeText, setCurrentResumeText] = useState<string>('');
  const [activeTab, setActiveTab] = useState<string>("input");
  const [selectedTemplateId, setSelectedTemplateId] = useState<string>(availableTemplates[0]?.id || 'classic');
  const [isLoaded, setIsLoaded] = useState(false);

  const previewRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    const savedData = localStorage.getItem(LOCAL_STORAGE_KEY);
    if (savedData) {
      try {
        const parsedData = JSON.parse(savedData);
        setResumeData(parsedData);
        setCurrentResumeText(resumeDataToText(parsedData));
      } catch (error) {
        console.error("Failed to parse resume data from localStorage", error);
        localStorage.removeItem(LOCAL_STORAGE_KEY); 
        setResumeData(initialResumeData);
        setCurrentResumeText(resumeDataToText(initialResumeData));
      }
    } else {
       setResumeData(initialResumeData);
       setCurrentResumeText(resumeDataToText(initialResumeData));
    }

    const savedTemplateId = localStorage.getItem(LOCAL_STORAGE_TEMPLATE_KEY);
    if (savedTemplateId && availableTemplates.some(t => t.id === savedTemplateId)) {
      setSelectedTemplateId(savedTemplateId);
    } else {
      setSelectedTemplateId(availableTemplates[0]?.id || 'classic');
    }

    setIsLoaded(true);
  }, []);

  const handleFormChange = (newData: ResumeData) => {
    setResumeData(newData);
    setCurrentResumeText(resumeDataToText(newData));
    if (isLoaded) {
        localStorage.setItem(LOCAL_STORAGE_KEY, JSON.stringify(newData));
    }
  };

  const handleTemplateSelect = (templateId: string) => {
    setSelectedTemplateId(templateId);
    if (isLoaded) {
      localStorage.setItem(LOCAL_STORAGE_TEMPLATE_KEY, templateId);
    }
  };
  
  if (!isLoaded) {
    return (
      <div className="flex items-center justify-center min-h-screen">
        <Loader2 className="mr-2 h-8 w-8 animate-spin text-primary" />
        <div className="text-lg font-semibold">Loading ResuMaster AI...</div>
      </div>
    );
  }


  return (
    <div className="min-h-screen flex flex-col">
      <Header />
      <ScrollArea className="flex-grow">
        <div className="container mx-auto px-4 py-8">
          <Tabs value={activeTab} onValueChange={setActiveTab} className="w-full">
            <TabsList className="grid w-full grid-cols-2 sm:grid-cols-4 mb-6 shadow-sm">
              <TabsTrigger value="input">1. Input Resume</TabsTrigger>
              <TabsTrigger value="enhance">2. AI Enhance</TabsTrigger>
              <TabsTrigger value="optimize">3. Keyword Optimize</TabsTrigger>
              <TabsTrigger value="preview">4. Preview & Export</TabsTrigger>
            </TabsList>

            <TabsContent value="input">
              <ResumeForm initialData={resumeData} onFormChange={handleFormChange} />
            </TabsContent>

            <TabsContent value="enhance">
              <AIEnhancement currentResumeText={currentResumeText} />
            </TabsContent>

            <TabsContent value="optimize">
              <KeywordOptimization currentResumeText={currentResumeText} />
            </TabsContent>

            <TabsContent value="preview" className="space-y-6">
              <TemplateSelector
                selectedTemplateId={selectedTemplateId}
                onSelectTemplate={handleTemplateSelect}
              />
              <TemplatePreview 
                resumeData={resumeData} 
                previewRef={previewRef}
                selectedTemplateId={selectedTemplateId} 
              />
              <div className="text-center">
                <PdfExportButton 
                  targetRef={previewRef} 
                  resumeDataExists={!!resumeData.name}
                />
              </div>
            </TabsContent>
          </Tabs>
        </div>
      </ScrollArea>
      <footer className="py-4 text-center text-sm text-muted-foreground border-t">
        © {new Date().getFullYear()} ResuMaster AI. All rights reserved.
      </footer>
    </div>
  );
}
