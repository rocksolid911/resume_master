
"use client";

import React from 'react';
import Image from 'next/image';
import { Card, CardContent, CardDescription, CardFooter, CardHeader, CardTitle } from '@/components/ui/card';
import { ScrollArea, ScrollBar } from '@/components/ui/scroll-area';
import { Button } from '@/components/ui/button';
import { CheckCircle } from 'lucide-react';
import { cn } from '@/lib/utils';
import type { ResumeTemplateMeta } from '@/types/templates';
import { availableTemplates } from '@/types/templates';

interface TemplateSelectorProps {
  selectedTemplateId: string;
  onSelectTemplate: (id: string) => void;
}

export const TemplateSelector: React.FC<TemplateSelectorProps> = ({ selectedTemplateId, onSelectTemplate }) => {
  return (
    <Card className="shadow-lg mb-6">
      <CardHeader>
        <CardTitle>Choose a Template</CardTitle>
        <CardDescription>Select a template for your resume. The preview below will update.</CardDescription>
      </CardHeader>
      <CardContent>
        <ScrollArea className="w-full whitespace-nowrap">
          <div className="flex space-x-4 pb-4">
            {availableTemplates.map((template) => (
              <Card
                key={template.id}
                className={cn(
                  "w-[220px] h-[380px] flex-shrink-0 cursor-pointer transition-all hover:shadow-xl flex flex-col",
                  selectedTemplateId === template.id ? "border-primary ring-2 ring-primary" : "border-border"
                )}
                onClick={() => onSelectTemplate(template.id)}
                role="button"
                tabIndex={0}
                onKeyDown={(e) => { if (e.key === 'Enter' || e.key === ' ') onSelectTemplate(template.id); }}
                aria-pressed={selectedTemplateId === template.id}
                aria-label={`Select ${template.name} template`}
              >
                <CardHeader className="p-3">
                  <CardTitle className="text-sm truncate">{template.name}</CardTitle>
                </CardHeader>
                <CardContent className="p-3 pt-0 flex flex-col items-center justify-center flex-grow">
                  <Image
                    src={template.thumbnailUrl}
                    alt={template.name}
                    width={180}
                    height={252}
                    className="rounded-sm border bg-muted object-cover"
                    data-ai-hint={template.dataAiHint}
                  />
                  <p className="text-xs text-muted-foreground mt-2 line-clamp-2 h-8 w-full text-center">{template.description}</p>
                </CardContent>
                <CardFooter className="p-3 pt-0">
                  <Button 
                    variant={selectedTemplateId === template.id ? "default" : "outline"} 
                    size="sm" 
                    className="w-full"
                    onClick={(e) => {
                        e.stopPropagation(); // prevent card click from firing again
                        onSelectTemplate(template.id);
                    }}
                    aria-label={selectedTemplateId === template.id ? `Current template: ${template.name}` : `Select ${template.name}`}
                  >
                    {selectedTemplateId === template.id && <CheckCircle className="mr-2 h-4 w-4" />}
                    {selectedTemplateId === template.id ? 'Selected' : 'Select'}
                  </Button>
                </CardFooter>
              </Card>
            ))}
          </div>
          <ScrollBar orientation="horizontal" />
        </ScrollArea>
      </CardContent>
    </Card>
  );
};
