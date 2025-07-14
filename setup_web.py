#!/usr/bin/env python3
"""
Setup script for CrewBuilder Web Interface
Creates the necessary configuration files for the Next.js frontend
"""

import json
import os

def create_package_json():
    """Create package.json for Next.js project"""
    package_config = {
        "name": "crewbuilder-web",
        "version": "0.1.0",
        "private": True,
        "scripts": {
            "dev": "next dev",
            "build": "next build",
            "start": "next start",
            "lint": "next lint"
        },
        "dependencies": {
            "next": "14.0.0",
            "react": "^18.0.0",
            "react-dom": "^18.0.0",
            "@types/node": "^20.0.0",
            "@types/react": "^18.0.0",
            "@types/react-dom": "^18.0.0",
            "typescript": "^5.0.0",
            "tailwindcss": "^3.3.0",
            "autoprefixer": "^10.4.16",
            "postcss": "^8.4.31",
            "lucide-react": "^0.292.0",
            "framer-motion": "^10.16.5",
            "axios": "^1.6.0",
            "zustand": "^4.4.7"
        },
        "devDependencies": {
            "eslint": "^8.0.0",
            "eslint-config-next": "14.0.0"
        }
    }
    
    os.makedirs("web", exist_ok=True)
    with open("web/package.json", "w") as f:
        json.dump(package_config, f, indent=2)
    print("Created web/package.json")

def create_tailwind_config():
    """Create Tailwind CSS configuration"""
    config_content = '''/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    './pages/**/*.{js,ts,jsx,tsx,mdx}',
    './components/**/*.{js,ts,jsx,tsx,mdx}',
    './app/**/*.{js,ts,jsx,tsx,mdx}',
  ],
  theme: {
    extend: {},
  },
  plugins: [],
}'''
    
    with open("web/tailwind.config.js", "w") as f:
        f.write(config_content)
    print("Created web/tailwind.config.js")

def create_typescript_config():
    """Create TypeScript configuration"""
    ts_config = {
        "compilerOptions": {
            "target": "es5",
            "lib": ["dom", "dom.iterable", "es6"],
            "allowJs": True,
            "skipLibCheck": True,
            "strict": True,
            "noEmit": True,
            "esModuleInterop": True,
            "module": "esnext",
            "moduleResolution": "bundler",
            "resolveJsonModule": True,
            "isolatedModules": True,
            "jsx": "preserve",
            "incremental": True,
            "plugins": [
                {
                    "name": "next"
                }
            ],
            "paths": {
                "@/*": ["./src/*"]
            }
        },
        "include": ["next-env.d.ts", "**/*.ts", "**/*.tsx", ".next/types/**/*.ts"],
        "exclude": ["node_modules"]
    }
    
    with open("web/tsconfig.json", "w") as f:
        json.dump(ts_config, f, indent=2)
    print("Created web/tsconfig.json")

if __name__ == "__main__":
    print("Setting up CrewBuilder Web Interface...")
    create_package_json()
    create_tailwind_config()
    create_typescript_config()
    print("Web interface setup complete!")
    print("\nNext steps:")
    print("1. cd web")
    print("2. npm install")
    print("3. npm run dev")
