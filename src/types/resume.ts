export type ResumeExperience = {
  id: string;
  jobTitle: string;
  company: string;
  startDate: string;
  endDate: string;
  isCurrent: boolean;
  responsibilities: string;
};

export type ResumeEducation = {
  id: string;
  degree: string;
  institution: string;
  graduationDate: string;
  relevantCoursework?: string;
};

export type ResumeProject = {
  id: string;
  name: string;
  description: string;
  technologies: string;
  link?: string;
};

export type ResumeCustomSection = {
  id: string;
  title: string;
  content: string;
};

export type ResumeData = {
  name: string;
  email: string;
  phone: string;
  linkedin: string;
  portfolio: string;
  summary: string;
  experiences: ResumeExperience[];
  educationItems: ResumeEducation[]; // Renamed to avoid conflict with Education component if any
  skills: string;
  projects: ResumeProject[];
  customSections: ResumeCustomSection[];
};

export const initialResumeData: ResumeData = {
  name: '',
  email: '',
  phone: '',
  linkedin: '',
  portfolio: '',
  summary: '',
  experiences: [],
  educationItems: [],
  skills: '',
  projects: [],
  customSections: [],
};

// Function to convert ResumeData to a plain text string for AI input
export const resumeDataToText = (data: ResumeData | null): string => {
  if (!data) return "";
  
  let text = `Name: ${data.name}\nEmail: ${data.email}\nPhone: ${data.phone}\n`;
  if (data.linkedin) text += `LinkedIn: ${data.linkedin}\n`;
  if (data.portfolio) text += `Portfolio: ${data.portfolio}\n`;
  
  if (data.summary) {
    text += `\nSummary:\n${data.summary}\n`;
  }

  if (data.experiences.length > 0) {
    text += "\nExperience:\n";
    data.experiences.forEach(exp => {
      text += `- ${exp.jobTitle} at ${exp.company} (${exp.startDate} - ${exp.isCurrent ? 'Present' : exp.endDate})\n  Responsibilities:\n${exp.responsibilities.split('\n').map(line => `    ${line}`).join('\n')}\n`;
    });
  }

  if (data.educationItems.length > 0) {
    text += "\nEducation:\n";
    data.educationItems.forEach(edu => {
      text += `- ${edu.degree} from ${edu.institution} (Graduated: ${edu.graduationDate})\n`;
      if (edu.relevantCoursework) text += `  Relevant Coursework: ${edu.relevantCoursework}\n`;
    });
  }
  
  if (data.skills) {
    text += `\nSkills:\n${data.skills}\n`;
  }

  if (data.projects.length > 0) {
    text += "\nProjects:\n";
    data.projects.forEach(proj => {
      text += `- ${proj.name}: ${proj.description}\n  Technologies: ${proj.technologies}\n`;
      if (proj.link) text += `  Link: ${proj.link}\n`;
    });
  }

  if (data.customSections.length > 0) {
    data.customSections.forEach(section => {
      text += `\n${section.title}:\n${section.content}\n`;
    });
  }

  return text.trim();
};
