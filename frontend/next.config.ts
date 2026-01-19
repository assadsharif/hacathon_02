import type { NextConfig } from "next";

const nextConfig: NextConfig = {
  reactStrictMode: true,
  // Configure API proxy to backend during development
  // Exclude /api/auth/* to allow Better Auth to handle authentication
  async rewrites() {
    return [
      {
        source: "/api/todos/:path*",
        destination: "http://localhost:8000/api/todos/:path*",
      },
    ];
  },
};

export default nextConfig;
