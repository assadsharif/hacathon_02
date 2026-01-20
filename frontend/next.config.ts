import type { NextConfig } from "next";

const nextConfig: NextConfig = {
  reactStrictMode: true,
  // Enable standalone output for Docker deployment
  output: "standalone",
  // Configure API proxy to backend during development
  // In production, set NEXT_PUBLIC_API_URL to the deployed backend URL
  async rewrites() {
    const apiUrl = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";
    // Only use rewrites in development (when using localhost)
    if (apiUrl.includes("localhost")) {
      return [
        {
          source: "/api/todos/:path*",
          destination: `${apiUrl}/api/todos/:path*`,
        },
      ];
    }
    // In production, frontend calls backend directly via NEXT_PUBLIC_API_URL
    return [];
  },
};

export default nextConfig;
