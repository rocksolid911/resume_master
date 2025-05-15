
"use client";

import React from 'react';
import type { ResumeData } from '@/types/resume';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Separator } from '@/components/ui/separator';
import { Mail, Phone, Linkedin, Globe, Briefcase, GraduationCap, Lightbulb, FolderKanban, User, CalendarDays, Pin } from 'lucide-react';
import { cn } from '@/lib/utils';
import { availableTemplates } from '@/types/templates';


interface TemplatePreviewProps {
  resumeData: ResumeData | null;
  previewRef: React.RefObject<HTMLDivElement>;
  selectedTemplateId: string;
}

export const TemplatePreview: React.FC<TemplatePreviewProps> = ({ resumeData, previewRef, selectedTemplateId }) => {
  const selectedTemplateDetails = availableTemplates.find(t => t.id === selectedTemplateId);

  if (!resumeData || !resumeData.name) {
    return (
      <Card className="shadow-lg">
        <CardHeader>
          <CardTitle>Resume Preview</CardTitle>
          <CardDescription>Your resume will be previewed here once you input your details.</CardDescription>
        </CardHeader>
        <CardContent>
          <p className="text-muted-foreground text-center py-10">
            Please fill out the "Input Resume" form to see a preview.
          </p>
        </CardContent>
      </Card>
    );
  }

  return (
    <Card className="shadow-lg">
      <CardHeader>
        <CardTitle>Resume Preview</CardTitle>
        <CardDescription>
          Displaying preview for '{selectedTemplateDetails?.name || selectedTemplateId}' template. Use the button below to download as PDF.
        </CardDescription>
      </CardHeader>
      <CardContent>
        <div 
          ref={previewRef} 
          className={cn(
            "p-6 md:p-8 bg-card text-card-foreground rounded-lg border border-border print-friendly-preview",
            // Add specific classes or styles based on selectedTemplateId if needed for major layout changes
            // For now, font and color changes are applied directly to elements below.
            {
              'font-sans': selectedTemplateId === 'classic' || !selectedTemplateId,
              'font-mono': selectedTemplateId === 'modern',
              'font-serif': selectedTemplateId === 'creative', // Tailwind will use its default serif
            }
          )}
        >
          {/* Header */}
          <header className="text-center mb-6">
            <h1 className={cn(
                "text-3xl font-bold",
                selectedTemplateId === 'creative' ? "text-accent" : "text-primary"
                // Font family is now applied to the parent div for 'modern' and 'creative'
            )}>
                {resumeData.name}
            </h1>
            <div className="flex justify-center items-center space-x-4 text-sm text-muted-foreground mt-2 flex-wrap">
              {resumeData.email && <a href={`mailto:${resumeData.email}`} className="flex items-center hover:text-primary"><Mail className="mr-1 h-4 w-4" />{resumeData.email}</a>}
              {resumeData.phone && <span className="flex items-center"><Phone className="mr-1 h-4 w-4" />{resumeData.phone}</span>}
              {resumeData.linkedin && <a href={resumeData.linkedin} target="_blank" rel="noopener noreferrer" className="flex items-center hover:text-primary"><Linkedin className="mr-1 h-4 w-4" />LinkedIn</a>}
              {resumeData.portfolio && <a href={resumeData.portfolio} target="_blank" rel="noopener noreferrer" className="flex items-center hover:text-primary"><Globe className="mr-1 h-4 w-4" />Portfolio</a>}
            </div>
          </header>

          {/* Summary */}
          {resumeData.summary && (
            <section className="mb-6">
              <h2 className={cn(
                "text-xl font-semibold border-b-2 pb-1 mb-2 flex items-center",
                selectedTemplateId === 'creative' ? "text-accent border-accent" : "text-primary border-primary"
              )}><User className="mr-2 h-5 w-5"/> Summary</h2>
              <p className="text-sm leading-relaxed">{resumeData.summary}</p>
            </section>
          )}

          {/* Experience */}
          {resumeData.experiences.length > 0 && (
            <section className="mb-6">
               <h2 className={cn(
                "text-xl font-semibold border-b-2 pb-1 mb-2 flex items-center",
                selectedTemplateId === 'creative' ? "text-accent border-accent" : "text-primary border-primary"
              )}><Briefcase className="mr-2 h-5 w-5"/> Experience</h2>
              {resumeData.experiences.map((exp, index) => (
                <div key={exp.id || index} className="mb-4">
                  <h3 className="text-lg font-medium">{exp.jobTitle}</h3>
                  <p className="text-md font-semibold text-muted-foreground">{exp.company}</p>
                  <p className="text-xs text-muted-foreground mb-1 flex items-center">
                    <CalendarDays className="mr-1 h-3 w-3" /> {exp.startDate} - {exp.isCurrent ? 'Present' : exp.endDate}
                  </p>
                  <ul className="list-disc list-inside text-sm leading-relaxed space-y-1 pl-4">
                    {exp.responsibilities.split('\n').map((line, i) => line.trim() && <li key={i}>{line}</li>)}
                  </ul>
                </div>
              ))}
            </section>
          )}

          {/* Education */}
          {resumeData.educationItems.length > 0 && (
            <section className="mb-6">
               <h2 className={cn(
                "text-xl font-semibold border-b-2 pb-1 mb-2 flex items-center",
                selectedTemplateId === 'creative' ? "text-accent border-accent" : "text-primary border-primary"
              )}><GraduationCap className="mr-2 h-5 w-5"/> Education</h2>
              {resumeData.educationItems.map((edu, index) => (
                <div key={edu.id || index} className="mb-3">
                  <h3 className="text-lg font-medium">{edu.degree}</h3>
                  <p className="text-md font-semibold text-muted-foreground">{edu.institution}</p>
                  <p className="text-xs text-muted-foreground mb-1">Graduated: {edu.graduationDate}</p>
                  {edu.relevantCoursework && <p className="text-sm italic">Relevant Coursework: {edu.relevantCoursework}</p>}
                </div>
              ))}
            </section>
          )}
          
          {/* Skills */}
          {resumeData.skills && (
            <section className="mb-6">
               <h2 className={cn(
                "text-xl font-semibold border-b-2 pb-1 mb-2 flex items-center",
                selectedTemplateId === 'creative' ? "text-accent border-accent" : "text-primary border-primary"
              )}><Lightbulb className="mr-2 h-5 w-5"/> Skills</h2>
              <p className="text-sm leading-relaxed">{resumeData.skills.split(/,|\n/).map(skill => skill.trim()).filter(skill => skill).join(' • ')}</p>
            </section>
          )}

          {/* Projects */}
          {resumeData.projects.length > 0 && (
            <section className="mb-6">
              <h2 className={cn(
                "text-xl font-semibold border-b-2 pb-1 mb-2 flex items-center",
                selectedTemplateId === 'creative' ? "text-accent border-accent" : "text-primary border-primary"
              )}><FolderKanban className="mr-2 h-5 w-5"/> Projects</h2>
              {resumeData.projects.map((proj, index) => (
                <div key={proj.id || index} className="mb-4">
                  <div className="flex justify-between items-baseline">
                    <h3 className="text-lg font-medium">{proj.name}</h3>
                    {proj.link && <a href={proj.link} target="_blank" rel="noopener noreferrer" className="text-xs text-primary hover:underline flex items-center"><Globe className="mr-1 h-3 w-3"/>Link</a>}
                  </div>
                  <p className="text-sm text-muted-foreground italic mb-1">Technologies: {proj.technologies}</p>
                  <p className="text-sm leading-relaxed">{proj.description}</p>
                </div>
              ))}
            </section>
          )}
          
          {/* Custom Sections */}
          {resumeData.customSections.length > 0 && (
            resumeData.customSections.map((section, index) => (
              section.title && section.content && 
              <section key={section.id || index} className="mb-6">
                <h2 className={cn(
                  "text-xl font-semibold border-b-2 pb-1 mb-2",
                  selectedTemplateId === 'creative' ? "text-accent border-accent" : "text-primary border-primary"
                )}>{section.title}</h2>
                <p className="text-sm leading-relaxed whitespace-pre-line">{section.content}</p>
              </section>
            ))
          )}
        </div>
      </CardContent>
    </Card>
  );
};
