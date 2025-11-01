import React from 'react';
import { useNavigate } from 'react-router-dom';
import { Scale, FileText, Zap, Shield } from 'lucide-react';

export const Landing = () => {
    const navigate = useNavigate();

    return (
        <div className="min-h-screen bg-gradient-to-br from-slate-900 via-slate-800 to-slate-900 text-white overflow-hidden">
            {/* Navigation */}
            <nav className="flex justify-between items-center px-8 py-6 border-b border-slate-700 bg-slate-950 relative z-10">
                <div className="flex items-center gap-3">
                    <div className="bg-blue-500 p-2 rounded-lg">
                        <Scale size={30} />
                    </div>
                    <h1 className="text-3xl font-bold">LexoraAI</h1>
                </div>
                <div className="flex gap-5">
                <button
                    onClick={() => navigate('/signin')}
                    className="px-6 py-2 bg-slate-700 hover:bg-slate-600 rounded-lg font-semibold transition text-white" >
                    Sign In
                </button>

                    <button
                        onClick={() => navigate('/signup')}
                        className="px-6 py-2 bg-blue-600 hover:bg-blue-700 rounded-lg transition font-semibold"
                    >
                        Sign Up
                    </button>
                </div>
            </nav>


            {/* Hero Section with Background */}
            <div className="relative min-h-[calc(100vh-80px)] flex items-center justify-center overflow-hidden">
            {/* Wave Background */}
<div className="absolute inset-0 opacity-30">
    <svg className="w-full h-full" viewBox="0 0 1200 600" preserveAspectRatio="none">
        <defs>
            <linearGradient id="waveGrad" x1="0%" y1="0%" x2="100%" y2="100%">
                <stop offset="0%" stopColor="#3b82f6" stopOpacity="0.4" />
                <stop offset="50%" stopColor="#8b5cf6" stopOpacity="0.3" />
                <stop offset="100%" stopColor="#ec4899" stopOpacity="0.4" />
            </linearGradient>
        </defs>
        <path d="M0,300 Q300,250 600,300 T1200,300 L1200,600 L0,600 Z" fill="url(#waveGrad)">
            <animate attributeName="d" 
                values="M0,300 Q300,250 600,300 T1200,300 L1200,600 L0,600 Z;
                        M0,300 Q300,350 600,300 T1200,300 L1200,600 L0,600 Z;
                        M0,300 Q300,250 600,300 T1200,300 L1200,600 L0,600 Z"
                dur="6s" repeatCount="indefinite" />
        </path>
        <path d="M0,350 Q300,300 600,350 T1200,350 L1200,600 L0,600 Z" fill="url(#waveGrad)" opacity="0.5">
            <animate attributeName="d" 
                values="M0,350 Q300,300 600,350 T1200,350 L1200,600 L0,600 Z;
                        M0,350 Q300,400 600,350 T1200,350 L1200,600 L0,600 Z;
                        M0,350 Q300,300 600,350 T1200,350 L1200,600 L0,600 Z"
                dur="8s" repeatCount="indefinite" />
        </path>
    </svg>
</div>




                {/* Content */}
                <div className="max-w-6xl mx-auto px-8 py-20 relative z-5 text-center">
                    <div className="mb-16">
                        <h2 className="text-6xl font-bold mb-6 leading-tight">
                            Your AI Legal <span className="text-blue-400">Assistant</span>
                        </h2>
                        <p className="text-xl text-slate-400 mb-8 max-w-2xl mx-auto">
                            Upload legal documents and get instant AI-powered insights. Ask questions, get answers in seconds.
                        </p>
                        <button
                            onClick={() => navigate('/signup')}
                            className="px-8 py-4 bg-blue-600 hover:bg-blue-700 rounded-lg text-lg font-semibold transition"
                        >
                            Get Started
                        </button>
                    </div>

                    {/* Features */}
                    <div className="grid grid-cols-1 md:grid-cols-3 gap-8 mt-20">
                        <div className="bg-slate-800 bg-opacity-50 backdrop-blur p-8 rounded-lg border border-slate-700 hover:border-blue-500 transition">
                            <FileText size={40} className="text-blue-400 mb-4 mx-auto" />
                            <h3 className="text-xl font-bold mb-3">Upload Documents</h3>
                            <p className="text-slate-400">
                                Upload any legal document. LexoraAI processes it instantly and makes it searchable.
                            </p>
                        </div>

                        <div className="bg-slate-800 bg-opacity-50 backdrop-blur p-8 rounded-lg border border-slate-700 hover:border-blue-500 transition">
                            <Zap size={40} className="text-yellow-400 mb-4 mx-auto" />
                            <h3 className="text-xl font-bold mb-3">Instant Answers</h3>
                            <p className="text-slate-400">
                                Ask complex legal questions and get comprehensive answers powered by AI.
                            </p>
                        </div>

                        <div className="bg-slate-800 bg-opacity-50 backdrop-blur p-8 rounded-lg border border-slate-700 hover:border-blue-500 transition">
                            <Shield size={40} className="text-green-400 mb-4 mx-auto" />
                            <h3 className="text-xl font-bold mb-3">Secure & Private</h3>
                            <p className="text-slate-400">
                                Your documents are encrypted and never shared. Complete privacy guaranteed.
                            </p>
                        </div>
                    </div>
                </div>
            </div>

            {/* Footer */}
            <div className="border-t border-slate-600 bg-slate-950 py-8 text-center text-slate-400 relative z-10">
                <p>© 2025 LexoraAI. All rights reserved.</p>
            </div>

        </div>
    );
};
