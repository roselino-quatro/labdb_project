import { ReactNode } from 'react';
import Navbar from './Navbar';
import Footer from './Footer';
import Messages from './Messages';

interface LayoutProps {
  children: ReactNode;
  hideNavbar?: boolean;
  hideFooter?: boolean;
  mainClass?: string;
  messages?: Array<{ category: 'success' | 'error' | 'warning' | 'info'; text: string }>;
  hideDebugButtons?: boolean;
}

export default function Layout({
  children,
  hideNavbar = false,
  hideFooter = false,
  mainClass = 'mx-auto w-full max-w-6xl p-6 flex-1',
  messages,
  hideDebugButtons = false,
}: LayoutProps) {
  return (
    <div className="min-h-screen bg-gray-100 text-gray-900 flex flex-col">
      {!hideNavbar && <Navbar />}
      <main className={mainClass}>
        {messages && <Messages messages={messages} />}
        {children}
      </main>
      {!hideFooter && <Footer />}
    </div>
  );
}
