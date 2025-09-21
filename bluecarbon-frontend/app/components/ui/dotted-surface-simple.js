'use client';
import React from 'react';

export function DottedSurface({ className, ...props }) {
  return (
    <>
      {/* CSS-based animated background that always works */}
      <div
        style={{
          position: 'fixed',
          top: 0,
          left: 0,
          width: '100vw',
          height: '100vh',
          pointerEvents: 'none',
          zIndex: 0,
          background: `
            radial-gradient(circle at 20% 50%, rgba(79, 70, 229, 0.4) 0%, transparent 50%),
            radial-gradient(circle at 80% 20%, rgba(168, 85, 247, 0.4) 0%, transparent 50%),
            radial-gradient(circle at 40% 80%, rgba(59, 130, 246, 0.4) 0%, transparent 50%),
            radial-gradient(circle at 60% 30%, rgba(16, 185, 129, 0.3) 0%, transparent 50%)
          `,
          backgroundSize: '200% 200%',
          animation: 'floatingBG 15s ease-in-out infinite'
        }}
      />
      
      {/* Animated dots overlay */}
      <div
        style={{
          position: 'fixed',
          top: 0,
          left: 0,
          width: '100vw',
          height: '100vh',
          pointerEvents: 'none',
          zIndex: 0,
          backgroundImage: `
            radial-gradient(circle at 25% 25%, #4f46e5 2px, transparent 2px),
            radial-gradient(circle at 75% 25%, #7c3aed 2px, transparent 2px),
            radial-gradient(circle at 25% 75%, #3b82f6 2px, transparent 2px),
            radial-gradient(circle at 75% 75%, #10b981 2px, transparent 2px)
          `,
          backgroundSize: '100px 100px, 120px 120px, 80px 80px, 140px 140px',
          opacity: 0.6,
          animation: 'floatingDots 20s linear infinite'
        }}
      />

      <style jsx>{`
        @keyframes floatingBG {
          0%, 100% {
            background-position: 0% 50%, 100% 50%, 50% 100%, 50% 0%;
            transform: scale(1);
          }
          25% {
            background-position: 100% 0%, 0% 100%, 100% 50%, 0% 50%;
            transform: scale(1.05);
          }
          50% {
            background-position: 100% 100%, 0% 0%, 0% 0%, 100% 100%;
            transform: scale(1);
          }
          75% {
            background-position: 0% 100%, 100% 0%, 50% 0%, 50% 100%;
            transform: scale(1.02);
          }
        }

        @keyframes floatingDots {
          0% {
            background-position: 0px 0px, 0px 0px, 0px 0px, 0px 0px;
          }
          25% {
            background-position: 40px 20px, -20px 30px, 30px -10px, -40px 40px;
          }
          50% {
            background-position: 80px 40px, -40px 60px, 60px -20px, -80px 80px;
          }
          75% {
            background-position: 40px 60px, -60px 30px, 30px -30px, -40px 120px;
          }
          100% {
            background-position: 0px 80px, -80px 0px, 0px -40px, 0px 160px;
          }
        }
      `}</style>
    </>
  );
}