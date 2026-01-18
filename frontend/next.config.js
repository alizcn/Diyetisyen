/** @type {import('next').NextConfig} */
const nextConfig = {
  images: {
    remotePatterns: [
      {
        protocol: 'http',
        hostname: 'localhost',
        port: '8000',
        pathname: '/media/**',
      },
      {
        protocol: 'http',
        hostname: 'diyetisyen.apexdock.net',
        pathname: '/media/**',
      },
      {
        protocol: 'https',
        hostname: 'diyetisyen.apexdock.net',
        pathname: '/media/**',
      },
    ],
  },
};

module.exports = nextConfig;
