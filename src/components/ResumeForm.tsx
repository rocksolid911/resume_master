"use client";

import React from 'react';
import { useForm, useFieldArray, Controller } from 'react-hook-form';
import { zodResolver } from '@hookform/resolvers/zod';
import * as z from 'zod';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Textarea } from '@/components/ui/textarea';
import { Checkbox } from '@/components/ui/checkbox';
import { Form, FormControl, FormDescription, FormField, FormItem, FormLabel, FormMessage } from '@/components/ui/form';
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from '@/components/ui/card';
import { Separator } from '@/components/ui/separator';
import { Briefcase, GraduationCap, Lightbulb, FolderKanban, User, PlusCircle, Trash2, Wand2 } from 'lucide-react';
import type { ResumeData } from '@/types/resume';

const experienceSchema = z.object({
  id: z.string().optional(),
  jobTitle: z.string().min(1, 'Job title is required'),
  company: z.string().min(1, 'Company name is required'),
  startDate: z.string().min(1, 'Start date is required'),
  endDate: z.string(),
  isCurrent: z.boolean().default(false),
  responsibilities: z.string().min(1, 'Responsibilities are required'),
});

const educationSchema = z.object({
  id: z.string().optional(),
  degree: z.string().min(1, 'Degree is required'),
  institution: z.string().min(1, 'Institution is required'),
  graduationDate: z.string().min(1, 'Graduation date is required'),
  relevantCoursework: z.string().optional(),
});

const projectSchema = z.object({
  id: z.string().optional(),
  name: z.string().min(1, 'Project name is required'),
  description: z.string().min(1, 'Description is required'),
  technologies: z.string().min(1, 'Technologies used are required'),
  link: z.string().url().optional().or(z.literal('')),
});

const customSectionSchema = z.object({
  id: z.string().optional(),
  title: z.string().min(1, 'Section title is required'),
  content: z.string().min(1, 'Content is required'),
});

const resumeFormSchema = z.object({
  name: z.string().min(1, 'Full name is required'),
  email: z.string().email('Invalid email address'),
  phone: z.string().min(1, 'Phone number is required'),
  linkedin: z.string().url('Invalid LinkedIn URL (must include http/https)').optional().or(z.literal('')),
  portfolio: z.string().url('Invalid Portfolio URL (must include http/https)').optional().or(z.literal('')),
  summary: z.string().optional(),
  experiences: z.array(experienceSchema),
  educationItems: z.array(educationSchema),
  skills: z.string().min(1, 'Skills are required'),
  projects: z.array(projectSchema),
  customSections: z.array(customSectionSchema),
});

interface ResumeFormProps {
  initialData: ResumeData;
  onFormChange: (data: ResumeData) => void;
}

