import { Wand2 } from 'lucide-react';
import React from 'react';

export const Logo: React.FC = () => {
  return (
    <div className="flex items-center space-x-2">
      <Wand2 className="h-8 w-8 text-primary" />
      <h1 className="text-2xl font-bold text-primary">ResuMaster AI</h1>
    </div>
  );
};
