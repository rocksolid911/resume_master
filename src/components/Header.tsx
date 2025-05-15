import React from 'react';
import { Logo } from './Logo';

export const Header: React.FC = () => {
  return (
    <header className="py-6 mb-8 border-b border-border">
      <div className="container mx-auto flex justify-between items-center">
        <Logo />
      </div>
    </header>
  );
};