export const ResumeForm: React.FC<ResumeFormProps> = ({ initialData, onFormChange }) => {
  const form = useForm<ResumeData>({
    resolver: zodResolver(resumeFormSchema),
    defaultValues: initialData,
    mode: 'onChange', // Validate on change to provide real-time feedback
  });

  const { fields: experienceFields, append: appendExperience, remove: removeExperience } = useFieldArray({
    control: form.control,
    name: 'experiences',
  });

  const { fields: educationFields, append: appendEducation, remove: removeEducation } = useFieldArray({
    control: form.control,
    name: 'educationItems',
  });
  
  const { fields: projectFields, append: appendProject, remove: removeProject } = useFieldArray({
    control: form.control,
    name: 'projects',
  });

  const { fields: customSectionFields, append: appendCustomSection, remove: removeCustomSection } = useFieldArray({
    control: form.control,
    name: 'customSections',
  });

  React.useEffect(() => {
    const subscription = form.watch((value) => {
      onFormChange(value as ResumeData);
    });
    return () => subscription.unsubscribe();
  }, [form, onFormChange]);


  return (
    <Form {...form}>
      <form className="space-y-8">
        <Card className="shadow-lg">
          <CardHeader>
            <CardTitle className="flex items-center"><User className="mr-2 h-6 w-6 text-primary" /> Personal Details</CardTitle>
            <CardDescription>Let's start with your basic information.</CardDescription>
          </CardHeader>
          <CardContent className="space-y-4">
            <FormField control={form.control} name="name" render={({ field }) => ( <FormItem> <FormLabel>Full Name</FormLabel> <FormControl><Input placeholder="e.g., Jane Doe" {...field} /></FormControl> <FormMessage /> </FormItem> )} />
            <div className="grid md:grid-cols-2 gap-4">
              <FormField control={form.control} name="email" render={({ field }) => ( <FormItem> <FormLabel>Email</FormLabel> <FormControl><Input type="email" placeholder="e.g., jane.doe@example.com" {...field} /></FormControl> <FormMessage /> </FormItem> )} />
              <FormField control={form.control} name="phone" render={({ field }) => ( <FormItem> <FormLabel>Phone</FormLabel> <FormControl><Input placeholder="e.g., (123) 456-7890" {...field} /></FormControl> <FormMessage /> </FormItem> )} />
            </div>
            <div className="grid md:grid-cols-2 gap-4">
              <FormField control={form.control} name="linkedin" render={({ field }) => ( <FormItem> <FormLabel>LinkedIn Profile URL</FormLabel> <FormControl><Input placeholder="e.g., https://linkedin.com/in/janedoe" {...field} /></FormControl> <FormMessage /> </FormItem> )} />
              <FormField control={form.control} name="portfolio" render={({ field }) => ( <FormItem> <FormLabel>Portfolio/Website URL</FormLabel> <FormControl><Input placeholder="e.g., https://janedoe.dev" {...field} /></FormControl> <FormMessage /> </FormItem> )} />
            </div>
             <FormField control={form.control} name="summary" render={({ field }) => ( <FormItem> <FormLabel>Summary/Objective</FormLabel> <FormControl><Textarea placeholder="A brief overview of your career goals and key qualifications." {...field} rows={4} /></FormControl> <FormDescription>This can also be generated or refined by AI later.</FormDescription> <FormMessage /> </FormItem> )} />
          </CardContent>
        </Card>

        <Card className="shadow-lg">
          <CardHeader>
            <CardTitle className="flex items-center"><Briefcase className="mr-2 h-6 w-6 text-primary" /> Work Experience</CardTitle>
            <CardDescription>Detail your professional roles and responsibilities.</CardDescription>
          </CardHeader>
          <CardContent className="space-y-6">
            {experienceFields.map((field, index) => (
              <div key={field.id} className="p-4 border rounded-md space-y-4 relative shadow-sm bg-card">
                <FormField control={form.control} name={`experiences.${index}.jobTitle`} render={({ field }) => ( <FormItem> <FormLabel>Job Title</FormLabel> <FormControl><Input placeholder="e.g., Software Engineer" {...field} /></FormControl> <FormMessage /> </FormItem> )} />
                <FormField control={form.control} name={`experiences.${index}.company`} render={({ field }) => ( <FormItem> <FormLabel>Company</FormLabel> <FormControl><Input placeholder="e.g., Tech Solutions Inc." {...field} /></FormControl> <FormMessage /> </FormItem> )} />
                <div className="grid md:grid-cols-2 gap-4">
                  <FormField control={form.control} name={`experiences.${index}.startDate`} render={({ field }) => ( <FormItem> <FormLabel>Start Date</FormLabel> <FormControl><Input type="month" {...field} /></FormControl> <FormMessage /> </FormItem> )} />
                  <FormField control={form.control} name={`experiences.${index}.endDate`} render={({ field }) => ( <FormItem> <FormLabel>End Date</FormLabel> <FormControl><Input type="month" {...field} disabled={form.watch(`experiences.${index}.isCurrent`)} /></FormControl> <FormMessage /> </FormItem> )} />
                </div>
                <FormField control={form.control} name={`experiences.${index}.isCurrent`} render={({ field }) => ( <FormItem className="flex flex-row items-start space-x-3 space-y-0"> <FormControl><Checkbox checked={field.value} onCheckedChange={field.onChange} /></FormControl> <FormLabel className="font-normal">I currently work here</FormLabel> </FormItem>)} />
                <FormField control={form.control} name={`experiences.${index}.responsibilities`} render={({ field }) => ( <FormItem> <FormLabel>Responsibilities & Achievements</FormLabel> <FormControl><Textarea placeholder="Describe your key duties and accomplishments. Use bullet points for clarity." {...field} rows={5} /></FormControl> <FormMessage /> </FormItem> )} />
                <Button type="button" variant="ghost" size="icon" className="absolute top-2 right-2 text-destructive hover:text-destructive-foreground hover:bg-destructive" onClick={() => removeExperience(index)}><Trash2 className="h-4 w-4" /></Button>
              </div>
            ))}
            <Button type="button" variant="outline" onClick={() => appendExperience({ id: Date.now().toString(), jobTitle: '', company: '', startDate: '', endDate: '', isCurrent: false, responsibilities: '' })}> <PlusCircle className="mr-2 h-4 w-4" /> Add Experience </Button>
          </CardContent>
        </Card>

        <Card className="shadow-lg">
          <CardHeader>
            <CardTitle className="flex items-center"><GraduationCap className="mr-2 h-6 w-6 text-primary" /> Education</CardTitle>
            <CardDescription>List your educational qualifications.</CardDescription>
          </CardHeader>
          <CardContent className="space-y-6">
            {educationFields.map((field, index) => (
              <div key={field.id} className="p-4 border rounded-md space-y-4 relative shadow-sm bg-card">
                <FormField control={form.control} name={`educationItems.${index}.degree`} render={({ field }) => ( <FormItem> <FormLabel>Degree/Certificate</FormLabel> <FormControl><Input placeholder="e.g., B.S. in Computer Science" {...field} /></FormControl> <FormMessage /> </FormItem> )} />
                <FormField control={form.control} name={`educationItems.${index}.institution`} render={({ field }) => ( <FormItem> <FormLabel>Institution</FormLabel> <FormControl><Input placeholder="e.g., University of Technology" {...field} /></FormControl> <FormMessage /> </FormItem> )} />
                <FormField control={form.control} name={`educationItems.${index}.graduationDate`} render={({ field }) => ( <FormItem> <FormLabel>Graduation Date</FormLabel> <FormControl><Input type="month" {...field} /></FormControl> <FormMessage /> </FormItem> )} />
                <FormField control={form.control} name={`educationItems.${index}.relevantCoursework`} render={({ field }) => ( <FormItem> <FormLabel>Relevant Coursework (Optional)</FormLabel> <FormControl><Input placeholder="e.g., Data Structures, Algorithms" {...field} /></FormControl> <FormMessage /> </FormItem> )} />
                <Button type="button" variant="ghost" size="icon" className="absolute top-2 right-2 text-destructive hover:text-destructive-foreground hover:bg-destructive" onClick={() => removeEducation(index)}><Trash2 className="h-4 w-4" /></Button>
              </div>
            ))}
            <Button type="button" variant="outline" onClick={() => appendEducation({ id: Date.now().toString(), degree: '', institution: '', graduationDate: '', relevantCoursework: '' })}> <PlusCircle className="mr-2 h-4 w-4" /> Add Education </Button>
          </CardContent>
        </Card>

        <Card className="shadow-lg">
          <CardHeader>
            <CardTitle className="flex items-center"><Lightbulb className="mr-2 h-6 w-6 text-primary" /> Skills</CardTitle>
            <CardDescription>Highlight your key skills. You can separate them with commas or new lines.</CardDescription>
          </CardHeader>
          <CardContent>
            <FormField control={form.control} name="skills" render={({ field }) => ( <FormItem> <FormControl><Textarea placeholder="e.g., JavaScript, React, Node.js, Project Management, Agile Methodologies" {...field} rows={5} /></FormControl> <FormMessage /> </FormItem> )} />
          </CardContent>
        </Card>
        
        <Card className="shadow-lg">
          <CardHeader>
            <CardTitle className="flex items-center"><FolderKanban className="mr-2 h-6 w-6 text-primary" /> Projects</CardTitle>
            <CardDescription>Showcase your personal or professional projects.</CardDescription>
          </CardHeader>
          <CardContent className="space-y-6">
            {projectFields.map((field, index) => (
              <div key={field.id} className="p-4 border rounded-md space-y-4 relative shadow-sm bg-card">
                <FormField control={form.control} name={`projects.${index}.name`} render={({ field }) => ( <FormItem> <FormLabel>Project Name</FormLabel> <FormControl><Input {...field} /></FormControl> <FormMessage /> </FormItem> )} />
                <FormField control={form.control} name={`projects.${index}.description`} render={({ field }) => ( <FormItem> <FormLabel>Description</FormLabel> <FormControl><Textarea {...field} rows={3} /></FormControl> <FormMessage /> </FormItem> )} />
                <FormField control={form.control} name={`projects.${index}.technologies`} render={({ field }) => ( <FormItem> <FormLabel>Technologies Used</FormLabel> <FormControl><Input placeholder="e.g., React, Firebase, Tailwind CSS" {...field} /></FormControl> <FormMessage /> </FormItem> )} />
                <FormField control={form.control} name={`projects.${index}.link`} render={({ field }) => ( <FormItem> <FormLabel>Project Link (Optional)</FormLabel> <FormControl><Input placeholder="https://github.com/user/project" {...field} /></FormControl> <FormMessage /> </FormItem> )} />
                <Button type="button" variant="ghost" size="icon" className="absolute top-2 right-2 text-destructive hover:text-destructive-foreground hover:bg-destructive" onClick={() => removeProject(index)}><Trash2 className="h-4 w-4" /></Button>
              </div>
            ))}
            <Button type="button" variant="outline" onClick={() => appendProject({ id: Date.now().toString(), name: '', description: '', technologies: '', link: '' })}> <PlusCircle className="mr-2 h-4 w-4" /> Add Project </Button>
          </CardContent>
        </Card>

        <Card className="shadow-lg">
          <CardHeader>
            <CardTitle className="flex items-center"><Wand2 className="mr-2 h-6 w-6 text-primary" /> Custom Sections</CardTitle>
            <CardDescription>Add any other relevant sections (e.g., Certifications, Awards).</CardDescription>
          </CardHeader>
          <CardContent className="space-y-6">
            {customSectionFields.map((field, index) => (
              <div key={field.id} className="p-4 border rounded-md space-y-4 relative shadow-sm bg-card">
                <FormField control={form.control} name={`customSections.${index}.title`} render={({ field }) => ( <FormItem> <FormLabel>Section Title</FormLabel> <FormControl><Input placeholder="e.g., Certifications" {...field} /></FormControl> <FormMessage /> </FormItem> )} />
                <FormField control={form.control} name={`customSections.${index}.content`} render={({ field }) => ( <FormItem> <FormLabel>Content</FormLabel> <FormControl><Textarea {...field} rows={4} /></FormControl> <FormMessage /> </FormItem> )} />
                <Button type="button" variant="ghost" size="icon" className="absolute top-2 right-2 text-destructive hover:text-destructive-foreground hover:bg-destructive" onClick={() => removeCustomSection(index)}><Trash2 className="h-4 w-4" /></Button>
              </div>
            ))}
            <Button type="button" variant="outline" onClick={() => appendCustomSection({ id: Date.now().toString(), title: '', content: '' })}> <PlusCircle className="mr-2 h-4 w-4" /> Add Custom Section </Button>
          </CardContent>
        </Card>

        <Separator />
        <div className="text-sm text-muted-foreground">
          Your data is auto-saved as you type. Proceed to other tabs to enhance and preview your resume.
        </div>
      </form>
    </Form>
  );
};
