"use client";

import React from 'react';
import { Button } from '@/components/ui/button';
import { Download } from 'lucide-react';
import html2canvas from 'html2canvas';
import jsPDF from 'jspdf';
import { useToast } from "@/hooks/use-toast";

interface PdfExportButtonProps {
  targetRef: React.RefObject<HTMLElement>;
  fileName?: string;
  resumeDataExists: boolean;
}

export const PdfExportButton: React.FC<PdfExportButtonProps> = ({ targetRef, fileName = "ResuMaster_AI_Resume.pdf", resumeDataExists }) => {
  const { toast } = useToast();
  const [isExporting, setIsExporting] = React.useState(false);

  const handleExport = async () => {
    if (!resumeDataExists) {
      toast({
        title: "Cannot Export PDF",
        description: "Please fill in some resume data before exporting.",
        variant: "destructive",
      });
      return;
    }
    if (targetRef.current) {
      setIsExporting(true);
      try {
        // Give a brief moment for any final rendering updates
        await new Promise(resolve => setTimeout(resolve, 100));

        const canvas = await html2canvas(targetRef.current, { 
          scale: 2, // Higher scale for better quality
          useCORS: true, // If you have external images
          logging: false, // Disable logging to console
          backgroundColor: null, // Use element's background
         });
        const imgData = canvas.toDataURL('image/png');
        
        const pdf = new jsPDF({
          orientation: 'portrait',
          unit: 'pt',
          format: 'a4',
        });

        const pdfWidth = pdf.internal.pageSize.getWidth();
        const pdfHeight = pdf.internal.pageSize.getHeight();
        
        const imgProps= pdf.getImageProperties(imgData);
        const imgWidth = imgProps.width;
        const imgHeight = imgProps.height;

        // Calculate the ratio to fit the image within the PDF page
        const widthRatio = pdfWidth / imgWidth;
        const heightRatio = pdfHeight / imgHeight;
        const ratio = Math.min(widthRatio, heightRatio);

        const newImgWidth = imgWidth * ratio;
        const newImgHeight = imgHeight * ratio;
        
        // Center the image on the PDF page (optional)
        const x = (pdfWidth - newImgWidth) / 2;
        const y = 0; // Start from top; can add margin if needed

        pdf.addImage(imgData, 'PNG', x, y, newImgWidth, newImgHeight);
        pdf.save(fileName);
        toast({
          title: "Export Successful",
          description: `Your resume has been downloaded as ${fileName}.`,
        });
      } catch (error) {
        console.error("Error exporting PDF:", error);
        toast({
          title: "Export Failed",
          description: "An error occurred while exporting your resume to PDF.",
          variant: "destructive",
        });
      } finally {
        setIsExporting(false);
      }
    } else {
       toast({
        title: "Export Error",
        description: "Preview content not found. Cannot export PDF.",
        variant: "destructive",
      });
    }
  };

  return (
    <Button onClick={handleExport} variant="default" className="w-full sm:w-auto" disabled={isExporting || !resumeDataExists}>
      {isExporting ? <Loader2 className="mr-2 h-4 w-4 animate-spin" /> : <Download className="mr-2 h-4 w-4" />}
      {isExporting ? 'Exporting...' : 'Download as PDF'}
    </Button>
  );
};
