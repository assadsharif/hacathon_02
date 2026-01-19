'use client';

import "./globals.css";

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en" style={{ backgroundColor: '#f0f2f5', colorScheme: 'light' }}>
      <head>
        <title>Todo App</title>
        <meta name="description" content="Simple todo application" />
        <meta name="color-scheme" content="light only" />
      </head>
      <body style={{ backgroundColor: '#f0f2f5', color: '#1c1e21', margin: 0, padding: 0 }}>
        {children}
      </body>
    </html>
  );
}
